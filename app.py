import os
import threading
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import pandas as pd
import time
from werkzeug.utils import secure_filename
from db.database import init_db
from db.models import db, Mapping, File
from process import process_csv_file
from project_logger import logger

processing_thread = None
processing_file = None

app = Flask(__name__, static_folder='client/build')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/project_db.db')

CORS(app)  # This will enable CORS for all routes
init_db(app)

def save_mapping_to_db(mapping, update_existing=True):
    for header, category in mapping.items():
        existing_mapping = Mapping.query.filter_by(spec=header).first()
        if existing_mapping is not None:
            # If a mapping for this header already exists, update it
            if update_existing:
                existing_mapping.category = category
        else:
            # Otherwise, create a new mapping
            new_mapping = Mapping(spec=header, category=category)
            db.session.add(new_mapping)
    db.session.commit()
    
def unique_filename(base_filename):
    base_name, ext = os.path.splitext(base_filename)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    unique_filename = f"{base_name}-{timestamp}{ext}"
    return unique_filename

@app.route('/api/upload', methods=['POST'])
def upload():
    global processing_thread
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and secure_filename(file.filename):
        filename = secure_filename(file.filename)
        filename = unique_filename(filename)
        new_file = File(file_name=filename)
        db.session.add(new_file)
        file.save(os.path.join('data/input/', f'input_{filename}'))
        new_file.update_file_metrics()
        db.session.commit()
        return jsonify({'message': 'File uploaded succesfully'}), 200

@app.route('/api/files', methods=['GET'])
def get_files():
    files = File.query.all()
    for file in files:
        file.update_file_metrics()
    db.session.commit()  # Make sure to commit the changes to the database
    return jsonify([file.to_dict() for file in files]), 200

@app.route('/api/data', methods=['POST'])
def get_csv_data():
    filepath = request.json.get('filepath')  # Get file path from request body
    # Check if the file exists
    if not os.path.exists(filepath):
        return jsonify([])  # Return an empty array if the file does not exist
    
    df = pd.read_csv(filepath)
    df = df.fillna('')  # Replace NaN values with ''
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/download', methods=['GET'])
def download_file():
    filepath = request.args.get('file')
    return send_file(filepath, as_attachment=True)
    
@app.route('/api/process', methods=['POST'])
def process():
    global processing_thread
    global processing_file
    if processing_thread and processing_thread.is_alive():
        return jsonify({'error': 'Processing thread is already running'}), 400
    filename = request.json.get('fileName')
    file = File.query.filter_by(file_name=filename).first()
    if file and file.status == 'Complete':
        return jsonify({'error': 'File processing is already complete'}), 400
    processing_thread = threading.Thread(target=process_csv_file, args=(filename,))
    processing_thread.start()
    processing_file = filename
    return jsonify({'message': 'Processing started'}), 200

@app.route('/api/check-process', methods=['GET'])
def check_process():
    global processing_thread
    global processing_file
    if processing_thread and processing_thread.is_alive():
        return jsonify({'isProcessing': True, 'fileName': processing_file}), 200
    else:
        processing_thread = None
        processing_file = None
        return jsonify({'isProcessing': False}), 200
    
@app.route('/api/get_mapping', methods=['POST'])
def get_mapping():
    # Get all mappings from the database
    filepath = request.json.get('filepath')

    if filepath:
        # If a file path is provided, return mapping for each header in the file
        data = pd.read_csv(filepath, nrows=0)  # Read just the headers
        headers = data.columns.tolist()

        # Convert the query result to a dictionary
        mappings = Mapping.query.all()
        mapping_dict = {mapping.spec: mapping.category for mapping in mappings}

        # Check for new headers and add them to the database
        new_headers = set(headers) - set(mapping_dict.keys())
        if new_headers:
            new_mapping = {header: 'Category 1' for header in new_headers}
            save_mapping_to_db(new_mapping, update_existing=False)

        # Update the mapping dictionary with the latest database entries
        mappings = Mapping.query.filter(Mapping.spec.in_(headers)).all()
    else:
        mappings = Mapping.query.all()

    # Convert the query result to a dictionary
    mapping_dict = {mapping.spec: mapping.category for mapping in mappings}

    return jsonify(mapping_dict)


@app.route('/api/save_mapping', methods=['POST'])
def save_mapping():
    mapping = request.json  # Get the user-created mapping
    # Save the mapping to the database
    save_mapping_to_db(mapping)
    return jsonify({'message': 'Mapping saved successfully'})

@app.route('/api/compress', methods=['POST'])
def compress():
    filename = request.json.get('filename')
    data = pd.read_csv(f'data/specs/specs_{filename}')
    headers = data.columns.tolist()
    mappings = Mapping.query.filter(Mapping.spec.in_(headers)).all()
    mappings = {mapping.spec: mapping.category for mapping in mappings}

    # Initialize the categories in the DataFrame
    for category in ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5']:
        data[category] = ''

    # Compress the columns based on the mapping
    for header, category in mappings.items():
        # Check if the header exists in the DataFrame and is not 'keyword' or 'id'
        if header in data.columns and header not in ['keyword', 'Keyword']:
            # Append the values of the header to the corresponding category, ignoring NaN values
            data[category] = data.apply(lambda row: ', '.join(filter(None, [row[category], str(row[header]) if pd.notna(row[header]) else ''])), axis=1)

    # Drop the original columns, excluding 'keyword' and 'id'
    columns_to_drop = [key for key in mappings.keys() if key not in ['keyword', 'id']]
    data.drop(columns=columns_to_drop, inplace=True)
    # Save the output to a CSV file
    data.to_csv(f'data/compressed/compressed_{filename}', index=False)
    return data.to_json(orient='records')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)

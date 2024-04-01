import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Mapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spec = db.Column(db.String(80), unique=True, nullable=False)  # spec is now a unique key
    category = db.Column(db.String(80), nullable=False, default='Category 1')  # category for the spec
    
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(80), nullable=False, default='New')
    total_records = db.Column(db.Integer, nullable=False, default=0)
    total_specs = db.Column(db.Integer, nullable=False, default=0)
    total_remaining = db.Column(db.Integer, nullable=False, default=0)
    total_compressed = db.Column(db.Integer, nullable=False, default=0)
    total_failed = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def update_file_metrics(self):
        input_path = f'data/input/input_{self.file_name}'
        specs_path = f'data/specs/specs_{self.file_name}'
        compressed_path = f'data/compressed/compressed_{self.file_name}'
        failed_path = f'data/failed/failed_{self.file_name}'

        self.total_records = self.count_lines(input_path)
        self.total_specs = self.count_lines(specs_path)
        self.total_remaining = self.total_records - self.total_specs
        self.total_compressed = self.count_lines(compressed_path)
        self.total_failed = self.count_lines(failed_path)

        if self.total_specs > 0:
            self.status = 'Complete' if self.total_records == self.total_specs else 'In Progress'
        else:
            self.status = 'New'

    @staticmethod
    def count_lines(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return sum(1 for _ in file)
        return 0

    def to_dict(self):
        return {
            'id': self.id,
            'file_name': self.file_name,
            'status': self.status,
            'total_records': self.total_records,
            'total_specs': self.total_specs,
            'total_remaining': self.total_remaining,
            'total_compressed': self.total_compressed,
            'total_failed': self.total_failed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

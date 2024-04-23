import csv
import json
import os
import pandas as pd
from dotenv import load_dotenv
from ai import add_message, run_assistant, check_run_status, get_thread_messages, create_thread
import time
from project_logger import logger

load_dotenv()

def read_csv(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Skip empty rows
                data.append(row[0])
    return data

def write_json(filename, data):
    with open(filename, 'a') as file:
        json.dump(data, file, indent=4)

def process_csv_file(filename):
    logger.info(f'Processing file: {filename}')
    if not os.path.exists(f'data/specs/specs_{filename}'):
        with open(f'data/specs/specs_{filename}', 'a') as f:
            pass

    if not os.path.exists(f'data/output/failed_{filename}'):
        with open(f'data/failed/failed_{filename}', 'a') as f:
            pass  
    
    df = pd.DataFrame()
    processed_keywords = read_csv(f'data/specs/specs_{filename}')
    with open(f'data/input/input_{filename}', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            keyword = row[0]
            if keyword in ['Keyword', 'Keywords', 'keyword', 'keywords']:
                continue
            if not keyword in processed_keywords:
                threadId = create_thread()
                add_message(keyword, threadId)
                runId = run_assistant(threadId)
                time.sleep(5)
                status = check_run_status(threadId, runId)
                while not status == 'completed':
                    time.sleep(2)
                    status = check_run_status(threadId, runId)
                    print(f'Keyword: {row[0]} - Status: {status}')
                    if status in ['expired', 'failed']:
                        with open(f'data/failed/failed_{filename}', 'a', newline='') as file:
                            writer = csv.writer(file)
                            if keyword:
                                writer.writerow([keyword])
                            break
                if status in ['expired', 'failed']:
                    continue
                                    
                messages = get_thread_messages(threadId)


                for message in messages.data:
                    if keyword not in processed_keywords:
                        try:
                            message_content = json.loads(message.content[0].text.value)

                            output_data = {
                                'keyword': keyword,
                                'Name': message_content['Name'],
                                'Category': message_content['Category'],
                            }
                            output_data.update(message_content['Specs'])

                            df = pd.concat([df, pd.DataFrame([output_data])], ignore_index=True)

                            df.to_csv(f'data/specs/specs_{filename}', index=False)

                            processed_keywords.append(keyword)
                        except Exception as e:
                            logger.error(f'Error processing keyword: {keyword} - {e}')
                            with open(f'data/failed/failed_{filename}', 'a', newline='') as file:
                                writer = csv.writer(file)
                                if keyword:
                                    writer.writerow([keyword])

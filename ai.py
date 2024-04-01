import os
from dotenv import load_dotenv
from openai import OpenAI
from project_logger import logger

load_dotenv()

assistant_id = os.getenv('OPENAI_ASSISTANT_ID')
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError('Missing OpenAI API Key')

client = OpenAI(api_key=api_key)

def create_thread():
    try:
        thread = client.beta.threads.create()
        return thread.id
    except Exception as e:
        print(f'Error creating thread {str(e)}')
        logger.error(f'Error creating thread {str(e)}')
        raise

def add_message(message, threadId):
    try:
        message = client.beta.threads.messages.create(
            thread_id=threadId,
            role='user',
            content= message
        )
        return message.id
    except Exception as e:
        print(f'Error adding message {str(e)}')
        logger.error(f'Error adding message {str(e)}')
        raise
    
def run_assistant(threadId):
    try:
        run = client.beta.threads.runs.create(
            thread_id=threadId,
            assistant_id=assistant_id,
        )
        return run.id
    except Exception as e:
        print(f'Error running assistant {str(e)}')
        logger.error(f'Error running assistant {str(e)}')
        raise

def check_run_status(threadId, runId):
    try:
        run = client.beta.threads.runs.retrieve(
            thread_id=threadId,
            run_id=runId
        )
        # print(run.usage)
        return run.status
    except Exception as e:
        print(f'Error checking run status {str(e)}')
        logger.error(f'Error checking run status {str(e)}')
        raise
    
def get_thread_messages(threadId):
    try:
        messages = client.beta.threads.messages.list(
            thread_id=threadId
        )
        # print(messages)
        return messages
    except Exception as e:
        print(f'Error getting thread messages {str(e)}')
        logger.error(f'Error getting thread messages {str(e)}')
        raise

# print(create_thread())
# add_message('test message', 'thread_j4b3JCffZYbuFt3vb1Zj0RAT')
# print(run_assistant('thread_j4b3JCffZYbuFt3vb1Zj0RAT'))
# check_run_status('thread_j4b3JCffZYbuFt3vb1Zj0RAT', 'run_pA03itrIt6aIo9gQCkTlpkJK')
# get_thread_messages('thread_j4b3JCffZYbuFt3vb1Zj0RAT')

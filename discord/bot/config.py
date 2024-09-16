import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Reading environment variables
TOKEN = os.getenv('TOKEN')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
PERSIST_DIR = os.getenv('PERSIST_DIR')
DOCSTORE_PATH = os.getenv('DOCSTORE_PATH')
COMMAND_NAME = os.getenv("COMMAND_NAME", 'tomo')

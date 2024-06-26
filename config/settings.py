import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGODB_URI = os.environ.get('MONGODB_URI')
    GOOGLE_SHEETS_CREDENTIALS_FILE = os.environ.get('GOOGLE_SHEETS_CREDENTIALS_FILE')
    GOOGLE_SHEETS_ID = os.environ.get('GOOGLE_SHEETS_ID')
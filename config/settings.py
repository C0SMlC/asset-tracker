import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGODB_URI = os.environ.get('MONGODB_URI')
    GOOGLE_SHEETS_CREDENTIALS_FILE = os.environ.get('GOOGLE_SHEETS_CREDENTIALS_FILE')
    GOOGLE_SHEETS_ID = os.environ.get('GOOGLE_SHEETS_ID')
    GOOGLE_SHEETS_CREDENTIALS = {
        "type": os.environ.get('GOOGLE_TYPE'),
        "project_id": os.environ.get('GOOGLE_PROJECT_ID'),
        "private_key_id": os.environ.get('GOOGLE_PRIVATE_KEY_ID'),
        "private_key": os.environ.get('GOOGLE_PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": os.environ.get('GOOGLE_CLIENT_EMAIL'),
        "client_id": os.environ.get('GOOGLE_CLIENT_ID'),
        "auth_uri": os.environ.get('GOOGLE_AUTH_URI'),
        "token_uri": os.environ.get('GOOGLE_TOKEN_URI'),
        "auth_provider_x509_cert_url": os.environ.get('GOOGLE_AUTH_PROVIDER_CERT_URL'),
        "client_x509_cert_url": os.environ.get('GOOGLE_CLIENT_CERT_URL')
    }
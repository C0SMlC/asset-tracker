import gspread
from google.oauth2.service_account import Credentials
from flask import current_app

def get_google_sheet():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file(
        current_app.config['GOOGLE_SHEETS_CREDENTIALS_FILE'], 
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    return client.open_by_key(current_app.config['GOOGLE_SHEETS_ID']).sheet1
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class gsheets:
    """
    A wrapper that abstracts all the complexity away of communicating with the Google Sheets API.
    Only allows you to retrieve values from a specified spreadsheet.
    """
    def __init__(self):
        self.credentials = self.getCredentials()
        self.sheets = build('sheets', 'v4', credentials=self.credentials).spreadsheets()

    # Authenticate with the Google Sheets API
    def getCredentials(self):
        creds = None
        if os.path.exists('sheetsToken.pickle'):
            with open('sheetsToken.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', ['https://www.googleapis.com/auth/spreadsheets.readonly'])
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('sheetsToken.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    # Gets a range of values from a specific spreadsheet
    def getValues(self, spreadsheetId, cellRange):
        result = self.sheets.values().get(spreadsheetId=spreadsheetId, range=cellRange).execute()
        return result.get('values', [])
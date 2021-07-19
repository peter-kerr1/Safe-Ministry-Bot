import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# https://stackoverflow.com/questions/8953983/do-google-refresh-tokens-expire
# "A Google Cloud Platform project with an OAuth consent screen configured for an external user type and a publishing status of "Testing" is issued a refresh token expiring in 7 days."
# To stop refresh tokens from expiring, you need to submit the app for verification, even if you don't intend on going through with the verification process. Once this is done, the refresh token remains permanent.

class gsheets:
    """
    A wrapper that abstracts all the complexity away of communicating with the Google Sheets API.
    Only allows you to retrieve values from a specified spreadsheet.
    """
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.tokenJson = 'credentials/gsheets_token.json'
        self.credsJson = 'credentials/gsheets_oauth2.json'
        self.credentials = self.getCredentials()
        self.sheets = build('sheets', 'v4', credentials=self.credentials).spreadsheets()

    # Authenticate with the Google Sheets API
    def getCredentials(self):
        creds = None
        if os.path.exists(self.tokenJson):
            creds = Credentials.from_authorized_user_file(self.tokenJson, self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credsJson, self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.tokenJson, 'w') as token:
                token.write(creds.to_json())
        return creds

    # Gets a range of values from a specific spreadsheet
    def getValues(self, spreadsheetId, cellRange):
        result = self.sheets.values().get(spreadsheetId=spreadsheetId, range=cellRange).execute()
        return result.get('values', [])
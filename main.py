from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
from kivy.config import Config
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
APP_SPREADSHEET_ID = '1-bSB1JPLFDz_f0u4DCn-fe5sOfhucD5wF8zHfDJ9whE'


class mybudgetingapp(App):
    Config.set('graphics', 'width', '450')
    Config.set('graphics', 'height', '800')

    def on_press_get_started(self):

        # Google Authentication and Authorizations
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPE)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPE)
                creds = flow.run_local_server(port=0)
            with open("token.json", 'w') as token:
                token.write(creds.to_json())

        # Check if the requisite sheets file present in present in drive
        try:
            service = build("sheets", "v4", credentials=creds)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=APP_SPREADSHEET_ID,
                                        range='Sheet1!A:D').execute()
            self.root.current = 'DashBoard'

        except HttpError as error:
            print(f"An error occurred: {error.error_details}")

            # If not present create one specific google sheets specific to the user
            try:
                spreadsheet = {
                    'properties': {'title': 'MybudgetingApp-Resources'}
                }
                spreadsheet = sheet.create(
                    body=spreadsheet, fields='spreadsheetId').execute()
                print(f'Spreadsheet ID: {spreadsheet.get('spreadsheetId')}')

            except HttpError as error2:
                print(f"An error occurred: {error2.error_details}")
                return None


mybudgetingapp().run()

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

AUTH_FILE = BASE_DIR / "auth.json"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


def get_credentials():

        flow = InstalledAppFlow.from_client_secrets_file(
            AUTH_FILE,
            SCOPES
        )
        return flow.run_local_server(port=0)


class GmailClient:
    def __init__(self, credentials: Credentials):
        self.service = build('gmail', 'v1', credentials=credentials)

    def list_messages(self, user_id='me', max_results=10):
        results = self.service.users().messages().list(userId=user_id, maxResults=max_results).execute()
        return results.get('messages', [])
    def get_unread_messages(self):
        response = self.service.users().messages().list(
            userId="me",
            q="is:unread"
        ).execute()

        return response.get("messages", [])
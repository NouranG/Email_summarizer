from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = Path(__file__).resolve().parents[2]
AUTH_FILE = BASE_DIR / "auth.json"


def get_credentials():
    flow = InstalledAppFlow.from_client_secrets_file(
        AUTH_FILE,
        SCOPES
    )
    return flow.run_local_server(port=0)


class GmailClient:

    def __init__(self, credentials: Credentials):
        self.service = build("gmail", "v1", credentials=credentials)

    def list_unread(self, max_results=10):
        res = self.service.users().messages().list(
            userId="me",
            q="is:unread",
            maxResults=max_results
        ).execute()

        return res.get("messages", [])

    def get_message_raw(self, message_id):
        return self.service.users().messages().get(
            userId="me",
            id=message_id,
            format="raw"
        ).execute()
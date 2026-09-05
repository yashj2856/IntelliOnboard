"""
One-time Google OAuth authorization — run this on your HOST machine
(not inside Docker), once, before switching the app out of simulation mode.

It opens your browser, asks you to sign in with your own Google account and
approve the requested scopes (Drive / Calendar / Gmail / Sheets), then saves
a reusable token to credentials/token.json. The Docker containers mount
that file and use it (refreshing it automatically) — they never need to
open a browser themselves.

Usage:
    python3 authorize_google.py

Prerequisites:
    1. A Google Cloud project with the Drive, Calendar, Gmail, and Sheets
       APIs enabled (all free).
    2. An OAuth 2.0 Client ID of type "Desktop app", downloaded as JSON
       and saved to credentials/oauth_client.json.
    See SETUP_OAUTH.md for the exact click-by-click steps.
"""

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/spreadsheets",
]

CLIENT_SECRET_PATH = os.getenv("GOOGLE_OAUTH_CLIENT_PATH", "credentials/oauth_client.json")
TOKEN_PATH = os.getenv("GOOGLE_TOKEN_PATH_LOCAL", "credentials/token.json")


def main():
    if not os.path.exists(CLIENT_SECRET_PATH):
        raise FileNotFoundError(
            f"'{CLIENT_SECRET_PATH}' not found.\n\n"
            "Download your OAuth Client ID JSON from Google Cloud Console "
            "(APIs & Services > Credentials > Desktop app client) and save "
            f"it as '{CLIENT_SECRET_PATH}'. See SETUP_OAUTH.md."
        )

    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
            # Opens your default browser for the Google consent screen.
            creds = flow.run_local_server(port=0)

        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())

    print(f"\n✅ Authorized. Token saved to '{TOKEN_PATH}'.")
    print("Run `docker compose up --build`, then switch off the 'Simulation Mode' "
          "toggle in the sidebar of http://localhost:8501 to use real Google APIs.")


if __name__ == "__main__":
    main()

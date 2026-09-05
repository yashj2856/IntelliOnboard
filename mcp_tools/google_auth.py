"""
Google authentication — personal OAuth2 (Installed App flow).

This replaces the original domain-wide-delegation Service Account approach,
which requires a Google Workspace domain you administer (not available to
individual/student accounts).

Instead, this authenticates as YOUR OWN Google account (a regular Gmail
account is fine) using the standard "Sign in with Google" OAuth consent
flow. The browser-based consent step happens once, on your HOST machine
(not inside Docker) via `authorize_google.py`, and produces a cached
`token.json` that this module reuses (and silently refreshes) on every
run — including inside the container.
"""

import os
import logging
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/spreadsheets",
]


def get_credentials(scopes: list[str] | None = None) -> Credentials:
    """
    Returns cached user OAuth2 credentials, refreshing the access token
    if it has expired. Raises a clear error if the one-time browser
    authorization hasn't been done yet.
    """
    token_path = os.getenv("GOOGLE_TOKEN_PATH", "/app/credentials/token.json")

    if not os.path.exists(token_path):
        raise FileNotFoundError(
            f"No Google OAuth token found at '{token_path}'.\n"
            "Run `python3 authorize_google.py` on your HOST machine first "
            "(outside Docker) to complete the one-time Google sign-in, "
            "then restart `docker compose up`."
        )

    credentials = Credentials.from_authorized_user_file(token_path, scopes or SCOPES)

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        with open(token_path, "w") as f:
            f.write(credentials.to_json())
        logger.info("Google OAuth access token refreshed.")

    return credentials


def get_drive_service():
    return build("drive", "v3", credentials=get_credentials())


def get_calendar_service():
    return build("calendar", "v3", credentials=get_credentials())


def get_gmail_service():
    return build("gmail", "v1", credentials=get_credentials())


def get_sheets_service():
    return build("sheets", "v4", credentials=get_credentials())

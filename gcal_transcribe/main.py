import datetime
import os.path
import time
from typing import Any, Generator

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CREDENTIALS_FILE = "credentials.json"

# If modifying these scopes, delete the file token.json.
READ_SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
READ_WRITE_SCOPES = ["https://www.googleapis.com/auth/calendar"]


def connect(scopes: list[str], name: str, token_file: str) -> Credentials:
    """
    Gets Credentials for the given scopes and saves to a JSON file for later.
    If the given token_file exists, attempts to use that token and will refresh
    the token if it is expired. Saves the token to token_file.
    """
    creds = None

    # The file token_file stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        input(f"Requesting a token for the {name} account. Enter to continue:")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    assert creds is not None
    return creds


def get_all_events(creds: Credentials, page_size: int = 100, sleep_time: int = 0.5, limit: int | None = None) -> Generator[dict[str, Any], None, None]:
    service = build("calendar", "v3", credentials=creds)

    sentinel_token = ""
    page_token = None
    while page_token != sentinel_token:
        events_result = (
            service.events()
            .list(
                calendarId='primary',
                maxResults=page_size,
                pageToken=page_token,
            )
            .execute()
        )

        events = events_result.get("items", [])

        for event in events:
            # Check if we have exceeded limit
            if limit is not None:
                if limit == 0:
                    return # Exit out of this function
                else:
                    limit -= 1

            yield event

        page_token = events_result.get("nextPageToken", sentinel_token)
        time.sleep(sleep_time)


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    src_creds = connect(READ_SCOPES, "SOURCE", "src_token.json")
    dest_creds = connect(READ_WRITE_SCOPES, "DESTINATION", "dest_token.json")

    events = get_all_events(src_creds, limit=5)
    for event in events:
        print(event)


if __name__ == "__main__":
    main()

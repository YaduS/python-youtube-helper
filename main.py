# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from time import sleep

from dotenv import load_dotenv

load_dotenv()

CLIENT_SECRETS_FILE = os.getenv("CLIENT_SECRET_FILE")
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
PLAYLIST_ID = os.getenv("PLAYLIST_ID")
CREDENTIALS_FILE = "token.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
API_SUBSEQUENT_CALL_DELAY = 5  # seconds
MAX_COUNT = 2


def init_youtube_client():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    credentials = None
    # Check if the credentials file already exists
    if os.path.exists(CREDENTIALS_FILE):
        credentials = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)

    # If there are no valid credentials, request authorization
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            # Get credentials and create an API client
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            credentials = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open(CREDENTIALS_FILE, "w") as token:
            token.write(credentials.to_json())

    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, credentials=credentials)

    return youtube


def get_playlist_data(youtube, nextPageToken=None):
    request = youtube.playlistItems().list(
        part="snippet,contentDetails", playlistId=PLAYLIST_ID, pageToken=nextPageToken
    )
    response = request.execute()
    return response


def main():
    global MAX_COUNT

    # counter added as a fallback to nextPageToken
    counter = 0
    nextPageToken = None
    youtube = init_youtube_client()

    while counter < MAX_COUNT:

        response = get_playlist_data(youtube, nextPageToken)
        nextPageToken = (
            response["nextPageToken"] if "nextPageToken" in response else None
        )

        print(response)
        print("\n=====================================================================")
        print(f"nextPageToken:  {nextPageToken}, \n page no: + {counter + 1}")
        print("=====================================================================\n")

        if nextPageToken == None:
            break

        sleep(API_SUBSEQUENT_CALL_DELAY)

        counter += 1


if __name__ == "__main__":
    main()

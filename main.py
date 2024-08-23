# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from time import sleep

from dotenv import load_dotenv

load_dotenv()

CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE")
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
PLAYLIST_ID = os.getenv("PLAYLIST_ID")

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
API_SUBSEQUENT_CALL_DELAY = 5  # seconds
MAX_COUNT = 2


def init_youtube_variables():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"

    client_secrets_file = CLIENT_SECRET_FILE
    # Get credentials and create an API client
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)

    # credentials = flow.run_console()
    """
    run_console command kept failing since that function was no longer supported; after digging around trying to fix the versions in which this was supported,
    found that google shows error in browser even after getting it to work with older versions.

    with some help from chatGPT was able to figure out that flow using run_console is no longer supported, and we should instead use run_local_server,
    which worked and was able to display channel details in console
    """
    credentials = flow.run_local_server(port=0)
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

    youtube = init_youtube_variables()
    while counter < MAX_COUNT and nextPageToken != None:

        response = get_playlist_data(youtube, nextPageToken)
        nextPageToken = (
            response["nextPageToken"] if "nextPageToken" in response else None
        )

        print(response)
        print("\n=====================================================================")
        print("nextPageToken: " + str(nextPageToken))
        print("=====================================================================\n")
        sleep(API_SUBSEQUENT_CALL_DELAY)
        counter += 1


if __name__ == "__main__":
    main()

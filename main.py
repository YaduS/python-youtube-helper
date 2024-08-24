# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json

from time import sleep
from dotenv import load_dotenv

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


load_dotenv()

CLIENT_SECRETS_FILE = os.getenv("CLIENT_SECRET_FILE")
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
PLAYLIST_ID = os.getenv("PLAYLIST_ID")
CREDENTIALS_FILE = "token.json"
PLAYLIST_DATA_OUTPUT_JSON = "playlist_items.json"

# SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
API_SUBSEQUENT_CALL_DELAY = 5  # seconds
MAX_COUNT = 15


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


def write_playlist_data(playlistItems):
    with open(PLAYLIST_DATA_OUTPUT_JSON, "w") as json_file:
        json.dump(playlistItems, json_file, indent=2)


# def update_video_details(youtube):
def update_video_details(youtube, details: dict, uploadVideoId):
    # print(details, uploadVideoId)
    request = youtube.videos().update(
        part="snippet, status",
        body={
            "id": uploadVideoId,
            "snippet": {
                "title": details["title"],
                "categoryId": "20",
                "description": details["description"],
            },
            "status": {"selfDeclaredMadeForKids": False},
        },
    )
    request.execute()


PLAYLIST_DATA_INPUT_JSON = os.getenv("PLAYLIST_DATA_INPUT_JSON")
PLAYLIST_UPLOAD_VIDEOS_JSON = os.getenv("PLAYLIST_UPLOAD_VIDEOS_JSON")


def update_from_playlist_data(youtube):
    with open(PLAYLIST_UPLOAD_VIDEOS_JSON, "r") as upload_videos_file:
        upload_videos_data = json.load(upload_videos_file)
        with open(PLAYLIST_DATA_INPUT_JSON, "r") as json_file:
            playlist_data = json.load(json_file)
            for index, item in enumerate(playlist_data):
                videoDetails = {
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                }
                videoId = upload_videos_data[index]["videoId"]
                update_video_details(youtube, videoDetails, videoId)
                print(
                    f"================================\n Updated {videoId}; with title {videoDetails['title']}"
                )
                sleep(API_SUBSEQUENT_CALL_DELAY)


def main():

    youtube = init_youtube_client()

    # NOTE: USE ONLY ONE OF THE BELOW SECTIONS AT A TIME. COMMENT OUT THE OTHER SECTIONS

    # ========================== GET DATA FROM PLAYLIST ===========================#

    # counter added as a fallback to nextPageToken
    counter = 0
    nextPageToken = None
    playlistItems = []

    while counter < MAX_COUNT:
        response = get_playlist_data(youtube, nextPageToken)
        nextPageToken = (
            response["nextPageToken"] if "nextPageToken" in response else None
        )
        playlistItems += response["items"]
        print(f"===================================\n fetched page: {counter + 1}")
        if nextPageToken == None:
            break
        counter += 1
        sleep(API_SUBSEQUENT_CALL_DELAY)

    write_playlist_data(playlistItems)
    # ================================SECTION END==================================#

    # ============UPDATE VIDEO DETAILS FROM JSON FILE(PLAYLIST DATA)===============#
    update_from_playlist_data(youtube)
    # ================================SECTION END==================================#


if __name__ == "__main__":
    main()

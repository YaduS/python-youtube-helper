# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from dotenv import load_dotenv

load_dotenv()

CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET_FILE')
API_KEY = os.getenv('API_KEY')
CHANNEL_ID = os.getenv('CHANNEL_ID')


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = CLIENT_SECRET_FILE

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    
    # credentials = flow.run_console()
    '''
    run_console command kept failing since that function was no longer supported; after digging around trying to fix the versions in which this was supported,
    found that google shows error in browser even after getting it to work with older versions.

    with some help from chatGPT was able to figure out that flow using run_console is no longer supported, and we should instead use run_local_server, 
    which worked and was able to display channel details in console
    '''
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-

# Sample Python code for youtube.activities.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

from dotenv import load_dotenv
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.api_key import Credentials

scopes = ["https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly"]

load_dotenv()
youtube_api_key = os.environ['YOUTUBE_API_KEY']


def get_playlist_id(channel):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    # client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #     client_secrets_file, scopes)
    # credentials = flow.run_console()
    credentials = Credentials(youtube_api_key)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.channels().list(
        forHandle=channel, part='contentDetails')
    response = request.execute()
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return playlist_id


if __name__ == "__main__":
    get_playlist_id('BplusPodcast')

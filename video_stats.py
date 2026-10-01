from datetime import date
import json

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


def get_youtube_session(api_version="v3"):
    api_service_name = "youtube"
    # client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
    # Get credentials and create an API client
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #     client_secrets_file, scopes)
    # credentials = flow.run_console()
    credentials = Credentials(youtube_api_key)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube


def get_playlist_id(channel_handle, session):
    request = session.channels().list(
        forHandle=channel_handle, part='contentDetails')
    response = request.execute()
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return playlist_id


def get_video_ids(playlist_id,  session, max_results: None | int = 5):
    video_ids = []
    next_page_token = ''
    prev_page_token = None
    max_results_per_page = 50
    max_results = 1000000 if max_results is None else max_results
    while (next_page_token is not None) and (len(video_ids) < max_results):
        request = session.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            pageToken=prev_page_token,
            maxResults=50
        )
        response = request.execute()
        next_page_token = response.get('nextPageToken')
        prev_page_token = next_page_token
        for video in response['items']:
            v_id = video['contentDetails']['videoId']
            video_ids.append(v_id)
            if len(video_ids) >= max_results:
                break
    return video_ids


def get_video_stats(video_ids, session):
    video_stats = []
    max_results = 50
    batch = 0
    while batch * max_results < len(video_ids):
        parsed_ids = ','.join(
            video_ids[batch*max_results:(batch+1) * max_results])
        batch += 1
        request = session.videos().list(
            part='snippet,contentDetails,statistics',
            maxResults=max_results,
            id=parsed_ids
        )
        response = request.execute()
        for item in response['items']:
            snippet = item['snippet']
            content_details = item['contentDetails']
            statistics = item['statistics']
            video_item_stats = {
                'id': item['id'],
                'title': snippet['title'],
                'publishedAt': snippet.get('publishedAt'),
                'duration': content_details.get('duration'),
                'viewCount': statistics.get('viewCount'),
                'likeCount': statistics.get('likeCount'),
                'commentCount': statistics.get('commentCount'),
            }
            video_stats.append(video_item_stats)

    return video_stats


def save_to_json(data):
    file_path = f"./data/YT_data_{date.today()}.json"

    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    session = get_youtube_session()
    playlist_id = get_playlist_id('MrBeast', session=session)
    video_ids = get_video_ids(playlist_id, session, None)
    video_stats = get_video_stats(video_ids, session)
    save_to_json(video_stats)

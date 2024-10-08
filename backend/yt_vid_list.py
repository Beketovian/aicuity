import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_top_videos(query, max_results=10):
    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    search_response = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    ).execute()

    videos = []

    for item in search_response.get('items', []):
        video_id = item['id']['videoId']
        videos.append(video_id)

    return videos

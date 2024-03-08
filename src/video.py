from googleapiclient import channel
from googleapiclient.discovery import build
from dotenv import load_dotenv

import os
import json
from pprint import pprint

load_dotenv()



class Video:

    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=video_id).execute()
        self.title: str = self.video_response['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/{self.video_id}"
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']


    def __str__(self) -> str:
        return self.title if self.title else self.video_id


class PLVideo:
    """Класс инициализируется  'id видео' и 'id плейлиста'"""
    def __init__(self, video_id: str, playlist_id: str) -> None:
        self.video_id = video_id
        self.playlist_id = playlist_id

    def __str__(self) -> str:
        return 'MoscowPython Meetup 78 - вступление'

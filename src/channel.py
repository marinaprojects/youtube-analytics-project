from pprint import pprint
from googleapiclient.discovery import build
from dotenv import load_dotenv
from settings import FILE_NAME
from helper.youtube_api_manual import channel

import os
import json

load_dotenv(FILE_NAME)
load_dotenv()
moscowpython_list = []


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.channel_name = channel['items'][0]['snippet']['title']
        self.channel_desc = channel['items'][0]['snippet']['description']
        self.channel_link = f'https://www.youtube.com/channel/{channel["items"][0]["id"]}'
        self.channel_sub_count = channel['items'][0]['statistics']['subscriberCount']
        self.channel_video_count = channel['items'][0]['statistics']['videoCount']
        self.channel_view_count = channel['items'][0]['statistics']['viewCount']
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        self.channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        pprint(channel)

    def to_json(self, file_name: str):
        data = json.dumps(self, channel)
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(data)


    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return f'{self.channel["items"][0]["snippet"]["title"]}'

    @property
    def view_count(self):
        return f'{moscowpython_list["items"][0]["statistics"]["viewCount"]}'

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube
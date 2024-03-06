from googleapiclient import channel
from googleapiclient.discovery import build
from dotenv import load_dotenv

import os
import json
from pprint import pprint

load_dotenv()

class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        #self.sub_count = int(self.channel_id['items'][0]['statistics']['subscriberCount'])
        self.channel_data = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.video_count = self.channel_data['items'][0]['statistics']['viewCount']
        self.url = f'https://www.youtube.com/channel/{self.channel_data["items"][0]["id"]}'


    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, value):
        self.__channel_id = value


    @property
    def channel(self):
        return self.channel_data

    @property
    def title(self):
        return self.channel_data['items'][0]['snippet']['title']

    @property
    def video_count(self):
        return self.channel_data['items'][0]['statistics']['viewCount']

    @video_count.setter
    def video_count(self, value):
        self._video_count = value

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        pprint(self.channel_data)

    def to_json(self, file_name: str):
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(self.channel_data, file)


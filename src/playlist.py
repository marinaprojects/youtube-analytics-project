import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import datetime


load_dotenv()


class PlayList:
    """класс для плейлиста"""
    api_key: str = os.getenv('YT_API_KEY')
    """специальный объект для работы с API"""
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        # Здесь должна быть логика для получения данных о плейлисте, таких как название и ссылка
        self.url = f"https://www.youtube.com/playlist?list=" + self.playlist_id
        self.playlist_data: dict = None
        self.video_response: dict = None
        self.title = None
        #self.title: str = self.playlist_data()['items'][0]['snippet']['title']
        # получить все id видеороликов из плейлиста
        self.video_ids = []



    def playlist_response(self) -> None:
        """если информации в словаре нет, возвращает информацию о плейлисте"""
        if self.playlist_data is None:
            self.playlist_data = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       playlist_dataid=self.playlist_data).execute()
            return self.playlist_data


    @property
    def total_duration(self) -> datetime.timedelta:
        """Возвращает суммарную длительность плейлиста"""
        total_duration = datetime.timedelta()
        for video_id in self.video_ids:
            video_info = self.fetch_video_info(video_id)
            if 'items' in video_info and len(video_info['items']) > 0:
                duration = int(video_info['items'][0]['contentDetails']['duration'])
                total_duration += datetime.timedelta(seconds=duration)
        return total_duration

    def video_response(self) -> None:
        """если информации в словаре нет возвращает информацию о плейлисте"""
        if self.video_response is None:
            self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                             id=','.join(self.video_ids)).execute()
            return self.playlist_data

    def show_best_video(self) -> str:
        """показывает видео с наибольшим количеством лайков из плейлиста"""
        best_video_id = None
        max_likes = 0
        for video_id in self.video_ids:
            video_info = self.youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()
            if 'items' in video_info and len(video_info['items']) > 0:
                like_count = int(video_info['items'][0]['statistics']['likeCount'])
                if like_count > max_likes:
                    max_likes = like_count
                    best_video_id = video_id
        if best_video_id:
            return f"https://youtu.be/{best_video_id}"
        else:
            return "No videos found in the playlist"

    """показывает видео с наибольшим количеством лайков из плейлиста"""

    def most_viewed_video(self) -> str:
        more_viewed: int = 0
        for video in self.video_response()['items']:
            view_count: int = video['statistics']['viewCount']
            video_id = video['id']
            if int(view_count) > int(more_viewed):
                more_viewed = view_count
                self.right_id = video_id
        return "https://youtu.be/{self.right_id}"


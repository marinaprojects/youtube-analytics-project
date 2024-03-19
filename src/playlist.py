import os
import datetime
import isodate  # Для разбора ISO 8601 длительности

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class PlayList:
    """класс для плейлиста"""
    api_key: str = os.getenv('YT_API_KEY')
    """специальный объект для работы с API"""
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str):
        self.right_id = None
        self.playlist_id = playlist_id
        # Здесь должна быть логика для получения данных о плейлисте, таких, как название и ссылка
        self.url = f"https://www.youtube.com/playlist?list=" + self.playlist_id
        self.playlist_data = None
        self.video_response = None
        self.title = None
        # получить все id видеороликов из плейлиста
        self.video_ids = []
        # Вызов метода для заполнения информации о плейлисте
        self.fetch_playlist_info()

    def fetch_playlist_info(self):
        """Получить информацию о плейлисте"""
        if self.playlist_data is None:
            self.playlist_data = self.youtube.playlists().list(part='snippet', id=self.playlist_id).execute()
            if 'items' in self.playlist_data and len(self.playlist_data['items']) > 0:
                self.title = self.playlist_data['items'][0]['snippet']['title']
                self.video_ids = self.get_video_ids()

    def get_video_ids(self):
        """Получить id видеороликов из плейлиста"""
        video_ids = []
        playlist_items = self.youtube.playlistItems().list(part="contentDetails", playlistId=self.playlist_id,
                                                           maxResults=50).execute()
        while playlist_items:
            for item in playlist_items["items"]:
                video_ids.append(item["contentDetails"]["videoId"])
            playlist_items = self.youtube.playlistItems().list_next(playlist_items, playlist_items)
        return video_ids

    def fetch_video_info(self, video_id: str) -> dict:
        """Получает информацию о видео по его идентификатору"""
        video_info = self.youtube.videos().list(
            part='contentDetails',
            id=video_id
        ).execute()
        return video_info

    def video_response(self) -> None:
        """Возвращает информацию о видео в плейлисте"""
        if self.video_response is None:
            self.video_response = self.youtube.videos().list(part='contentDetails', id=','.join(self.video_ids)).execute()
        return self.video_response

    def show_best_video(self) -> str:
        """Показывает видео с наибольшим количеством лайков из плейлиста"""
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

    def most_viewed_video(self) -> str:
        """Возвращает ссылку на видео с наибольшим количеством просмотров"""
        more_viewed = 0
        for video in self.video_response()['items']:
            view_count = int(video['statistics']['viewCount'])
            video_id = video['id']
            if view_count > more_viewed:
                more_viewed = view_count
                self.right_id = video_id
        return f"https://youtu.be/{self.right_id}"

    @property
    def total_duration(self) -> datetime.timedelta:
        """Возвращает суммарную длительность плейлиста"""
        total_duration = datetime.timedelta()
        for video_id in self.video_ids:
            video_info = self.fetch_video_info(video_id)
            if 'items' in video_info and len(video_info['items']) > 0:
                duration = isodate.parse_duration(video_info['items'][0]['contentDetails']['duration'])
                total_duration += duration
        return total_duration
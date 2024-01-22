from scrapper import Scrapper
import os
from googleapiclient.discovery import build
from pytube import YouTube
import configparser
import pathlib
from dataset_to_parse import youtube_channel_ids
from aws import push_stream_to_s3

config_path = pathlib.Path(__file__).parent.absolute() / "config.ini"
config = configparser.ConfigParser()
config.read(config_path)
API_KEY = config["YoutubeAPI"]["API_KEY"]
BUCKET_NAME = config["AppConfig"]["BUCKET_NAME"]


class YoutubeScrapper(Scrapper):
    def __init__(self, channel_id: str):
        Scrapper.__init__(
            self,
            "youtube",
            channel_id,
        )

    def scrap(self, max_results: int = 50):
        video_ids = YoutubeScrapper.get_youtube_video_list(self.user_id, max_results)
        for video_id in video_ids:
            audio = YoutubeScrapper.get_audio(video_id)
            success = push_stream_to_s3(audio, BUCKET_NAME, self.user_id)
            if success is not None:
                print(f"Logged s3 push: {video_id}")
            else:
                print(f"Logged s3 push faliure: {video_id}")

    @staticmethod
    def get_youtube_video_list(channel_id, max_count=50):
        youtube = build("youtube", "v3", developerKey=API_KEY)

        # Get the list of all uploaded videos from the channel
        videos = []
        next_page_token = None

        while True:
            search_response = (
                youtube.search()
                .list(
                    part="id",
                    channelId=channel_id,
                    type="video",
                    maxResults=50,
                    pageToken=next_page_token,
                    order="viewCount",
                )
                .execute()
            )

            video_ids = [item["id"]["videoId"] for item in search_response["items"]]

            next_page_token = search_response.get("nextPageToken")

            if not next_page_token or (
                max_count is not None and len(video_ids) >= max_count
            ):
                break

        return video_ids

    @staticmethod
    def get_audio(video_id: str) -> bool:
        youtube_url = f'https://www.youtube.com/watch?v={video_id}"'
        try:
            video = YouTube(youtube_url)
            audio = video.streams.filter(only_audio=True).first()
            if audio.filesize_mb >3:
                return audio
            return None
        except Exception as err:
            print(repr(err))
            return None


for video_id in youtube_channel_ids.values():
    youtube_scrapper = YoutubeScrapper(video_id)
    youtube_scrapper.scrap(10)

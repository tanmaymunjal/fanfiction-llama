from scrapper import Scrapper
import os
from googleapiclient.discovery import build
from pytube import YouTube
import configparser
import pathlib
from dataset_to_parse import youtube_channel_ids

config_path = pathlib.Path(__file__).parent.absolute() / "config.ini"
config = configparser.ConfigParser()
config.read(config_path)
API_KEY = config["YoutubeAPI"]["API_KEY"]


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
            YoutubeScrapper.get_audio(video_id,output_path=f"../audios/{self.user_id}")

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
                    order = "viewCount"
                )
                .execute()
            )

            video_ids = [item["id"]["videoId"] for item in search_response["items"]]

            videos_response = (
                youtube.videos().list(part="snippet", id=",".join(video_ids)).execute()
            )

            for video in videos_response["items"]:
                videos.append(video["id"])

                # Break the loop if the maximum count is reached
                if max_count is not None and len(videos) >= max_count:
                    break

            next_page_token = search_response.get("nextPageToken")

            if not next_page_token or (
                max_count is not None and len(videos) >= max_count
            ):
                break

        return videos

    @staticmethod
    def get_audio(
        video_id: str, audio_extension: str = "mp3", output_path="../audios"
    ) -> bool:
        print("wOW")
        youtube_url = f'https://www.youtube.com/watch?v={video_id}"'
        try:
            video = YouTube(youtube_url)
            audio = video.streams.filter(only_audio=True, file_extension="mp3").first()
            audio.download(output_path=output_path)
            return True
        except Exception as err:
            print(repr(err))
            return False


for value in youtube_channel_ids.values():
    youtube = YoutubeScrapper(value)
    youtube.scrap(100)

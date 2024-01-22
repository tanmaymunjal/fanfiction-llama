import boto3
from io import BytesIO
from pytube import YouTube
import pathlib
import configparser
import urllib.parse

config_path = pathlib.Path(__file__).parent.absolute() / "config.ini"
config = configparser.ConfigParser()
config.read(config_path)
aws_access_key = config["AWS"]["API_KEY"]
aws_secret_key = config["AWS"]["SECRET_API_KEY"]

# Create an S3 clie/nt
s3 = boto3.client(
    "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
)

def make_uri_safe(filename):
    # Replace special characters with URL-encoded equivalents
    uri_safe_filename = urllib.parse.quote(filename)

    return uri_safe_filename

def push_stream_to_s3(pytube_stream, bucket_name, video_id):
    if pytube_stream is None:
        return None

    video_content = BytesIO()
    pytube_stream.stream_to_buffer(video_content)

    # Reset the BytesIO object's position to the beginning
    video_content.seek(0)

    # Upload the video stream content directly to S3
    try:
        s3.upload_fileobj(
            video_content, bucket_name, f"{video_id}/{make_uri_safe(pytube_stream.title)}.mp3"
        )
        return True
    except Exception as e:
        print(repr(e))
        return False

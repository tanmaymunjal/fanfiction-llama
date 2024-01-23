import boto3
import librosa
import configparser
import pathlib
import io
import os

config_path = pathlib.Path(__file__).parent.absolute() / "config.ini"
config = configparser.ConfigParser()
config.read(config_path)
aws_access_key = config["S3"]["ACCESS_KEY"]
aws_secret_key = config["S3"]["SECRET_ACCESS_KEY"]
local_folder = "Audios/"
# Save binary data to local files
if not os.path.exists(local_folder):
    os.makedirs(local_folder)


data = []
s3 = boto3.client(
    "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
)
# Paginator for listing objects
paginator = s3.get_paginator("list_objects_v2")
pages = paginator.paginate(Bucket="financialcontenthindi-raw")
i = 0
# List objects in the specified prefix (folder)
for page in pages:
    # Iterate through each object in the page
    for obj in page.get("Contents", []):
        # Check if the object is a file with the .mp3 extension
        if obj["Key"].endswith(".mp3"):
            # Download the binary content of the MP3 file
            response = s3.get_object(Bucket="financialcontenthindi-raw", Key=obj["Key"])["Body"].read()
            local_file_path = os.path.join(local_folder, str(i))+".mp4"
            i+=1
            if i==10:
                break
            with open(local_file_path, 'wb+') as local_file:
                local_file.write(response)
            audio_data, _ = librosa.load(local_file_path)
            data.append([audio_data,obj["Key"]])

def delete_local_files(local_folder):
    # Delete local files
    for file_name in os.listdir(local_folder):
        file_path = os.path.join(local_folder, file_name)
        os.remove(file_path)
        print(f"Deleted: {file_path}")


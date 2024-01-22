import boto3
import librosa

data = []
s3 = boto3.resource("s3")
bucket = s3.Bucket("financialcontenthindi-raw")
for file in bucket.objects.filter(Prefix="/*/*.mp3"):
    print("Horray!")

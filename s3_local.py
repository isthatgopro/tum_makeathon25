import os

import boto3
from dotenv import load_dotenv

# Load variables from .evn file
load_dotenv()

# Load access keys
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

bucket_name = "tumai.makeathon2025"
# Make sure you set your group name correctly! e.g. "Group42/", "Group03/"
prefix = "GroupXX/"

# Instantiate the boto3 client
s3 = boto3.client(
    service_name="s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="eu-central-1",
)

# Construct unique S3 key (file path in the bucket)
remote_file_name = "welcome.md"
s3_key = prefix + remote_file_name

# Download a file and store it locally
local_file_name = "downloaded_welcome.md"
s3.download_file(Filename=local_file_name, Bucket=bucket_name, Key=s3_key)
print(
    f"Downloaded 's3://{bucket_name}/{s3_key}' and stored file in '{local_file_name}'"
)

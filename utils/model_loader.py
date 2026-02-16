import boto3
import os

BUCKET_NAME = "urbanbot-storage"

s3 = boto3.client("s3")


def ensure_model(local_path, s3_key):
    """
    Download model from S3 if not present locally
    local_path → where model should exist
    s3_key → path inside S3 bucket
    """

    if os.path.exists(local_path):
        print(f"Model exists: {local_path}")
        return

    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    print(f"Downloading from S3: {s3_key}")

    s3.download_file(
        BUCKET_NAME,
        s3_key,
        local_path
    )

    print("Download complete")

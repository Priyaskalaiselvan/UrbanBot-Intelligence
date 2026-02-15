import boto3
import os
from uuid import uuid4

s3 = boto3.client("s3")

BUCKET_NAME = "urbanbot-storage"

def upload_image_to_s3(local_path, category):
    """
    category: traffic / accident / crowd / road_damage
    """
    ext = os.path.splitext(local_path)[1]
    image_name = f"{uuid4()}{ext}"

    s3_key = f"detected-images/{category}/{image_name}"

    s3.upload_file(
        Filename=local_path,
        Bucket=BUCKET_NAME,
        Key=s3_key
    )

    s3_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
    return s3_url

import boto3
from django.conf import settings


def get_lambda_client():
    return boto3.client(
        "lambda",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

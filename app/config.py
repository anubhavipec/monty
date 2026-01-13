import os

class Settings:
    # LocalStack always runs on 4566
    AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
    AWS_REGION = "us-east-1"
    
    # S3 and DynamoDB Names
    BUCKET_NAME = "user-images"
    TABLE_NAME = "ImageMetadata"
    
    # AWS Fake Credentials for LocalStack
    AWS_ACCESS_KEY_ID = "test"
    AWS_SECRET_ACCESS_KEY = "test"

settings = Settings()
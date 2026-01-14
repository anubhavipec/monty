import boto3
import uuid
from app.config import settings
from botocore.exceptions import ClientError

# Resource/Client initialization
s3 = boto3.client(
    "s3", 
    endpoint_url=settings.AWS_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

dynamodb = boto3.resource(
    "dynamodb", 
    endpoint_url=settings.AWS_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)
table = dynamodb.Table(settings.TABLE_NAME)

class ImageService:
    @staticmethod
    def upload_image(file_obj, filename, user_id, category):
        image_id = str(uuid.uuid4())
        s3_key = f"uploads/{user_id}/{image_id}_{filename}"
        
        # 1. Stream file directly to S3
        s3.upload_fileobj(file_obj, settings.BUCKET_NAME, s3_key)
    
        # 2. Save Metadata to DynamoDB
        metadata = {
            "image_id": image_id,
            "s3_key": s3_key,
            "user_id": user_id,
            "category": category,
            "filename": filename
        }
        table.put_item(Item=metadata)
        return metadata

    @staticmethod
    def list_images(filter_key=None, filter_value=None):
        if filter_key and filter_value:
            # Using Attr to filter results
            response = table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr(filter_key).eq(filter_value)
            )
        else:
            response = table.scan()
        return response.get("Items", [])

    @staticmethod
    def get_presigned_url(image_id):
        item = table.get_item(Key={"image_id": image_id}).get("Item")
        if not item:
            return None
        
        return s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.BUCKET_NAME, 'Key': item['s3_key']},
            ExpiresIn=3600
        )

    @staticmethod
    def delete_image(image_id):
        item = table.get_item(Key={"image_id": image_id}).get("Item")
        if not item:
            return False
        
        s3.delete_object(Bucket=settings.BUCKET_NAME, Key=item["s3_key"])
        table.delete_item(Key={"image_id": image_id})
        return True
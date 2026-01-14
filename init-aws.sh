#!/bin/bash
echo "Creating S3 Bucket..."
awslocal s3 mb s3://user-images
echo "Creating DynamoDB Table..."
awslocal dynamodb create-table \
    --table-name ImageMetadata \
    --attribute-definitions AttributeName=image_id,AttributeType=S \
    --key-schema AttributeName=image_id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

echo "Infrastructure provisioned successfully!"
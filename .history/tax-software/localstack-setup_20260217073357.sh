#!/bin/bash
# LocalStack setup script for S3 + Lambda demo
# Prerequisites: LocalStack running, awslocal (from localstack-client) installed, Python Lambda zip built
set -e

# Create S3 buckets
awslocal s3 mb s3://localstack-source-bucket
awslocal s3 mb s3://localstack-destination-bucket

# Package and deploy ProcessTaxReturn Lambda
pip install -r requirements.txt -t package/
cp backend/app/handler.py package/
cd package && zip -r ../process-tax-return.zip . && cd ..
awslocal s3 cp process-tax-return.zip s3://localstack-source-bucket/process-tax-return.zip
awslocal lambda create-function \
  --function-name ProcessTaxReturn \
  --runtime python3.11 \
  --handler handler.lambda_handler \
  --role arn:aws:iam::000000000000:role/lambda-ex \
  --code S3Bucket=localstack-source-bucket,S3Key=process-tax-return.zip \
  --environment Variables={BUCKET=localstack-source-bucket}

# Package and deploy GenerateReport Lambda
cp backend/app/report.py package/
cd package && zip -r ../generate-report.zip . && cd ..
awslocal s3 cp generate-report.zip s3://localstack-destination-bucket/generate-report.zip
awslocal lambda create-function \
  --function-name GenerateReport \
  --runtime python3.11 \
  --handler report.lambda_handler \
  --role arn:aws:iam::000000000000:role/lambda-ex \
  --code S3Bucket=localstack-destination-bucket,S3Key=generate-report.zip \
  --environment Variables={BUCKET=localstack-destination-bucket}

echo "LocalStack S3 buckets and Lambda functions provisioned."

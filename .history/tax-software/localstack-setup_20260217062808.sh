#!/bin/bash
# LocalStack setup script for S3 + Lambda image resizer demo
# Prerequisites: LocalStack running, awslocal installed, Python Lambda zip built

set -e


# Create S3 buckets
awslocal s3 mb s3://localstack-source-bucket
awslocal s3 mb s3://localstack-destination-bucket

# Package and deploy ProcessTaxReturn Lambda
pip install -r requirements.txt -t package/
cp handler.py package/
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
cp report.py package/
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

# Add S3 event notification to trigger Lambda on .jpeg upload
awslocal s3api put-bucket-notification-configuration \
  --bucket $SOURCE_BUCKET \
  --notification-configuration '{
    "LambdaFunctionConfigurations": [
      {
        "LambdaFunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:'$LAMBDA_NAME'",
        "Events": ["s3:ObjectCreated:*"],
        "Filter": {"Key": {"FilterRules": [{"Name": "suffix", "Value": ".jpeg"}]}}
      }
    ]
  }'

# Grant S3 permission to invoke Lambda (LocalStack auto-permits, but for AWS parity)
awslocal lambda add-permission \
  --function-name $LAMBDA_NAME \
  --statement-id s3invoke \
  --action "lambda:InvokeFunction" \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::$SOURCE_BUCKET

echo "LocalStack S3 + Lambda setup complete."

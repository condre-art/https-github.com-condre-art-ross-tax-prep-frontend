#!/bin/bash
# setup.sh - Provision and wire up S3 and Lambda for LocalStack emulation
# Prerequisites: LocalStack running, awslocal installed, Lambda zip ready

set -e

SOURCE_BUCKET=localstack-source-bucket
DEST_BUCKET=localstack-destination-bucket
LAMBDA_NAME=ResizerFunction
LAMBDA_ROLE_ARN=arn:aws:iam::000000000000:role/lambda-role
LAMBDA_HANDLER=app.lambda_handler
LAMBDA_RUNTIME=python3.14
LAMBDA_ZIP=your-lambda.zip  # Update with your actual zip file

# Create S3 buckets
awslocal s3 mb s3://$SOURCE_BUCKET || true
awslocal s3 mb s3://$DEST_BUCKET || true

# Upload Lambda code to S3
awslocal s3 cp $LAMBDA_ZIP s3://$SOURCE_BUCKET/$LAMBDA_ZIP

# Create Lambda function
awslocal lambda create-function \
  --function-name $LAMBDA_NAME \
  --runtime $LAMBDA_RUNTIME \
  --handler $LAMBDA_HANDLER \
  --role $LAMBDA_ROLE_ARN \
  --code S3Bucket=$SOURCE_BUCKET,S3Key=$LAMBDA_ZIP \
  --environment Variables={DESTINATION_BUCKETNAME=$DEST_BUCKET} || true

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
  --source-arn arn:aws:s3:::$SOURCE_BUCKET || true

echo "LocalStack S3 + Lambda setup complete."

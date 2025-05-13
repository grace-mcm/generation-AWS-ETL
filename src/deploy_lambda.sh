#!/bin/bash

# This script creates a proper Lambda deployment package with the handler at the root

# Create a temporary directory for packaging
#echo "Creating Lambda deployment package..."
#mkdir -p lambda_package
#
## Copy the Lambda handler and dependencies to the package directory
#cp raw_data_etl_lambda.py etl_transform.py lambda_package/
#cp -r utils lambda_package/
#
## Install Python dependencies in the package directory
#echo "Installing dependencies..."
#cd lambda_package && pip install --platform manylinux2014_x86_64 \
#    --implementation cp --python-version 3.12 \
#    --only-binary=:all: --upgrade -r ../requirements-lambda.txt --target .
#
## Create the zip file
#echo "Creating zip file..."
#zip -r ../lambda_code.zip .
#cd ..

# Upload to S3 (uncomment and modify with your bucket name and profile)
echo "Uploading to S3..."
# Replace YOUR_BUCKET_NAME and YOUR_PROFILE with your actual values
aws s3 cp lambda_code.zip s3://roast-me-raw-deployment-bucket/lambda_code.zip --profile de-course

# Update the Lambda function (uncomment and modify with your function name and profile)
echo "Updating Lambda function..."
# Replace YOUR_FUNCTION_NAME and YOUR_PROFILE with your actual values
# aws lambda update-function-code \
#   --function-name YOUR_FUNCTION_NAME \
#   --s3-bucket roast-me-raw-deployment-bucket \
#   --s3-key lambda_code.zip \
#   --profile YOUR_PROFILE

echo "Done!"

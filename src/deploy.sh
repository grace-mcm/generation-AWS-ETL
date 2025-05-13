#!/bin/sh

###
### Script to deploy S3 bucket + lambda in cloudformation stack
###

#### CONFIGURATION SECTION ####
aws_profile="$1" # e.g. sot
your_name="$2" # e.g. rory-gilmore
team_name="$3" # e.g. la-vida-mocha (WITH DASHES)

# EC2 config
ec2_ingress_ip="$4" # e.g. 12.34.56.78 (of your laptop where you are running this)

deployment_bucket="${your_name}-raw-deployment-bucket"
ec2_userdata=$(base64 -i userdata)
#### CONFIGURATION SECTION ####

# Create deployment bucket stack
echo ""
echo "Doing deployment bucket..."
echo ""
aws cloudformation deploy --stack-name "${your_name}-raw-deployment-bucket" \
    --template-file deployment-bucket-stack.yml --region eu-west-1 \
    --capabilities CAPABILITY_IAM --profile ${aws_profile} \
    --parameter-overrides \
      YourName="${your_name}";

#if [ -z "${SKIP_PIP_INSTALL:-}" ]; then
#    echo ""
#    echo "Doing pip install..."
#    # Install dependencies from requirements-lambda.txt into src directory
#    py -m pip install --platform manylinux2014_x86_64 \
#        --target=./src --implementation cp --python-version 3.12 \
#        --only-binary=:all: --upgrade -r requirements-lambda.txt;
#else
#    echo ""
#    echo "Skipping pip install"
#fi

# # Create Lambda deployment package
# echo ""
# echo "Creating Lambda deployment package..."
# cd src && zip -r ../lambda_code.zip . && cd ..
# # zip -r ../lambda_code.zip .

# Create Lambda deployment package
#echo ""
#echo "Creating Lambda deployment package..."
## Create a temporary directory for packaging
#mkdir -p lambda_package
## Copy the Lambda handler and dependencies to the package directory
#cp raw_data_etl_lambda.py etl_transform.py lambda_package/
#cp -r utils lambda_package/
## Install Python dependencies in the package directory
#cd lambda_package && pip install --platform manylinux2014_x86_64 \
#    --implementation cp --python-version 3.12 \
#    --only-binary=:all: --upgrade -r ../requirements-lambda.txt --target .
## Create the zip file
#zip -r ../lambda_code.zip .
#cd ..
#zip lamba_code.zip raw_data_etl_lambda.py

# Upload Lambda code to S3
echo ""
echo "Uploading Lambda code to S3..."
aws s3 cp lambda_code.zip "s3://${deployment_bucket}/lambda_code.zip" --profile ${aws_profile}

# Package template and upload local resources to S3
echo ""
echo "Doing packaging..."
echo ""
aws cloudformation package --template-file etl-stack.yml \
    --s3-bucket ${deployment_bucket} \
    --output-template-file etl-stack-packaged.yml \
    --profile ${aws_profile};

# Deploy template
echo ""
echo "Doing etl stack deployment..."
echo ""
aws cloudformation deploy --stack-name "${your_name}-raw-etl-pipeline" \
    --template-file etl-stack-packaged.yml --region eu-west-1 \
    --capabilities CAPABILITY_IAM \
    --profile ${aws_profile} \
    --parameter-overrides \
      YourName="${your_name}" \
      TeamName="${team_name}" \
      EC2InstanceIngressIp="${ec2_ingress_ip}" \
      EC2UserData="${ec2_userdata}";
# Cleanup
#rm lambda_code.zip

echo ""
echo "...all done!"
echo ""

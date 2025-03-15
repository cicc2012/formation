# cicc-formation

In this demo, we are going to experience how to use AWS CloudFormation templates to manipulate AWS resources with the spirit of Infrastructure as Code (IaC).

## Table of Contents

- [Introduction](#introduction)
- [Plans](#plans)
- [Details](#details)
    - [Step 1](#step-1-lambda-for-textract)
    - [Step 2](#step-2-api-gateway)
    - [Step 3](#step-3-create-an-amplify-app)
    - [Step 4](#step-4-deploy-the-amplify-app)
- [Future Work](#future-work)


## Introduction

- CloudFormation is the fundation for IaC practices on AWS.
- After playing around with AWS consoles, we can start the journey of IaC.
- Here is an comparison of [AWS CLI, SDK, CDK, and CloudFormation](compare.md). 
- With CloudFormation, we can purely use code to implement our previous project.
- After getting familiar with CloudFormation, we can reuse the templates to manipulate the AWS resources more flexibly and efficiently. 

## Plans

- [ ] Step 1: Lambda for Textract 
- [ ] Step 2: API Gateway
- [ ] Step 3: Create an Amplify APP
- [ ] Step 4: Deploy the Amplify APP


## Details

### Step 1: Lambda for Textract 

#### Create the lambda function to Textract locally
Create the lambda function to receive the url of S3 image, and deliver it to Textract to detect the text information in the image. This [lambda function](backend/lambda_function.py) is in the folder of backend.

#### Deploy the lambda function to AWS
To deploy this lambda function, we can CloudFormation. The [template](backend/proj3_backend.yml) is in the folder of backend.

#### Test the lambda function
In the web console of AWS Lambda, we can find the deployed function, named ProcessImageFunction. This can be found in the code of our template:
```yaml
  ImageProcessingLambda:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: ProcessImageFunction
      Handler: "lambda_function.lambda_handler"
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        S3Bucket: !Ref ExistingBucketName
        S3Key: proj3/lambda_function.zip  # The Lambda code uploaded to this S3 bucket
      Runtime: python3.13
      Timeout: 30 # Set timeout as needed (max 15 minutes for Lambda)`
```
You can this name as the FunctionName Properites.

To test this lambda function, we can use the test body like:
```json
{
    "body": "{\"s3_url\":\"https://uco-cicc-media.s3.us-east-1.amazonaws.com/proj2/dt.jpg\"}"
}
```

Change the https link with your own S3 object URL.

To deploy this template from command line, you can use:
```bash
aws cloudformation deploy \
  --stack-name your-stack-name \
  --template-url https://your-bucket-name.s3.your-region.amazonaws.com/path/to/your-template.yml \
  --capabilities CAPABILITY_IAM
```
Replace the following placeholders:
- your-stack-name: The name you want to give to your CloudFormation stack
- your-bucket-name: The name of your S3 bucket 
- path/to/your-template.yml: The path to your YAML template file within the S3 bucket
- The --capabilities CAPABILITY_IAM flag is included in case your template creates IAM resources. If your template doesn't create IAM resources, you can omit this flag
The URL can be constructed as follow:
```text
https://your-bucket-name.s3.your-region.amazonaws.com/path/to/your-object
```

### Step 2: API Gateway


### Step 3: Create an Amplify APP


### Step 4: Deploy the Amplify APP


## Future Work

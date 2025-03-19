import boto3
import json
from urllib.parse import urlparse

# Initialize clients for S3, Textract, and Rekognition
s3 = boto3.client('s3')
textract = boto3.client('textract')

def lambda_handler(event, context):

    print(event)

    url = 'World'

    try:
        if (event['queryStringParameters']) and (event['queryStringParameters']['s3_url']) and (
                event['queryStringParameters']['s3_url'] is not None):
            url = event['queryStringParameters']['s3_url']
    except KeyError:
        print('No url')

    try:
        if (event['multiValueHeaders']) and (event['multiValueHeaders']['s3_url']) and (
                event['multiValueHeaders']['s3_url'] is not None):
            url = " and ".join(event['multiValueHeaders']['s3_url'])
    except KeyError:
        print('No url')

    try:
        if (event['headers']) and (event['headers']['s3_url']) and (
                event['headers']['s3_url'] is not None):
            url = event['headers']['s3_url']
    except KeyError:
        print('No url')

    if (event['body']) and (event['body'] is not None):
        body = json.loads(event['body'])
        try:
            if (body['s3_url']) and (body['s3_url'] is not None):
                url = body['s3_url']
        except KeyError:
            print('No url')

    # Parse the S3 URL to get the bucket name and object key
    parsed_url = urlparse(url)
    bucket_name = parsed_url.netloc.split('.')[0]  # Extracts the bucket name
    key = parsed_url.path.lstrip('/')  # Extracts the object key
    print(bucket_name, key)
    
    # Step 2: Call Textract to extract text from the image
    textract_response = extract_text(bucket_name, key)
    
    # Combine results
    result = {
        'text': textract_response
    }

    res = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "*/*",
            "Access-Control-Allow-Origin": "*",  
            "Access-Control-Allow-Methods": "'POST','OPTIONS'",  
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        },
        "body": json.dumps(result)
    }

    return res

# Function to call Textract API to extract text from the image
def extract_text(bucket_name, key):
    try:
        response = textract.detect_document_text(
            Document={'S3Object': {'Bucket': bucket_name, 'Name': key}}
        )
        
        # Extract text lines from the Textract response
        extracted_text = []
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                extracted_text.append(block['Text'])
        
        return extracted_text
    
    except Exception as e:
        print(f"Error in Textract: {str(e)}")
        return {'error': 'Unable to process Textract request'}
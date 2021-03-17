import requests
import botocore
import datetime
import json
import os
from io import BytesIO

import boto3
import PIL
from PIL import Image

# Function that former the url image
def resized_image_url(resized_key, url):
    return "{url}/{resized_key}".format(url=url, resized_key=resized_key)

# Function that resize the image
def resize_image(bucket_name, key):
    
    # Obtain the size and the name of the image
    OriginalKey = key.split('/')
    
    # If the URL is not formed correctly, then return None and show error
    if len(OriginalKey) != 2:
        print("URL: " + resized_image_url(key, os.environ['url']))
        print("ERROR: URL is not correctly formed.")
        return None
    else:
        size = OriginalKey[0]
        image = OriginalKey[1]

    #Established a permanent width
    if size == "small":
        width = 396
    elif size == "medium":
        width = 750
    elif size == "large":
        width = 1280
    elif size == "micro":
        width = 15
    else:
        print("ERROR. This size is not available.")
        return None

    try:
        # Get the original image from S3 bucket
        s3 = boto3.resource('s3')
        obj = s3.Object(
            bucket_name=bucket_name,
            key=image,
        )
        obj_body = obj.get()['Body'].read()
    
        # Open the image, if exists in the bucket S3
        img = Image.open(BytesIO(obj_body))
        
        # If the image is not RGB, then convert to RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Obtain the new heigh
        original_width, original_height = img.size
        new_height = width * original_height / original_width
        
        # Resize the image
        img = img.resize(
            (width, int(new_height)), PIL.Image.ANTIALIAS
        )
        buffer = BytesIO()
        img.save(buffer, 'JPEG', quality=95)
        buffer.seek(0)
    
        resized_key="{key}".format(key=key)
        
        # Put the new image resize into bucket S3
        obj = s3.Object(
            bucket_name=bucket_name,
            key=resized_key,
        )
        obj.put(Body=buffer, ContentType='image/jpeg')
        
        # Return resize image url
        return resized_image_url(resized_key, os.environ['url'])
    
    # Exception in case the image doesn't exists
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == "NoSuchKey":
            print("URL: " + resized_image_url(key, os.environ['url']))
            print("key: " + key)
            print("ERROR: The image not exists in the bucket S3.")

# Main function
def main(event, context):
    
    # Events
    key = event["queryStringParameters"]["key"]
    
    # Call the image resize function
    result_url = resize_image(os.environ['bucket'], key)

    # If the image exits, show the image. If not, show error
    if result_url != None:
        print("Success!!!! Redirecting to the image.")
        
        # If the image exists, then redirect it
        responseObject = {
            "statusCode": 301,
            "body": "",
            "headers": {
                "location": result_url ,
                'Cache-Control': 'no-cache, no-store'
            }
        }
    else:
        # Construct the response body
        transactionresponse = {}
        transactionresponse['url'] = resized_image_url(key, os.environ['url'])
        transactionresponse['key'] = key
        transactionresponse["message"] = "ERROR: Something is not woking correctly. Please, read your logs file."
        
        responseObject = {}
        responseObject['body'] = json.dumps(transactionresponse)

    return responseObject
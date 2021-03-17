# Resize images

Lambda function that received an image and resize it, depends the size that you inserted.

The size must be:

* micro.
* small.
* medium.
* large.

This function received a key, that must be formed like **key=size/image_name** (for both functions files) or **key=size/image_name/extension** where extension must be **webp** or **jpeg** (this key is only valid for the function *resize-image-webp.py*).

The image is saved in a **bucket S3**, where is redirect to an API. You can create this API using the **API Gateway** service.

## Use

1. Zip the file that you need it.

```bash

zip your_script_zip_name.zip <your-function-resize-name>.py

```
2. Install the requirements to launch correctly the function. **Path is necessary**. For the function resize_image.py, **you can comment the package webp** to.

```bash

pip3 install -r requirements.txt -t python/lib/python3.8/site-packages/

```
3. Zip the folder with contains every libraries.

```bash

zip -r your_layer_zip_name.zip python

```

4. Create the layer, uploading the zip generated previously.

5. Create the lambda function, upload the zip generate previously.

You need this global environments to launch correctly your lambda function.

### Global Environments

- **BUCKET**: the name of the bucket S3, example *images*.
- **URL**: the url from your bucket S3, example *https://s3.eu-central-1.amazonaws.com/images*

### Notifications

Setup the notification from API Gateway.

### Basic setup

- Change the name for the controller to **resize_image.main**.
- Change timeout to 10 seconds.

### Permissions and role

Make sure that your role have access to bucket S3 and Cloudwatch for logging.

### Runtime

Python 3.8.

6. Deploy, break and fun!
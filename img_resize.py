import boto3
from io import BytesIO
from PIL import Image

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Retrieve bucket name and object key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    try:
        # Download the image from S3
        image_object = s3_client.get_object(Bucket=bucket, Key=key)
        image_data = image_object['Body'].read()
        
        # Open the image using Pillow
        image = Image.open(BytesIO(image_data))
        
        # Resize the image
        resized_image = image.resize((300, 300))  # Adjust dimensions as needed
        
        # Save the resized image to a buffer
        output_buffer = BytesIO()
        resized_image.save(output_buffer, format="JPEG")
        output_buffer.seek(0)
        
        # Upload the resized image back to S3
        new_key = 'resized/' + key  # Store resized images in a 'resized' folder
        s3_client.put_object(Bucket=bucket, Key=new_key, Body=output_buffer)
        
        print(f"Resized image uploaded to: s3://{bucket}/{new_key}")
        
    except Exception as e:
        print(f"Error resizing image: {e}")
        raise e

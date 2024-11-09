import boto3
import logging
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize boto3 S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Name of your S3 bucket
    bucket_name = 'my-cleanup-bucket'

    # Calculate 30 days ago
    cutoff_date = datetime.now() - timedelta(days=30)

    try:
        # List objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        # Check if the bucket contains any files
        if 'Contents' in response:
            for obj in response['Contents']:
                last_modified = obj['LastModified']
                object_key = obj['Key']
                
                # If file is older than 30 days, delete it
                if last_modified < cutoff_date:
                    logger.info(f"Deleting {object_key} last modified on {last_modified}")
                    
                    # Delete the object
                    s3_client.delete_object(Bucket=bucket_name, Key=object_key)
                else:
                    logger.info(f"Skipping {object_key}, last modified on {last_modified} (still within 30 days)")
        else:
            logger.info(f"No files found in the bucket {bucket_name}.")
    
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise e

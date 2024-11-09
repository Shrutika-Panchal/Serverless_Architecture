import boto3

# Define the bucket name
bucket_name = 'SP_bucket'
# Define the region
region = 'us-east-2'  # Change this to your desired region

# Create an S3 client
s3 = boto3.client('s3', region_name=region)

# Create the S3 bucket with specified region
s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={'LocationConstraint': region}
)

print(f'S3 bucket "{bucket_name}" created successfully in region "{region}".')

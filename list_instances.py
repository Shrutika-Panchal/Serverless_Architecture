''' import boto3

def list_ec2_instances():
    try:
        # Create an EC2 client
        ec2 = boto3.client('ec2')
        
        # Describe EC2 instances
        response = ec2.describe_instances()

        print("List of EC2 Instances:")
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_state = instance['State']['Name']
                print(f"Instance ID: {instance_id}, State: {instance_state}")

    except Exception as e:
        print("An error occurred:")
        print(e)

if __name__ == "__main__":
    list_ec2_instances() '''

import boto3

ec2 = boto3.client('ec2')
response = ec2.describe_instances()

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        print("Instance ID:", instance_id)
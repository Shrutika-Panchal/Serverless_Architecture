import boto3

def lambda_handler(event, context):
    # Initialize Boto3 EC2 client
    ec2_client = boto3.client('ec2')
    
    # Describe instances with Auto-Stop and Auto-Start tags
    response = ec2_client.describe_instances(Filters=[
        {
            'Name': 'tag:Action',
            'Values': ['Auto-Stop', 'Auto-Start']
        }
    ])
    
    # Initialize lists to store instance IDs for logging purposes
    stopped_instances = ['i-0060b45a56416da89']
    started_instances = ['i-01dd88e85476c152e']
    
    # Loop through instances and perform actions based on their tags
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            for tag in instance['Tags']:
                if tag['Key'] == 'Action':
                    action = tag['Value']
                    if action == 'Auto-Stop' and instance['State']['Name'] == 'running':
                        # Stop the Auto-Stop instances if they are currently running
                        ec2_client.stop_instances(InstanceIds=[instance_id])
                        stopped_instances.append(instance_id)
                    elif action == 'Auto-Start' and instance['State']['Name'] == 'stopped':
                        # Start the Auto-Start instances if they are currently stopped
                        ec2_client.start_instances(InstanceIds=[instance_id])
                        started_instances.append(instance_id)
    
    # Print instance IDs that were affected for logging purposes
    print("Instances stopped:", stopped_instances)
    print("Instances started:", started_instances)

# For testing locally
if __name__ == "__main__":
    lambda_handler(None, None)

import boto3
import base64

target = boto3.client('ec2') 
response = target.describe_subnets() 
subnets = response['Subnets']
sub_count = len(subnets)

def create_instance():
    ec2_client = boto3.client("ec2", region_name="us-east-1") 
    
    for n in range(sub_count):
        subnet_id = subnets[n]['SubnetId']
        
        userdata_script = """#!/bin/bash
yum update -y
yum install httpd -y
cd /var/www/html
echo "<html><body><h1> Hello from Karanvir Singh aka $(hostname -f) </h1></body></html>" > index.html
systemctl restart httpd
systemctl enable httpd
"""
        userdata_encoded = base64.b64encode(userdata_script.encode("utf-8")).decode("utf-8")
        
        instances = ec2_client.run_instances(
            ImageId="ami-0715c1897453cabd1",
            SecurityGroupIds=["sg-0ced6b3ac3d1527b1"],
            UserData=userdata_encoded,
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            SubnetId=subnet_id,
            KeyName="vockey",
            TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'Instance' + str(n + 1)}]}]
        )
        
        ec2_instanceId = instances["Instances"][0]["InstanceId"]
        ec2_subnetId = instances["Instances"][0]["SubnetId"]
        ec2_ipv4Id = instances["Instances"][0]["PrivateIpAddress"]
        
        print('The instance with instance ID ', ec2_instanceId, ' and subnet ID ', ec2_subnetId, ' has private address as ', ec2_ipv4Id)
        
    
        
create_instance()

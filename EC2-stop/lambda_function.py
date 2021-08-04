#!/usr/bin/python
# Purpose: Start all the instances having tag "Enviornment=dev" AND "Tenant=prod-dev" or "hibernation=yes"
# Ver 1.0
# Tested for Python 2.7, 3.8
# Author: Ashok Shelke
# -----------------------------------------------------------------------------------
import boto3
import os

# Enter the region your instances are in, e.g. 'us-east-1'

#Variables
region= os.environ["REGION"]

ec2 = boto3.client('ec2', region_name=region)
def lambda_handler(event, context):
    instancelst=[]
    reservations = ec2.describe_instances(
        Filters=[
#            {'Name': 'tag:Environment', 'Values': ['dev']},            
            {'Name': 'tag:hibernation', 'Values': ['yes']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    ).get(
        'Reservations', []
    )

    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])

    for instance in instances:
        instancelst.append(instance['InstanceId'])
    
#    print('stopped your instances: ' + str(instancelst))
#print StoppedInstances  
    if len(instancelst) > 0:
        ec2.stop_instances(InstanceIds=instancelst)
        print('stopped your instances: ' + str(instancelst))
    else:
        print("No instance with given tag value is in running state")

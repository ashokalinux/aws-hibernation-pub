#!/usr/bin/python
# Purpose: Start all the instances having tag "Enviornment=dev" AND "Tenant=prod-dev" or "hibernation=yes"
# Ver 1.0
# Tested for Python 2.7, 3.8
# Author: Ashok Shelke
# -----------------------------------------------------------------------------------
import boto3
import os
# Enter the region your instances are in under "Environment variables" section of "Configuration" tab of lambda, e.g. 'key=REGION'; 'value=us-east-1'

#Variables
region= os.environ["REGION"]

#define the connection and set the region
ec2 = boto3.client('ec2', region)
def lambda_handler(event, context):
    instancelst=[]
    reservations = ec2.describe_instances(
        Filters=[
#            {'Name': 'tag:Environment', 'Values': ['dev']},
            {'Name': 'tag:hibernation', 'Values': ['yes']},
            {'Name': 'instance-state-name', 'Values': ['stopped']}

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

#print StartedInstances  
    if len(instancelst) > 0:
        ec2.start_instances(InstanceIds=instancelst)
        print('started your instances: ' + str(instancelst))
    else:
        print("No instance with given tag value is in stopped state")

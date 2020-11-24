#!/usr/bin/env python

import boto3

rds = boto3.client('rds')

# only need to do this once
try: 
    cpg = rds.create_db_cluster_parameter_group(
        DBClusterParameterGroupName='music-pipeline',
        DBParameterGroupFamily='aurora5.6',
        Description='for loading raw data',
        Tags=[
            {
            'Key': 'Name',
            'Value': 'Staging'
            },
        ]
    )
except:
    pass

db_cluster = rds.create_db_cluster(
    AvailabilityZones=[
        'us-east-1a',
    ],
    BackupRetentionPeriod=1,
    DBClusterIdentifier='music-pipeline-staging',
    DBClusterParameterGroupName='music-pipeline',
    DatabaseName='staging1',
    Engine='aurora',
    EngineMode='serverless',
    ScalingConfiguration={
        'MinCapacity': 1,
        'MaxCapacity': 1, # since we are just doing scraping the total data will be low
        'AutoPause': True,
        'SecondsUntilAutoPause': 300,
        },
    MasterUserPassword=input('my password:'),
    MasterUsername='root',
    Port=3306,
    StorageEncrypted=True,
)

#instance = rds.create_db_instance(
#  DBInstanceIdentifier = 'staging-instance1a',
#  DBInstanceClass = 'db.t3.medium', # smallest standard instance
#  Engine='aurora',
#  DBClusterIdentifier='music-pipeline-staging' # this is where you put the cluster name
#)

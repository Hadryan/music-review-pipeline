#!/usr/bin/env python

import boto3

rds = boto3.client('rds')

cpg = rds.create_db_cluster_parameter_group(
    DBClusterParameterGroupName='staging',
    DBParameterGroupFamily='aurora5.6',
    Description='for loading raw data',
    Tags=[
        {
            'Key': 'Name',
            'Value': 'Staging'
        },
    ]
)

db_cluster = rds.create_db_cluster(
    AvailabilityZones=[
        'us-east-1a',
    ],
    BackupRetentionPeriod=1,
    DBClusterIdentifier='mydbcluster1',
    DBClusterParameterGroupName='staging',
    DatabaseName='staging1',
    Engine='aurora',
    EngineVersion='5.6.10a',
    MasterUserPassword=input('my password:'),
    MasterUsername=staging_admin,
    Port=3306,
    StorageEncrypted=True,
)

instance = rds.create_db_instance(
  DBInstanceIdentifier = 'staging_instance1',
  DBInstanceClass = 'db.t3.medium', # smallest standard instance
  Engine='aurora',
  DBClusterIdentifier='staging_cluster1' # this is where you put the cluster name
)

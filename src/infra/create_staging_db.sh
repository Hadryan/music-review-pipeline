#!/bin/sh
aws rds create-db-cluster --db-cluster-identifier staging-cluster --engine aurora-postgresql --engine-version 10.12 \
--engine-mode serverless --scaling-configuration MinCapacity=8,MaxCapacity=64,SecondsUntilAutoPause=1000,AutoPause=true \
--master-username chrisoyer

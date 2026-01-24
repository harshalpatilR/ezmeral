# Virtual Services in Private Cloud AI

## Purpose

This folder has various Istio Virtual Services that are useful to interact with appliance from external system.

They include Virtual Services to 

[1. ingest data into S3](s3_based_data_sharing.md)

[2. get access to Prometheus monitoring](prometheus_access.md)

[3. get access to helm charts](chartmuseum_access.md) 

The same concept can be extended by Kubernetes Admin of this appliance to expose additional services inside the cluster as needed.


# Spark on K8s Kafka Consumer to Write Iceberg Table

<br>

##### This is a Kafka Consumer details that reads from Kafka Topic and writes to Iceberg table in Object Store
##### The object store is S3 compatible object atore on Ezmeral Data Fabric
##### The Kafka Consumer is running under Spark on K8s on Ezmeral Unified Analytics

<br>

###### 1. Running Spark on K8s Consumer via Ezmeral Unified Analytics (UA) UI

<br>

![UA Spark](images/UAspark_stream_app_running.png) 

###### 2. Spark History Server view of running Streaming Application

![UA Spark Streaming App](images/spark_k8s_application.png) 

###### 3. Spark History Server details of running Streaming Application

![UA Spark Stream Details](images/spark_K8s_stream_1.png) 

###### 4. Iceberg Table in S3 bucket

![EDF S3 Iceberg Table](images/S3iceberg_kafka_ingest4.png)

###### 5. Iceberg Table in S3 bucket - Table Metadata

![EDF S3 Iceberg Table Metadata](images/S3iceberg_kafka_ingest4_metadata.png)

###### 6. Iceberg Table in S3 bucket - Table Data

![EDF S3 Iceberg Table Data](images/S3iceberg_kafka_ingest4_data.png)

###### 7. Iceberg Table in S3 bucket - Checkpoints

![EDF S3 Iceberg Table Checkpoints](images/S3iceberg_checkpoints.png)

###### 8. Iceberg Table in S3 bucket - Commits

![EDF S3 Iceberg Table Checkpoints](images/S3iceberg_checkpoints.png)





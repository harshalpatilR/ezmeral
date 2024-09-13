# Spark on K8s Kafka Consumer to Write Iceberg Table

<br>

##### This is a Kafka Consumer details that reads from Kafka Topic and writes to Iceberg table in Object Store
##### The object store is S3 compatible object atore on Ezmeral Data Fabric
##### The Kafka Consumer is running under Spark on K8s on Ezmeral Unified Analytics

<br>

###### 1. Running Spark on K8s Consumer via Ezmeral Unified Analytics (UA) UI

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

![EDF S3 Iceberg Table Commits](images/S3iceberg_commits.png)

###### 9. Presto connected to Iceberg Table in S3 bucket

![Presto S3 Iceberg Table](images/Presto_reads_S3_table.png)

###### 10. Presto connected to Iceberg Table in S3 bucket - read Iceberg Snapshots present in table

![Presto S3 Iceberg Snapshots](images/Presto_Iceberg_snapshots_S3table.png)

###### 11. Presto connected to Iceberg Table in S3 bucket - Select data from Iceberg table

![Presto S3 Iceberg Select](images/Presto_iceberg_S3table_select.png)

###### 12. Superset connected to Presto which is in-turn connected to Iceberg Table in S3 bucket

![Superset to Presto](images/superset-to-Presto-icebergS3.png)

###### 13. Superset can query to Presto which is in-turn connected to Iceberg Table in S3 bucket

![Superset to Presto Query Iceberg](images/superset-query-S3iceberg.png)

###### 14. Superset Real-Time Dashboard - KPIs update each 30 second based on Streaming Data 

![Superset Dashboard](images/superset-dashboard-streamingKPI.png)



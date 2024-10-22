# EZPresto Iceberg Operations
## This document shows query operations with EZPresto 
#### Read the file ingested via Python Producer to Kafka to Spark Structured Streaming to EDF / Iceberg to UA Presto
#### UA 1.5 Presto connector: [https://prestodb.io/docs/0.287/connector/iceberg.html](https://prestodb.io/docs/0.287/connector/iceberg.html)
<br>
<br>

1) After each ingestion, the counts will keep increasing. Check streaming counts are ok. 


```sql
select count(*) as num_records from dficeberg.default.kafka_ingest3
```

![Counts](images/iceberg_counts.jpg)
<br>
<br>

2) Ensure select works on the stream ingestion table. We should be able to select recrods from this table.

```sql
select * from dficeberg.default.kafka_ingest3
```

![Select](images/iceberg_select.jpg)
<br>
<br>


3) Ensure snapshots are visible. It is indeed Iceberg table.

```sql
select made_current_at, cast(snapshot_id as varchar) as snapshot, cast(parent_id as varchar) as parent, is_current_ancestor from dficeberg.default."kafka_ingest3$history"
```

![Snapshots](images/iceberg_snapshots.jpg)
<br>
<br>

4) Check time-travel by using the first snapshot created after append of 1st record to the Iceberg table. You should get only 1 record in the output.

```sql
select * from dficeberg.default.kafka_ingest3 FOR VERSION AS OF 1431105276184260366
```

![Time Travel](images/iceberg_timetravel.jpg)
<br>
<br>

5) Iceberg Connector can be configured via Ezmeral Unified Analytics UI.
![](images/Presto_Iceberg_connector.jpg)

Once added, the connector becomes active and can be used as data source to run Presto queries.
![](images/iceberg-connector-active.png)

This connector details can be checked via Presto Master Pod. The specific configurations are provided below.

```bash
$ cat s3icebergdata.properties

#adding catalog using endpoint
#Thu Sep 26 09:54:32 UTC 2024
hive.s3.path-style-access=true
hive.s3.aws-secret-key=<xxx>
hive.s3.aws-access-key=<xxx>
iceberg.catalog.cached-catalog-num=10
hive.s3.endpoint=https\://<IP>\:9000
iceberg.hadoop.config.resources=/etc/presto/catalog/s3icebergdata/iceberg.hadoop.config.resources.config
connector.name=iceberg
hive.s3.ssl.enabled=false
iceberg.catalog.warehouse=s3\://icebergdata/warehouse
iceberg.catalog.type=hadoop
```
```bash
$ cat /etc/presto/catalog/s3icebergdata/iceberg.hadoop.config.resources.config

<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>        
    <property>
        <name>presto.s3.ssl.enabled</name>
        <value>false</value>
    </property>

    <property>
        <name>presto.s3.access-key</name>
        <value>VABG8RZ0CHH8X49L91M4NIU2SZT18QDHJ8WY1DDIMCYQ7LNXE2Q03OK0J9I08TVM28MFCJ106CM7C9KEJ7E1I2G01TY6YL6V6D4WUJOO052B7F15Z7EQI4ARS</value>
    </property>

    <property>
        <name>presto.s3.secret-key</name>
        <value>VLPC88QV6Z9LQ63LPRUCK9XT2GCP7FXGZYL4F4JMLUUMGPNJ5C6V18VGCWEPLNUNATAYDZ310POFLYY90UBOR38ILSNWSDIUQSO8M16DYP3NVU5</value>
    </property>

    <property>
        <name>presto.s3.endpoint</name>
        <value>https://18.223.205.241:9000</value>
    </property>

    <property>
        <name>presto.s3.path-style-access</name>
        <value>true</value>
    </property>
    
    <property>
        <name>fs.s3.impl</name>
        <value>com.facebook.presto.hive.s3.PrestoS3FileSystem</value>
    </property>

    <property>
        <name>fs.s3a.impl</name>
        <value>com.facebook.presto.hive.s3.PrestoS3FileSystem</value>
    </property>
```
<br>
<br>
6) Similarly, Delta-Lake connector can be configured to connect to Delta-Lake tables as well. 
![](images/Presto_Delta_connector.jpg)

Once added, the connector becomes active and can be used a data source to run Presto queries.
![](images/delta-connector-active.png)

The details on configuration taken from Presto Master Pod are as below.

```bash
[presto@ezpresto-sts-mst-0 catalog]$ cat taxidelta.properties

#adding catalog using endpoint
#Fri Sep 13 15:51:51 UTC 2024
hive.s3.path-style-access=true
hive.hdfs.presto.principal=presto
hive.s3.aws-secret-key=<xxxx>
hive.s3.aws-access-key=<xxxx>
hive.s3.endpoint=https\://<IP>\:9000
connector.name=delta
hive.s3.ssl.enabled=false
hive.metastore=deltadiscovery
delta.datadir=s3\://delta/taxidelta/
```

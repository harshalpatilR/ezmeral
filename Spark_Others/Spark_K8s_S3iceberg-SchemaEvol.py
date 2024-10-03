from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, IntegerType, ArrayType
from pyspark.sql.functions import col, from_json

# this depends on the Spark K8s image - different images use different directories to store JARs
import os
#/opt/spark/conf::/opt/spark/jars/*:/opt/spark/work-dir
#print(os.getcwd())  
#print(os.listdir("/opt/spark/conf"))
#print(os.listdir("/opt/spark/jars"))
#print(os.listdir("/opt/spark/work-dir"))

# S3 console via https://ip-172-31-6-110.us-east-2.compute.internal:8443/app/mcs/#/app/overview
# you may choose to turn off warnings and their details
#.config("spark.sql.warnings.enabled", "true") \
#.config("spark.sql.warnings.level", "all") \
#.config("spark.sql.warnings.verbose", "true") \

# set table to use
querytable = "local.default.kafka_ingest3"
inputtable = "local.default.kafka_ingest5"

# spak session
spark = SparkSession \
.builder \
.appName("HarshalSchemaEvolDemoS3") \
.config("spark.streaming.stopGracefullyOnShutdown", "true") \
.config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
.config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
.config("spark.sql.catalog.local.type", "hadoop") \
.config("spark.sql.catalog.local.warehouse", "s3a://icebergdata/warehouse") \
.config("spark.logger", "ERROR") \
.getOrCreate()

print("-" * 20)
print("-" * 20)
print("-" * 20)

# queries to run
querylist = [
#    f"CREATE TABLE IF NOT EXISTS {querytable} (id bigint, name varchar(100), address varchar(500), amount bigint),
    f"CREATE OR REPLACE TABLE {querytable} As Select * from {inputtable} limit 300",
    f"select * from {querytable} limit 10",
    f"ALTER TABLE {querytable} ADD COLUMN selcol VARCHAR(10)",
    f"select * from {querytable} limit 10",
    f"ALTER TABLE {querytable} RENAME COLUMN selcol to highval",
    f"select * from {querytable} limit 10",
    f"UPDATE {querytable} SET highval = 'Y' WHERE amount > 400000",
    f"select * from {querytable} limit 10",
    f"select * from {querytable} WHERE highval = 'Y'"
]

commentlist = [
    f"--- Check and create empty table {querytable} if not exists",
    f"--- List contents to check table {querytable}",
    f"--- Alter schema and add a columnn in {querytable}",
    f"--- Alter schema and add a columnn in {querytable}",    
    f"--- Alter schema and modify columnn name in {querytable}",
    f"--- Alter schema and modify columnn name in {querytable}",    
    f"--- Update added column in {querytable} to identify 400k or more in amount",
    f"--- Update added column in {querytable} to identify 400k or more in amount",    
    f"--- Use added column in {querytable} to list out 400k or more in amount clients"
    
]

for query, comment in zip(querylist, commentlist):
    
    print(comment)
    print(query)
    spark.sql(query).show()
    
print(" ---- end of Iceberg Schema Evolution ----")
print("-" * 20)
print("-" * 20)
print("-" * 20)


from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, IntegerType, ArrayType
from pyspark.sql.functions import col, from_json

# this depends on the Spark K8s image - different images use different directories to store JARs
import os
#/opt/spark/conf::/opt/spark/jars/*:/opt/spark/work-dir
print(os.getcwd())  
print(os.listdir("/opt/spark/conf"))
print(os.listdir("/opt/spark/jars"))
print(os.listdir("/opt/spark/work-dir"))

# S3 console via https://ip-172-31-6-110.us-east-2.compute.internal:8443/app/mcs/#/app/overview
# you may choose to turn off warnings and their details
spark = SparkSession \
.builder \
.appName("HarshalIngestDemoS3") \
.config("spark.sql.warnings.enabled", "true") \
.config("spark.sql.warnings.level", "all") \
.config("spark.sql.warnings.verbose", "true") \
.config("spark.streaming.stopGracefullyOnShutdown", "true") \
.config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
.config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
.config("spark.sql.catalog.local.type", "hadoop") \
.config("spark.sql.catalog.local.warehouse", "s3a://icebergdata/warehouse") \
.getOrCreate()
        
#ingest table 
spark.sql("CREATE TABLE IF NOT EXISTS local.default.kafka_ingest5 (id bigint, name varchar(100), address varchar(500), amount bigint)")
spark.sql("select * from local.default.kafka_ingest5 limit 10").show()

schema = StructType([StructField("id", IntegerType()),
StructField("name", StringType()),
StructField("address", StringType()),
StructField("amount", IntegerType())
])

options = {
#    "kafka.sasl.jaas.config": 'org.apache.kafka.common.security.plain.PlainLoginModule required username="mapr" password="mapr";',
#    "kafka.sasl.mechanism": "PLAIN",
#    "kafka.security.protocol" : "SASL_PLAINTEXT",
    "kafka.bootstrap.servers": "13.215.254.242:9092",
    "subscribe": "freshtopic",
    "startingOffsets": "earliest"}

kafka_df = spark.readStream.format("kafka").options(**options).load()
kafka_df.printSchema()


value_df = kafka_df.select(from_json(col("value").cast("string"), schema))
value_df.printSchema()

output_df = value_df.selectExpr("`from_json(CAST(value AS STRING))`.id", 
                   "`from_json(CAST(value AS STRING))`.name",
                   "`from_json(CAST(value AS STRING))`.address",
                   "`from_json(CAST(value AS STRING))`.amount")

output_df.printSchema()

#write_query = output_df.writeStream.format("console").outputMode("append").trigger(processingTime="30 seconds").start().awaitTermination()

write_query = output_df.writeStream.format("iceberg").outputMode("append").trigger(processingTime="30 seconds").option("checkpointLocation", "s3a://checkpoints/kafka_ingest5").toTable("local.default.kafka_ingest5").awaitTermination()
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, IntegerType, ArrayType
from pyspark.sql.functions import col, from_json

#.config("spark.jars", "/home/harshal/spark-sql-kafka-0-10_2.13-3.5.1.jar,/home/harshal/spark-streaming-kafka-0-10_2.12-3.5.1.jar,/home/harshal/kafka-clients-2.6.1.jar") \
#.config("spark.jars", "/opt/spark/work-dir/spark-sql-kafka-0-10_2.13-3.5.1.jar,/opt/spark/work-dir/spark-streaming-kafka-0-10_2.12-3.5.1.jar,/opt/spark/work-dir/kafka-clients-2.6.1.jar") \

import os
#/opt/spark/conf::/opt/spark/jars/*:/opt/spark/work-dir
print(os.getcwd())  
print(os.listdir("/opt/spark/conf"))
print(os.listdir("/opt/spark/jars"))
print(os.listdir("/opt/spark/work-dir"))

spark = SparkSession \
.builder \
.appName("File Streaming Demo") \
.config("spark.sql.warnings.enabled", "true") \
.config("spark.sql.warnings.level", "all") \
.config("spark.sql.warnings.verbose", "true") \
.config("spark.streaming.stopGracefullyOnShutdown", "true") \
.getOrCreate()

schema = StructType([StructField("id", IntegerType()),
StructField("name", StringType()),
StructField("address", StringType()),
StructField("amount", IntegerType())
])

options = {
    "kafka.sasl.jaas.config": 'org.apache.kafka.common.security.plain.PlainLoginModule required username="mapr" password="mapr";',
    "kafka.sasl.mechanism": "PLAIN",
    "kafka.security.protocol" : "SASL_PLAINTEXT",
    "kafka.bootstrap.servers": "172.31.37.92:9092",
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

write_query = output_df.writeStream.format("console").outputMode("append").trigger(processingTime="59 seconds").start().awaitTermination()

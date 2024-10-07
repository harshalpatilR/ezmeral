##### Schema Evolution in Iceberg

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, IntegerType, ArrayType
from pyspark.sql.functions import col, from_json

# this depends on the Spark K8s image - different images use different directories to store JARs
import os
import time
import datetime

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
# keeping the streaming property in comments - not needed for schema evolution code
#.config("spark.streaming.stopGracefullyOnShutdown", "true") \
#.config("spark.logger", "ERROR") \

# set table to use
querytable = "local.default.kafka_ingest3"
inputtable = "local.default.kafka_ingest5"

# redirect output to a file for ease of reading
# this can be a parameter in Airflow DAG - but we will hardcode for now
fixedfile = "SchemaEvol"
unique = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
oppath = "/mounts/shared-volume/shared/airflow" 
opfile = oppath + "/" + fixedfile + unique + ".txt"

# spak session
spark = SparkSession \
.builder \
.appName("HarshalSchemaEvolDemoS3") \
.config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
.config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
.config("spark.sql.catalog.local.type", "hadoop") \
.config("spark.sql.catalog.local.warehouse", "s3a://icebergdata/warehouse") \
.getOrCreate()

spark.sparkContext.setLogLevel("WARN")

writefile = open(opfile, "w+")

print("-" * 20, file=writefile)
print("-" * 20, file=writefile)
print("-" * 20, file=writefile)

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

printlist = [
    False,
    True,
    False,
    True,
    False,
    True,
    False,
    True,
    True
]


os.mkdir(oppath + "/" + fixedfile + unique + "_D")

for query, comment, printdf in zip(querylist, commentlist, printlist):
    print("\n", file=writefile) 
    print(comment, file=writefile)
    print(query, file=writefile)
    df = spark.sql(query)
    if printdf:
        print("Output: DF output written in a file", file=writefile)  
        df.write.mode('append').csv(oppath + "/" + fixedfile + unique + "_D", header=True)
        
print("\n ---- end of Iceberg Schema Evolution ----", file=writefile)
print("-" * 20, file=writefile)
print("-" * 20, file=writefile)
print("-" * 20, file=writefile)

writefile.close()


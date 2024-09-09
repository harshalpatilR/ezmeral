# by harshal patil
# this is a working consumer on EDF 7.7 EEP 921
# /opt/mapr/spark/spark-3.3.3/bin/pyspark --packages org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.4.2

# to deploy


from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, IntegerType, ArrayType
from pyspark.sql.functions import col, from_json


#.config("spark.sql.catalog.local.warehouse", "file:///mapr/ez-anz-df/localiceberg") \

spark = SparkSession \
.builder \
.appName("File Streaming Demo") \
.config("spark.streaming.stopGracefullyOnShutdown", "true") \
.config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
.config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
.config("spark.sql.catalog.local.type", "hadoop") \
.config("spark.sql.catalog.local.warehouse", "maprfs:///localiceberg") \
.getOrCreate()


# to iceberg
# creating iceberg table first
# issue maprlogin password ticket first - else file accesss errors
# spark.sql("CREATE TABLE IF NOT EXISTS local.default.kafka_ingest3 (id bigint, name varchar(100), address varchar(500), amount bigint)")
# test one record
# spark.sql("INSERT INTO local.default.kafka_ingest3 VALUES (000000, 'Harshal Patil', '111 test drive, singapore', 123456);")
# spark.sql("select * from local.default.kafka_ingest3").show()

# +---+-------------+--------------------+------+
# | id|         name|             address|amount|
# +---+-------------+--------------------+------+
# |  0|Harshal Patil|111 test drive, s...|123456|
# +---+-------------+--------------------+------+



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

# print to console
#write_query = output_df.writeStream.format("console").outputMode("append").trigger(processingTime="59 seconds").start().awaitTermination()
# ctl-c to terminate


# -------------------------------------------                                                                                           
# Batch: 2
# -------------------------------------------
# +-----+--------------------+--------------------+------+
# |   id|                name|             address|amount|
# +-----+--------------------+--------------------+------+
# |12272|       Frances Noble|401 Chambers Grov...|266543|
# |24050|       Eric Richards|742 Edward Brook ...|524941|
# |47008|      Matthew Walker|196 Terri Turnpik...|316526|
# |40090|       Jose Phillips|62302 Hart Island...|239347|
# |88804|        Brian Murphy|315 Anderson Well...|575272|
# |75680|     Jennifer Garcia|81612 Hall Forges...|952545|
# |12159|    Jennifer Simpson|98046 Jacobs Fiel...|129123|
# |72635|      Travis Nichols|6662 Brown Square...| 24169|
# |96055|       Victoria Gray|791 Villegas Lane...|377509|
# |26652|          Jason Ryan|Unit 4756 Box 716...|213180|
# |45244|       Tiffany Baker|540 Foley Rapid\n...|113415|
# |22765|       Ryan Sullivan|117 Ruiz Plain Ap...|968526|
# |38604|      Cindy Anderson|51890 Carolyn Ave...|517766|
# |44682|        Carol Miller|31352 Rodriguez O...|457087|
# |75100|       Mark Williams|83184 Ryan Shore ...|453818|
# | 1417|        Cody Johnson|USNS Farrell\nFPO...|498911|
# |76209|      Sandra Harrell|798 Sarah Summit ...|396909|
# | 8559|          Mary Craig|735 Moore Common\...|344908|
# | 7589|Kimberly Anderson MD|7913 Banks River ...| 27825|
# |40835|      Mark Armstrong|87853 Wong Park S...| 74030|
# +-----+--------------------+--------------------+------+
# only showing top 20 rows



write_query = output_df.writeStream.format("iceberg").outputMode("append").trigger(processingTime="59 seconds").option("checkpointLocation", "maprfs:///test/chkpoint").toTable("local.default.kafka_ingest3")
#write_query = output_df.writeStream.format("iceberg").outputMode("append").trigger(processingTime="59 seconds").option("checkpointLocation", "/mapr/ez-anz-df/test/chkpoint").toTable("local.default.kafka_ingest2")
# ctl-c to terminate

#sheck the last record is the same as last generated in python kafka producer
table = spark.sql("select * from local.default.kafka_ingest3")
table.head()
table.tail(1)

#check shape of df
table.count()
table.columns
table.show(table.count())


# check to see multiple snapshots - one for each append
spark.sql("select * from local.default.kafka_ingest3.snapshots").show()



# +--------------------+-------------------+-------------------+---------+--------------------+--------------------+
# |        committed_at|        snapshot_id|          parent_id|operation|       manifest_list|             summary|
# +--------------------+-------------------+-------------------+---------+--------------------+--------------------+
# |2024-09-09 04:50:...|1431105276184260366|               null|   append|maprfs:/localiceb...|{spark.app.id -> ...|
# |2024-09-09 04:55:...|4456689898849003606|1431105276184260366|   append|maprfs:/localiceb...|{spark.app.id -> ...|
# |2024-09-09 04:56:...|6960058330029300603|4456689898849003606|   append|maprfs:/localiceb...|{spark.app.id -> ...|
# +--------------------+-------------------+-------------------+---------+--------------------+--------------------+

#
#+--------------------+-------------------+-------------------+---------+--------------------+--------------------+
#|        committed_at|        snapshot_id|          parent_id|operation|       manifest_list|             summary|
#+--------------------+-------------------+-------------------+---------+--------------------+--------------------+
#|2024-09-05 05:38:...|5216326873244364635|               null|   append|file:/mapr/ez-anz...|{spark.app.id -> ...|
#|2024-09-05 05:39:...|3786370328313876646|5216326873244364635|   append|file:/mapr/ez-anz...|{spark.app.id -> ...|
#+--------------------+-------------------+-------------------+---------+--------------------+--------------------+




######### 
# end of file

import pyspark
from pyspark.sql.session import SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("ReadCSVFromS3Proxy").getOrCreate()

# Specify the S3 bucket and file path
bucket_name = "ezaf-demo"
file_path = "data/financial.csv"

# Read the CSV file from S3
df = spark.read.csv(f"s3a://{bucket_name}/{file_path}", header=True, inferSchema=True)

# Show the first few rows of the DataFrame
df.show()
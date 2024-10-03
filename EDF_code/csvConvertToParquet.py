from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, DoubleType

import argparse

def main():

    # Create a Spark session
    spark = SparkSession.builder.appName("CSVToParquet").getOrCreate()

    parser = argparse.ArgumentParser(description="Convert CSV to Parquet")
    parser.add_argument("--csv-file", required=True, help="Path to the CSV file")
    parser.add_argument("--parquet-output", required=True, help="Path for the Parquet output file")
    args = parser.parse_args()

    # Define the path to the CSV file
#    csv_file_path = "maprfs:///Data/data10.csv"
    csv_file_path = args.csv_file

    # Define the schema for your CSV data
    schema = StructType([
        StructField("timestamp", StringType(), True),
        StructField("id_uint16", IntegerType(), True),
        StructField("id_string", StringType(), True),
        StructField("ip_string1", StringType(), True),
        StructField("port_uint16", IntegerType(), True),
        StructField("ip_string2", StringType(), True),
        StructField("port_uint16_2", IntegerType(), True),
        StructField("num_uint16_1", IntegerType(), True),
        StructField("num_uint16_2", IntegerType(), True),
        StructField("num_uint16_3", IntegerType(), True),
        StructField("num_uint16_4", IntegerType(), True),
        StructField("data_string1", StringType(), True),
        StructField("data_string2", StringType(), True),
        StructField("numeric_uint16", IntegerType(), True),
        StructField("time_usec_uint64", LongType(), True),
        StructField("timestamp_uint64", LongType(), True),
        StructField("flags_uint16", IntegerType(), True),
        StructField("one_or_zero_uint8", IntegerType(), True),
        StructField("response_code_uint16", IntegerType(), True),
        StructField("data_string3", StringType(), True),
        StructField("numeric_uint8", IntegerType(), True),
        StructField("data_length_bytes_uint16", IntegerType(), True),
        StructField("numeric_uint16_2", IntegerType(), True),
        StructField("time_seconds_uint16", IntegerType(), True),
        StructField("data_string4", StringType(), True),
        StructField("one_or_zero_uint8_2", IntegerType(), True),
        StructField("flag_uint16", IntegerType(), True)
    ])

    # Read the CSV file into a DataFrame with the specified schema
    df = spark.read.csv(csv_file_path, header=True, schema=schema)
    
    # Define the path for the Parquet file with Snappy compression
#    parquet_output_path = "maprfs:///Data/data10.parquet"
    parquet_output_path = args.parquet_output

    # Write the DataFrame to Parquet format with Snappy compression
    df.write.parquet(parquet_output_path, mode="overwrite", compression="snappy")

    # Stop the Spark session
    spark.stop()

    print(f"CSV file '{csv_file_path}' has been successfully converted to Parquet format and saved in '{parquet_output_path}' with Snappy compression.")

if __name__ == "__main__":
    main()

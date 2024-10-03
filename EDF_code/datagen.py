
import csv
import random
import string
import threading

# Define the number of records
num_records = 1600000

# Define the CSV file path
csv_file_path = "multiThreadrecords.csv"

# Lock to synchronize access to the CSV file
csv_file_lock = threading.Lock()

# Function to generate and write records
def generate_and_write_records(start, end):
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for _ in range(start, end):
            record = [
                str(random.randint(20210101010101, 20211231235959)),  # timestamp
                random.randint(0, 65535),  # id (uint16)
                ''.join(random.choice(string.digits) for _ in range(18)),  # id (string)
                f'{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}',  # ip
                random.randint(0, 65535),  # port
                f'{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}',  # ip
                random.randint(0, 65535),  # port
                random.randint(0, 65535),  # num
                random.randint(0, 65535),  # num
                random.randint(0, 65535),  # num
                random.randint(0, 65535),  # num
                'sample.string.net',  # Data string
                'sample.string.net',  # Data string
                random.randint(0, 65535),  # numeric
                random.randint(0, 18446744073709551615),  # Time in usec (uint64)
                random.randint(0, 18446744073709551615),  # timestamp (uint64)
                random.randint(0, 65535),  # flags
                random.randint(0, 1),  # 1 or 0 (uint8)
                random.randint(0, 65535),  # Response code
                'samplestring',  # Data string
                random.randint(0, 255),  # numeric (uint8)
                random.randint(0, 65535),  # Data length in bytes
                random.randint(0, 65535),  # numeric
                random.randint(0, 65535),  # Time in seconds
                'sample.data.net',  # data string
                random.randint(0, 1),  # 1 or 0 (uint8)
                random.randint(0, 65535)  # flag
            ]
            with csv_file_lock:
                writer.writerow(record)

# Open the CSV file for writing (overwrite if it already exists)
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    # Write the header
    writer.writerow(["timestamp", "id", "ip", "port", "num", "Data", "numeric", "Time in usec",
                     "timestamp_uint64", "flags", "1 or 0", "Response code", "Data string",
                     "numeric_uint8", "Data length in bytes", "numeric_uint16", "Time in seconds", "data",
                     "1 or 0_uint8", "flag_uint16"])

# Define the number of threads
num_threads = 4

# Calculate the number of records per thread
records_per_thread = num_records // num_threads

# Create and start threads to generate and write records
threads = []
for i in range(num_threads):
    start = i * records_per_thread
    end = start + records_per_thread if i < num_threads - 1 else num_records
    thread = threading.Thread(target=generate_and_write_records, args=(start, end))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print(f'{num_records} records have been generated and saved to "{csv_file_path}".')


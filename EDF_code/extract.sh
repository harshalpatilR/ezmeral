#!/bin/bash

# Record the start time
start_time=$(date +%s.%N)

# Specify the number of parallel processes
num_processes=6

# Directory containing LZ4-compressed files
input_dir="/home/mapr/Lz4files/"

# Function to decompress and save as CSV
decompress_file() {
    lz4 -i -d -1 "$1" > "${1%.lz4}.csv"
    rm "$1"
}

export -f decompress_file

# Use find to locate LZ4 files in the directory and use parallel to decompress and save as CSV
find "$input_dir" -type f -name "*.lz4" | parallel -j $num_processes decompress_file

# Record the end time
end_time=$(date +%s.%N)

# Calculate the duration
duration=$(echo "$end_time - $start_time" | bc)

echo "Script took $duration seconds to run."

#!/bin/bash

# Record the start time

start_time=$(date +%s)


for i in {1..18}; do
#    if [[ $i -ge 1 && $i -le 6 ]]; then
#        csv_file="maprfs:///Data/node1-csv/data$i.csv"
#        parquet_file="maprfs:///Data/node1-csv/data$i.parquet"
#    elif [[ $i -ge 7 && $i -le 12 ]]; then
#        csv_file="maprfs:///Data/node2-csv/data$i.csv"
#        parquet_file="maprfs:///Data/node2-csv/data$i.parquet"
#    elif [[ $i -ge 13 && $i -le 18 ]]; then
#        csv_file="maprfs:///Data/node3-csv/data$i.csv"
#        parquet_file="maprfs:///Data/node3-csv/data$i.parquet"
#    fi
     csv_file="maprfs:///Data/node1-lz4/data$i.csv"
     parquet_file="maprfs:///Data/node1-parquet/data$i.parquet"
     /opt/mapr/spark/spark-3.3.2/bin/spark-submit --master yarn --conf spark.driver.memory=6g --conf spark.executor.memory=6g --conf spark.ui.enabled=false --conf spark.yarn.executor.memoryOverhead=1G --conf spark.yarn.maxAppAttempts=6 --num-executors 3 --executor-cores 4 csvConvertToParquet.py --csv-file "$csv_file" --parquet-output "$parquet_file" &
    echo "Started job $i"
done

echo "Waiting for all the jobs to complete"

wait
# Record the end time
end_time=$(date +%s)

# Calculate the elapsed time
elapsed_time=$((end_time - start_time))

echo "All background commands have completed."
echo "Total execution time: $elapsed_time seconds."

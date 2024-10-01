from airflow import DAG
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator
from airflow.utils.dates import days_ago
import subprocess
import venv
import os

# define all included single function
def generate_kafka_records():
    from kafka import KafkaProducer
    #from kafka import KafkaConsumer
    import sys
    import time
    import random
    import json
    #import pandas as pd
    #import pyarrow as pa
    #import pyarrow.parquet as pq
    import datetime as tm
    from faker import Faker

    #Kafka source details - this is for EDF Kafka Wire Protocol - so the broker is where Data Access Gateway is running and its port
    server = "13.215.254.242:9092"
    topic = "freshtopic"
    print("BROKER: " + server)
    print("TOPIC: " + topic)

    # this API call will change based on the actual Kafka broker 
    #PRODUCER
    print("\n**Starting Producer**")
    producer=KafkaProducer(bootstrap_servers=[server],
    #                        security_protocol='SASL_PLAINTEXT',
    #                        sasl_mechanism='PLAIN',
    #                        sasl_plain_username='mapr',
    #                        sasl_plain_password='mapr'
                          )

    numMsgProduced = 0
    fake = Faker()
    for h in range(100):
        record = {
            "id": h+random.randint(1,100000),
            "name": fake.name(),
            "address": fake.address(),
            "amount": random.randint(1,1000000)
        }
        print(record)
        producer.send(topic, json.dumps(record).encode('utf-8'))
        numMsgProduced += 1
    producer.flush()
    print("Messages produced: " + str(numMsgProduced))
    time.sleep(2)                      

# define DAG
with DAG(
    dag_id="python_kafka_record_producer",
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "start_date": days_ago(1),
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "max_active_runs": 1,
        "retries": 0,
    },
    schedule_interval=None,
    tags=["Python", "Kafka", "Producer"],
    access_control={"All": {"can_read", "can_edit", "can_delete"}},
) as dag:

    virtualenv_task = PythonVirtualenvOperator(
        task_id="virtualenv_python_kafka_producer",
        python_callable=generate_kafka_records,
        requirements=["kafka-python==2.0.2","Faker==28.0.0"],
        system_site_packages=False,
    )

    virtualenv_task

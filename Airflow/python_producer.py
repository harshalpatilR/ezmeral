from airflow import DAG
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator
from airflow.utils.dates import days_ago
import subprocess
import venv
import os

def create_virtualenv(venv_path):
    """Creates a virtual environment if it doesn't exist."""
    if not os.path.exists(venv_path):
        #venv.create(venv_path, clear=True)
        subprocess.run(["python", "-m", "venv", venv_path], capture_output=True, shell=True, check=True)
        print(f"Virtual environment created at {venv_path}")

def activate_virtualenv(venv_path):
    """Activates the specified virtual environment."""
    activate_script = venv_path + "/bin" + "/activate"
    output = subprocess.run(["source", str(activate_script)], shell=True, check=False)
    print(output)
    print(f"Virtual environment activated at {venv_path}")

def deactivate_virtualenv():
    """Deactivates the currently active virtual environment."""
    subprocess.run(["deactivate"], shell=True, check=True)
    print("Virtual environment deactivated")    

def install_packages(venv_path, requirements_file):
    """Installs Python packages from a requirements.txt file within the activated virtual environment."""
    activate_script = venv_path + "/bin" + "/activate"
    subprocess.run([str(activate_script)], shell=True, check=True)
    subprocess.run([venv_path + "/bin" + "/pip", "install", "-r", requirements_file], check=True)
    print(f"Packages from {requirements_file} installed successfully in {venv_path}")    

def run_python_script(script_path):
    """Runs the specified Python script within the activated virtual environment."""
    subprocess.run(["python", script_path], check=True)
    print(f"Python script {script_path} executed successfully")



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





#dag_venv_path = "/mnt/shared/shared/airflow/pyenv1"
#dag_code_path = "/mnt/shared/airflow-jobs/pytest.py"
#dag_req_path = "/mnt/shared/airflow-jobs/req1.txt"

with DAG(
    dag_id="virtualenv_and_python_script",
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



    # create_venv = PythonOperator(
    #     task_id="create_venv",
    #     python_callable=create_virtualenv,
    #     op_kwargs={'venv_path': dag_venv_path}
    # )

    # activate_venv = PythonOperator(
    #     task_id="activate_venv",
    #     python_callable=activate_virtualenv,
    #     op_kwargs={'venv_path': dag_venv_path},
    #     trigger_rule="all_success"
    # )

    # install_packages = PythonOperator(
    #     task_id="install_packages",
    #     python_callable=install_packages,
    #     op_kwargs={'venv_path': dag_venv_path, 'requirements_file': dag_req_path}
    # )

    # run_script = PythonOperator(
    #     task_id="run_script",
    #     python_callable=run_python_script,
    #     op_kwargs={'script_path': dag_code_path},
    #     trigger_rule="all_success"
    # )

    # deactivate_venv = PythonOperator(
    #     task_id="deactivate_venv",
    #     python_callable=deactivate_virtualenv,
    #     trigger_rule="all_success"
    # )


    # create_venv >> install_packages >> activate_venv >> run_script >> deactivate_venv
    virtualenv_task

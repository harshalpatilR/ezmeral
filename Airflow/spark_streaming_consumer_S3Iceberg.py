from airflow import DAG
from airflow.models.param import Param
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import (
    SparkKubernetesOperator,
)
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import (
    SparkKubernetesSensor,
)
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "max_active_runs": 1,
    "retries": 0,
}

dag = DAG(
    "spark_stream_consumer_s3iceberg",
    default_args=default_args,
    schedule_interval=None,
    tags=["Streaming", "Kafka", "Iceberg"],
    params={
        "spark_image_url": Param(
            "gcr.io/mapr-252711/apache-spark:3.5.1-py",
            type=["null", "string"],
            description="Provide Python-Spark image url",
        ),

        "spark_image_version": Param(
            "3.5.1",
            type=["null", "string"],
            description="Provide Spark image Version",
        ),

        "s3_endpoint": Param(
            "https://IP:port",
            type=["null", "string"],
            description="S3 endpoint for storage",
        ),


        "s3_access_key": Param(
            "xxxxxxx",
            type=["null", "string"],
            description="S3 access key for storage",
        ),


        "s3_secret_key": Param(
            "xxxxxxx",
            type=["null", "string"],
            description="S3 secret key for storage",
        ),

        "app_file": Param(
            "local:///mounts/shared-volume/shared/airflow-jobs/Spark_K8s_Consumer_S3iceberg.py",
            type=["null", "string"],
            description="Application Python file",
        )

    },
    render_template_as_native_obj=True,
    access_control={"All": {"can_read", "can_edit", "can_delete"}},
)

submit = SparkKubernetesOperator(
    task_id="submit",
    application_file="spark_streaming_consumer_S3iceberg.yaml",
    # do_xcom_push=True,
    delete_on_termination=False,
    dag=dag,
    enable_impersonation_from_ldap_user=True,
)

# sensor = SparkKubernetesSensor(
#     task_id="monitor",
#     application_name="{{ task_instance.xcom_pull(task_ids='submit')['metadata']['name'] }}",
#     dag=dag,
#     attach_log=True,
# )

# submit >> sensor

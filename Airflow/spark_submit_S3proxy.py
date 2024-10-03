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
    "spark_submit_S3proxy",
    default_args=default_args,
    schedule_interval=None,
    tags=["Spark", "Submit", "S3 Proxy"],
    params={
        "spark_image_url": Param(
            "gcr.io/mapr-252711/spark-py-3.5.1:v3.5.1.0.1",
            type=["string"],
            description="Provide Python-Spark image url",
        ),

        "spark_image_version": Param(
            "3.5.1",
            type=["string"],
            description="Provide Spark image Version",
        ),

        "s3_endpoint": Param(
            "http://harshaledf-service.ezdata-system.svc.cluster.local:30000",
            type=["string"],
            description="S3 Proxy endpoint in UA for storage",
        ),

        "app_file": Param(
            "local:///mounts/shared-volume/shared/airflow-jobs/Spark_K8s_Consumer_S3iceberg-SchemaEvol.py",
            type=["string"],
            description="Application Python file",
        ),


        "yaml_file": Param(
            "spark_submit_S3Proxy.yaml",
            type=["string"],
            description="Spark yaml file which can be local:///mounts/shared-volume/shared/airflow-jobs/x.yaml",
        ),
       

    },
    render_template_as_native_obj=True,
    access_control={"All": {"can_read", "can_edit", "can_delete"}},
)

submit = SparkKubernetesOperator(
    task_id="submit",
    application_file=dag.params["yaml_file"],
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

submit

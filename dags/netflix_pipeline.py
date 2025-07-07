from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="netflix_pipeline",
    start_date=datetime(2025, 7, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    ingest = BashOperator(
        task_id="ingest",
        bash_command="cd /path/to/Projet_netflix && python src/ingestion.py"
    )

    clean = BashOperator(
        task_id="clean",
        bash_command="cd /path/to/Projet_netflix && python src/cleaning.py"
    )

    enrich = BashOperator(
        task_id="enrich",
        bash_command="cd /path/to/Projet_netflix && python src/enrichment.py"
    )

    ingest >> clean >> enrich

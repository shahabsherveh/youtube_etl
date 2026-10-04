from datetime import datetime, timedelta
from os import wait
import pendulum
from airflow import DAG
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator

# Import tasks needed to fetch the data from youtube
from api.video_stats import get_playlist_id, get_video_ids, get_video_stats, save_to_json, get_youtube_session

# Import tasks needed for updating database
from datawarehouse.dwh import staging_table, core_table

# Import tasks needed for quality checks
from dataquality.soda import yt_elt_data_quality

# Define the local timezone
local_tz = pendulum.timezone("Iran")

# Default Args

default_args = {
    "owner": "dataengineers",
    "depends_on_past": False,
    "retries": 1,
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2026, 10, 2, tzinfo=local_tz),
}

with DAG(
        dag_id='produce_json',
        default_args=default_args,
        description="DAG to produce json from the raw data",
        schedule="0 14 * * *",
        catchup=False,
) as dag_extract:
    # Define tasks
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    data = get_video_stats(video_ids)
    save_to_json_task = save_to_json(data)
    trigger_load = TriggerDagRunOperator(
        task_id='trigger_load',
        trigger_dag_id="update_db",
    )

    # Dependencies
    playlist_id >> video_ids >> data >> save_to_json_task >> trigger_load

    # DAG 2: update_db
with DAG(
    dag_id="update_db",
    default_args=default_args,
    description="DAG to process JSON file and insert data into both staging and core schemas",
    catchup=False,
    schedule=None,
) as dag_update:

    # Define tasks
    update_staging = staging_table()
    update_core = core_table()
    trigger_quality_check = TriggerDagRunOperator(
        task_id="trigger_quality_check",
        trigger_dag_id="quality_check",
    )

    # Define dependencies
    update_staging >> update_core >> trigger_quality_check

with DAG(
    dag_id="quality_check",
    default_args=default_args,
    description="Checks quality for both staging and core schemas in ELT DB",
    catchup=False,
    schedule=None,
) as dag_update:

    # Define tasks

    soda_validating_staging = yt_elt_data_quality('staging')
    soda_validating_core = yt_elt_data_quality('core')

    # Tasks dependencies
    soda_validating_staging >> soda_validating_core

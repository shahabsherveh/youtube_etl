from airflow import DAG
import pendulum
from datetime import datetime, timedelta

from api.video_stats import get_playlist_id, get_video_ids, get_video_stats, save_to_json, get_youtube_session

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
) as dag:
    # Define tasks
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    data = get_video_stats(video_ids)
    save_to_json_task = save_to_json(data)

    # Dependencies
    playlist_id >> video_ids >> data >> save_to_json_task

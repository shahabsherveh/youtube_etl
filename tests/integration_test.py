import psycopg2
import requests
import pytest


def test_youtube_api_respones(airflow_variable):
    api_key = airflow_variable("youtube_api_key")
    channel_handle = airflow_variable("youtube_channel_handle")

    url = f'https://youtube.googleapis.com/youtube/v3/channels?part=id&forHandle={channel_handle}&key={api_key}'

    try:
        response = requests.get(url=url)
        assert response.status_code == 200
    except requests.RequestException as e:
        pytest.fail(f"Request to Youtube api failed: {e}")


def test_real_postgres_connection(real_postgres_connection):
    try:
        cursor = real_postgres_connection.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()

        assert result[0] == 1
    except psycopg2.Error as e:
        pytest.fail(f"Database query failed: {e}")

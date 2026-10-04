import os
import pytest
from unittest import mock
from airflow.sdk import Variable, Connection
from airflow.dag_processing.dagbag import DagBag
import psycopg2


@pytest.fixture
def youtube_api_key():
    with mock.patch.dict("os.environ", AIRFLOW_VAR_YOUTUBE_API_KEY="MOCK_KEY1234"):
        yield Variable.get('YOUTUBE_API_KEY')


@pytest.fixture
def youtube_channel_handle():
    with mock.patch.dict("os.environ", AIRFLOW_VAR_YOUTUBE_CHANNEL_HANDLE="MrCheese"):
        yield Variable.get('YOUTUBE_CHANNEL_HANDLE')


@pytest.fixture
def mock_postgres_conn_vars():
    conn = Connection(
        conn_id="POSTGRES_DB_YT_ELT",
        login="mock_user",
        password="mock_password",
        host="mock_host",
        port=1234,
        schema="mock_db_name",
    )
    conn_uri = conn.get_uri()

    with mock.patch.dict("os.environ", AIRFLOW_CONN_POSTGRES_DB_YT_ELT=conn_uri):
        yield conn


@pytest.fixture
def dagbag():
    yield DagBag()


@pytest.fixture
def airflow_variable():
    def get_airflow_variable(variable_name):
        env_var = f"AIRFLOW_VAR_{variable_name.upper()}"
        return os.getenv(env_var)
    return get_airflow_variable


@pytest.fixture
def real_postgres_connection():
    dbname = os.getenv("ELT_DATABASE_NAME")
    user = os.getenv("ELT_DATABASE_USERNAME")
    password = os.getenv("ELT_DATABASE_PASSWORD")
    host = os.getenv("POSTGRES_CONN_HOST")
    port = os.getenv("POSTGRES_CONN_PORT")
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

        yield conn
    except psycopg2.Error as e:
        pytest.fail(f"Failed to connect to database: {e}")
    finally:
        if conn:
            conn.close()

import logging

from airflow.providers.standard.operators.bash import BashOperator

logger = logging.getLogger(__name__)

SODA_PATH = "/opt/airflow/include/soda"
DATASOURCE = "pg_datasource"


def yt_elt_data_quality(schema):
    try:
        task = BashOperator(
            task_id=f"soda_test_{schema}",
            bash_command=f"soda scan -c {SODA_PATH}/configuration.yml -d {DATASOURCE} -v SCHEMA={schema} {SODA_PATH}/checks.yml"
        )
        return task
    except Exception as e:
        logger.error(
            "Error for running quality checks for schema:{}".format(schema))
        raise e

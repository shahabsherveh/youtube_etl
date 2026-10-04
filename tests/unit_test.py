def test_youtube_api_key(youtube_api_key):
    assert youtube_api_key == "MOCK_KEY1234"


def test_youtube_channel_handle(youtube_channel_handle):
    assert youtube_channel_handle == "MrCheese"


def test_postgres_conn(mock_postgres_conn_vars):
    conn = mock_postgres_conn_vars

    assert conn.login == "mock_user"
    assert conn.password == "mock_password"
    assert conn.host == "mock_host"
    assert conn.port == 1234
    assert conn.schema == "mock_db_name"


def test_dag_integrity(dagbag):
    # 1.
    assert dagbag.import_errors == {}, f"Import errors found: {dagbag.import_errors}"
    print("===============")
    print(dagbag.import_errors)

    # 2.
    expected_dag_ids = {"produce_json", "update_db", "quality_check"}
    loaded_dag_ids = set(dagbag.dags.keys())
    assert expected_dag_ids == loaded_dag_ids

    # 3.
    assert dagbag.size() == 3
    print("===========")
    print(dagbag.size())

    # 4.
    expected_task_counts = {
        "produce_json": 5,
        "update_db": 3,
        "quality_check": 2,
    }
    print("===========")
    for dag_id, dag in dagbag.dags.items():
        expected_count = expected_task_counts[dag_id]
        actual_count = len(dag.tasks)
        assert (
            expected_count == actual_count
        ), f"DAG {dag_id} has {actual_count} tasks, expected {expected_count}."
        print(dag_id, len(dag.tasks))

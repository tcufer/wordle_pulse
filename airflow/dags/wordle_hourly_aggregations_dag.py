from airflow import DAG
from datetime import datetime
from airflow.operators.postgres_operator import PostgresOperator

POSTGRES_CONN_ID = "wordle_pulse_db"
TMPL_SEARCH_PATH = "dags/sql/"

dag = DAG(
    "wordle_hourly_aggregations_dag",
    template_searchpath=[TMPL_SEARCH_PATH],
    schedule_interval="0 * * * *",
    start_date=datetime(2022, 4, 6),
    catchup=True)

add_hourly_aggregations = PostgresOperator(
    task_id="add_hourly_aggregations",
    dag=dag,
    postgres_conn_id=POSTGRES_CONN_ID,
    sql="wordle_results_hourly.sql"
)

add_hourly_aggregations_most_common_results = PostgresOperator(
    task_id="add_hourly_aggregations_most_common_results",
    dag=dag,
    postgres_conn_id=POSTGRES_CONN_ID,
    sql="wordle_most_common_results_hourly.sql"
)

add_hourly_results_distribution = PostgresOperator(
    task_id="add_hourly_results_distribution",
    dag=dag,
    postgres_conn_id=POSTGRES_CONN_ID,
    sql="wordle_results_distribution_hourly.sql"
)

add_hourly_aggregations >> add_hourly_aggregations_most_common_results >> add_hourly_results_distribution

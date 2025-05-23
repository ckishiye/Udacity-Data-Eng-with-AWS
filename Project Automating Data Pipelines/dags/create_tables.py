import pendulum
from datetime import timedelta

from airflow.decorators import dag
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'akemi',
    'start_date': pendulum.now(),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
}


@dag(
    default_args=default_args,
    description='Create tables in Redshift with Airflow',
    schedule_interval='@hourly'
)
def create_tables():
    start_operator = DummyOperator(task_id='Begin_execution')

    create_redshift_tables = PostgresOperator(
        task_id='Create_tables',
        postgres_conn_id='redshift',
        sql='create_tables.sql'
    )

    end_operator = DummyOperator(task_id='Stop_execution')

    start_operator >> create_redshift_tables >> end_operator


create_tables_dag = create_tables()
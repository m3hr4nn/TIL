# Apache Airflow Interview Cheat Sheet

## Core Concepts

**DAG**: Directed Acyclic Graph - workflow definition
**Task**: Single unit of work in a DAG
**Operator**: Template for a task (PythonOperator, BashOperator, etc.)
**Executor**: Component that runs tasks (LocalExecutor, CeleryExecutor, Kubernetes)
**Scheduler**: Monitors DAGs and triggers task instances
**Worker**: Process that executes tasks
**Webserver**: UI for monitoring and managing workflows
**XCom**: Cross-communication between tasks

## Architecture

```
Scheduler → Executor → Workers
    ↓
Metadata DB (PostgreSQL/MySQL)
    ↑
Webserver (UI)
```

## Basic DAG Structure

### Simple DAG
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Default arguments
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email': ['team@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'example_dag',
    default_args=default_args,
    description='A simple example DAG',
    schedule_interval='@daily',
    catchup=False,
    tags=['example'],
)

# Tasks
task1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

def print_hello():
    print("Hello World!")
    return "success"

task2 = PythonOperator(
    task_id='hello_world',
    python_callable=print_hello,
    dag=dag,
)

# Task dependencies
task1 >> task2  # task1 runs before task2
```

### Modern DAG Syntax (TaskFlow API)
```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id='modern_example_dag',
    start_date=datetime(2025, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['modern'],
)
def my_dag():
    
    @task()
    def extract():
        return {'data': [1, 2, 3, 4, 5]}
    
    @task()
    def transform(data: dict):
        values = data['data']
        transformed = [x * 2 for x in values]
        return {'transformed': transformed}
    
    @task()
    def load(data: dict):
        print(f"Loading: {data['transformed']}")
    
    # Define workflow
    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)

# Instantiate DAG
dag_instance = my_dag()
```

## Common Operators

### BashOperator
```python
from airflow.operators.bash import BashOperator

run_script = BashOperator(
    task_id='run_script',
    bash_command='bash /path/to/script.sh',
    env={'ENV_VAR': 'value'},
)
```

### PythonOperator
```python
from airflow.operators.python import PythonOperator

def my_function(name, **context):
    print(f"Hello {name}")
    execution_date = context['execution_date']
    return f"Executed on {execution_date}"

python_task = PythonOperator(
    task_id='python_task',
    python_callable=my_function,
    op_kwargs={'name': 'World'},
    provide_context=True,
)
```

### EmailOperator
```python
from airflow.operators.email import EmailOperator

send_email = EmailOperator(
    task_id='send_email',
    to='recipient@example.com',
    subject='DAG completed',
    html_content='<h3>Job finished successfully</h3>',
)
```

### SqlOperator
```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

create_table = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='postgres_default',
    sql='''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            created_at TIMESTAMP DEFAULT NOW()
        );
    ''',
)
```

### HTTPOperator
```python
from airflow.providers.http.operators.http import SimpleHttpOperator

api_call = SimpleHttpOperator(
    task_id='call_api',
    http_conn_id='http_default',
    endpoint='/api/endpoint',
    method='POST',
    data=json.dumps({'key': 'value'}),
    headers={'Content-Type': 'application/json'},
)
```

### PythonVirtualenvOperator
```python
from airflow.operators.python import PythonVirtualenvOperator

virtualenv_task = PythonVirtualenvOperator(
    task_id='virtualenv_task',
    python_callable=my_function,
    requirements=['pandas==1.3.0', 'requests'],
    system_site_packages=False,
)
```

## Task Dependencies

### Basic Dependencies
```python
# Sequential
task1 >> task2 >> task3

# Parallel then converge
task1 >> [task2, task3] >> task4

# Cross dependencies
task1 >> task2
task1 >> task3
task2 >> task4
task3 >> task4

# Using set_upstream/set_downstream
task2.set_upstream(task1)
task3.set_downstream(task4)
```

### Branching
```python
from airflow.operators.python import BranchPythonOperator

def choose_branch(**context):
    if context['execution_date'].weekday() < 5:
        return 'weekday_task'
    else:
        return 'weekend_task'

branch = BranchPythonOperator(
    task_id='branch_task',
    python_callable=choose_branch,
)

weekday_task = BashOperator(
    task_id='weekday_task',
    bash_command='echo "Weekday"',
)

weekend_task = BashOperator(
    task_id='weekend_task',
    bash_command='echo "Weekend"',
)

branch >> [weekday_task, weekend_task]
```

### Trigger Rules
```python
from airflow.utils.trigger_rule import TriggerRule

task = BashOperator(
    task_id='final_task',
    bash_command='echo "Done"',
    trigger_rule=TriggerRule.ALL_SUCCESS,  # Default
)

# Trigger rules:
# ALL_SUCCESS - all parents succeeded (default)
# ALL_FAILED - all parents failed
# ALL_DONE - all parents completed
# ONE_SUCCESS - at least one parent succeeded
# ONE_FAILED - at least one parent failed
# NONE_FAILED - no parent failed (some may be skipped)
# NONE_SKIPPED - no parent skipped
```

## XCom (Cross-Communication)

### Push and Pull XCom
```python
def push_function(**context):
    context['task_instance'].xcom_push(key='my_key', value='my_value')
    return 'This also gets pushed with key "return_value"'

def pull_function(**context):
    ti = context['task_instance']
    value = ti.xcom_pull(task_ids='push_task', key='my_key')
    return_value = ti.xcom_pull(task_ids='push_task')
    print(f"Pulled: {value}, {return_value}")

push_task = PythonOperator(
    task_id='push_task',
    python_callable=push_function,
)

pull_task = PythonOperator(
    task_id='pull_task',
    python_callable=pull_function,
)

push_task >> pull_task
```

### TaskFlow API XCom
```python
@task()
def extract():
    return {'data': [1, 2, 3]}

@task()
def process(data):
    # data is automatically pulled from XCom
    return [x * 2 for x in data['data']]

result = extract()
processed = process(result)
```

## Sensors

### FileSensor
```python
from airflow.sensors.filesystem import FileSensor

wait_for_file = FileSensor(
    task_id='wait_for_file',
    filepath='/path/to/file.txt',
    poke_interval=30,  # Check every 30 seconds
    timeout=600,  # Timeout after 10 minutes
)
```

### TimeDeltaSensor
```python
from airflow.sensors.time_delta import TimeDeltaSensor
from datetime import timedelta

wait = TimeDeltaSensor(
    task_id='wait_5_minutes',
    delta=timedelta(minutes=5),
)
```

### ExternalTaskSensor
```python
from airflow.sensors.external_task import ExternalTaskSensor

wait_for_other_dag = ExternalTaskSensor(
    task_id='wait_for_dag',
    external_dag_id='other_dag',
    external_task_id='other_task',
    timeout=600,
)
```

### HttpSensor
```python
from airflow.providers.http.sensors.http import HttpSensor

wait_for_api = HttpSensor(
    task_id='wait_for_api',
    http_conn_id='http_default',
    endpoint='/health',
    response_check=lambda response: response.status_code == 200,
)
```

## Connections

### Create via CLI
```bash
airflow connections add 'my_postgres' \
    --conn-type 'postgres' \
    --conn-host 'localhost' \
    --conn-schema 'mydb' \
    --conn-login 'user' \
    --conn-password 'password' \
    --conn-port 5432
```

### Use in Code
```python
from airflow.hooks.postgres_hook import PostgresHook

def query_database():
    hook = PostgresHook(postgres_conn_id='my_postgres')
    records = hook.get_records('SELECT * FROM users')
    return records
```

### Environment Variable
```bash
export AIRFLOW_CONN_MY_POSTGRES='postgresql://user:password@localhost:5432/mydb'
```

## Variables

### Set Variables
```bash
# Via CLI
airflow variables set my_var my_value
airflow variables set config '{"key": "value"}' --json

# Via UI: Admin -> Variables
```

### Use in DAG
```python
from airflow.models import Variable

# Get variable
my_var = Variable.get('my_var')
config = Variable.get('config', deserialize_json=True)

# Set variable
Variable.set('new_var', 'new_value')

# Use in template
task = BashOperator(
    task_id='use_var',
    bash_command='echo {{ var.value.my_var }}',
)
```

## Scheduling

### Schedule Intervals
```python
# Cron expression
schedule_interval='0 12 * * *'  # Daily at noon

# Preset schedules
schedule_interval='@daily'      # Midnight
schedule_interval='@hourly'     # Top of hour
schedule_interval='@weekly'     # Sunday midnight
schedule_interval='@monthly'    # First of month
schedule_interval='@yearly'     # January 1st

# Timedelta
schedule_interval=timedelta(hours=2)

# No schedule (manual only)
schedule_interval=None
```

### Catchup
```python
# Run all past schedules
dag = DAG(
    'my_dag',
    start_date=datetime(2024, 1, 1),
    catchup=True,  # Will backfill from start_date
)

# Skip past schedules
dag = DAG(
    'my_dag',
    start_date=datetime(2024, 1, 1),
    catchup=False,  # Only run current schedule
)
```

## Jinja Templating

### Context Variables
```python
task = BashOperator(
    task_id='templated_task',
    bash_command='''
        echo "Execution date: {{ ds }}"
        echo "DAG ID: {{ dag.dag_id }}"
        echo "Task ID: {{ task.task_id }}"
        echo "Run ID: {{ run_id }}"
    ''',
)

# Common templates:
# {{ ds }}                  # Execution date (YYYY-MM-DD)
# {{ ds_nodash }}           # YYYYMMDD
# {{ ts }}                  # Timestamp (ISO 8601)
# {{ dag }}                 # DAG object
# {{ task }}                # Task object
# {{ task_instance }}       # TaskInstance object
# {{ execution_date }}      # Execution datetime
# {{ prev_execution_date }} # Previous execution
# {{ next_execution_date }} # Next execution
# {{ var.value.my_var }}    # Airflow variable
# {{ params.my_param }}     # Custom params
```

### Custom Parameters
```python
task = BashOperator(
    task_id='param_task',
    bash_command='echo {{ params.name }}',
    params={'name': 'World'},
)
```

## CLI Commands

### DAG Management
```bash
# List DAGs
airflow dags list

# Trigger DAG
airflow dags trigger my_dag
airflow dags trigger my_dag --conf '{"key":"value"}'

# Pause/Unpause DAG
airflow dags pause my_dag
airflow dags unpause my_dag

# Test DAG
airflow dags test my_dag 2025-01-01

# Backfill
airflow dags backfill my_dag \
    --start-date 2025-01-01 \
    --end-date 2025-01-31
```

### Task Management
```bash
# List tasks
airflow tasks list my_dag

# Test task
airflow tasks test my_dag task_id 2025-01-01

# Clear task
airflow tasks clear my_dag --task-regex task_id

# Task state
airflow tasks state my_dag task_id 2025-01-01
```

### Database
```bash
# Initialize database
airflow db init

# Upgrade database
airflow db upgrade

# Reset database
airflow db reset
```

### Users
```bash
# Create user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

## Configuration

### airflow.cfg
```ini
[core]
dags_folder = /path/to/dags
executor = LocalExecutor
parallelism = 32
max_active_runs_per_dag = 16

[webserver]
base_url = http://localhost:8080
web_server_port = 8080

[scheduler]
scheduler_heartbeat_sec = 5
max_threads = 2

[email]
email_backend = airflow.utils.email.send_email_smtp

[smtp]
smtp_host = smtp.gmail.com
smtp_port = 587
smtp_user = your-email@gmail.com
smtp_password = your-password
smtp_mail_from = airflow@example.com
```

## Best Practices

### Idempotency
```python
# BAD: Not idempotent
INSERT INTO table VALUES (1, 'data')

# GOOD: Idempotent
INSERT INTO table VALUES (1, 'data')
ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data
```

### Task Design
```python
# Keep tasks atomic and focused
# BAD: One task does everything
def monolithic_task():
    extract_data()
    transform_data()
    load_data()

# GOOD: Separate tasks
@task()
def extract(): ...

@task()
def transform(): ...

@task()
def load(): ...
```

### Dynamic DAGs
```python
# Generate tasks dynamically
for i in range(10):
    task = BashOperator(
        task_id=f'task_{i}',
        bash_command=f'echo "Task {i}"',
    )
```

## Common Interview Questions

**Q: What is Apache Airflow?**
- Workflow orchestration platform
- Python-based DAG definition
- Schedules and monitors data pipelines
- Rich UI for management

**Q: Explain DAG**
- Directed Acyclic Graph
- Defines workflow structure
- No cycles allowed
- Python code that defines tasks and dependencies

**Q: What are Executors?**
- SequentialExecutor: Single-threaded (dev only)
- LocalExecutor: Multi-threaded on single machine
- CeleryExecutor: Distributed, uses Celery
- KubernetesExecutor: Each task in K8s pod

**Q: Difference between Operator and Sensor?**
- Operator: Performs an action
- Sensor: Waits for condition to be met
- Sensor polls until condition is true

**Q: What is XCom?**
- Cross-communication between tasks
- Stores small amounts of data in metadata DB
- push/pull mechanism
- Not for large data transfer

**Q: Explain schedule_interval**
- Cron expression or timedelta
- Determines how often DAG runs
- None = manual trigger only
- Use catchup for historical runs

**Q: What is execution_date?**
- Start of the schedule interval
- Not the actual run time
- Used for data partitioning
- Can be confusing initially

**Q: How to pass data between tasks?**
- XCom for small data
- External storage (S3, DB) for large data
- TaskFlow API simplifies XCom usage

**Q: What are Hooks?**
- Interface to external systems
- Reusable connection logic
- PostgresHook, S3Hook, etc.
- Used by Operators internally

**Q: Difference between start_date and execution_date?**
- start_date: When DAG should start scheduling
- execution_date: Logical date of the data interval
- First run is at start_date + schedule_interval

**Q: How to handle failures?**
- retries parameter
- retry_delay
- on_failure_callback
- email_on_failure
- depends_on_past

**Q: What is catchup?**
- Backfills missed runs
- If False, skips historical runs
- If True, runs all schedules since start_date

**Q: Explain trigger rules**
- Control when tasks run
- ALL_SUCCESS (default)
- Useful for cleanup tasks (ALL_DONE)
- Branching scenarios

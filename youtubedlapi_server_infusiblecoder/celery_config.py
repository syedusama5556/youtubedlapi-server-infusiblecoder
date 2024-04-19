# celery_config.py
broker_url = 'redis://localhost:6379/0'  # Redis running on the local machine, database 0
result_backend = 'redis://localhost:6379/0'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/London'
enable_utc = True

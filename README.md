# celery_demo

Toy project to play with celery and rabbitmq

## Run flower

```bash
celery flower -A celery_demo --broker-api=http://guest:guest@localhost:15672/api/
```

## Run celery worker

```bash
celery -A celery_demo worker -l info -Q finish_parking,celery,parking_report
```

## Run celery beat

```bash
celery -A celery_demo beat -l info --scheduler django_celery_beat
```

import json

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Parking(BaseModel):
    plate = models.CharField(max_length=6)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)


class Report(BaseModel):
    data = JSONField()


@receiver(post_save, sender=Parking)
def schedule_parking_finish(instance, *_, **__):
    end_at = instance.end_at
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=end_at.minute,
        hour=end_at.hour,
        day_of_week="*",
        day_of_month=end_at.day,
        month_of_year=end_at.month,
    )
    defaults = {
        "crontab": schedule,
        "enabled": True,
        "task": "parking.tasks.finish_parking",
        "kwargs": json.dumps({"parking_id": instance.id}),
        "one_off": True,
    }

    PeriodicTask.objects.update_or_create(
        name=f"Finish parking for {instance.plate}", defaults=defaults,
    )


@receiver(post_save, sender=PeriodicTask)
def inject_periodic_task_id_on_kwargs(instance, *_, **__):
    kwargs = json.loads(instance.kwargs)
    if "periodic_task_id" not in kwargs:
        kwargs["periodic_task_id"] = instance.id
        instance.kwargs = json.dumps(kwargs)
        instance.save()

from __future__ import absolute_import

from celery import shared_task
from django.core import serializers
from django.utils import timezone

from .models import Parking, Report


@shared_task(queue="finish_parking")
def finish_parking(parking_id: int, *_args, **_kwargs):
    ended_at = timezone.now()
    Parking.objects.filter(id=parking_id).update(ended_at=ended_at)
    return {"ended_at": ended_at}


@shared_task(queue="parking_report")
def parking_report(*_args, **_kwargs):
    qs = Parking.objects.all()
    data = serializers.serialize("json", qs)
    Report.objects.create(data=data)
    return {"created_on": timezone.now().isoformat(), "records_processed": qs.count()}

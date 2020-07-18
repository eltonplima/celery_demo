from django.contrib import admin

from .models import Parking, Report


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    fields = ("plate", "start_at", "end_at")
    list_display = ("plate", "start_at", "end_at", "finished")

    def finished(self, obj):
        return obj.ended_at is not None

    finished.boolean = True


admin.site.register(Report)

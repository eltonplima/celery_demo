from django.contrib import admin

from .models import Parking, Report


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ("plate", "start_at", "end_at", "finished")
    readonly_fields = ("ended_at",)

    def finished(self, obj):
        return obj.ended_at is not None

    finished.boolean = True


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ("data", "created_at", "updated_at")
    list_display = ("created_at", "updated_at")

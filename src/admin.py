from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location_country", "job_type", "posted_at", "scraped_at")
    list_filter = ("location_country", "job_type", "posted_at")
    search_fields = ("title", "company", "location_country", "job_type")
    ordering = ("-posted_at",)
    readonly_fields = ("scraped_at",)

    def view_on_site(self, obj):
        return obj.url

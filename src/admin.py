from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "posted_at", "scraped_at")
    search_fields = ("title", "company", "url")
    ordering = ("-posted_at",)

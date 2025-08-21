from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    posted_at = models.DateTimeField()
    scraped_at = models.DateTimeField(auto_now_add=True)

    location_country = models.CharField(max_length=64, null=True, blank=True)
    job_type = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"{self.title} @ {self.company}"

from celery import shared_task
from django.core.management import call_command

@shared_task(bind=True, max_retries=3)
def scrape_jobs_task(self):

    try:
        call_command("scrape_jobs")
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)

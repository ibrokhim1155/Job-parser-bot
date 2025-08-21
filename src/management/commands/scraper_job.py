import json
from datetime import datetime, timezone
from django.core.management.base import BaseCommand
from django.conf import settings
import requests

from src.models import Job

REMOTIVE_URL = getattr(settings, "REMOTIVE_API", "https://remotive.com/api/remote-jobs?search=python")

class Command(BaseCommand):
    help = "Scrape jobs from public API and upsert into DB"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(f"Fetching: {REMOTIVE_URL}"))
        try:
            resp = requests.get(REMOTIVE_URL, timeout=25)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Request failed: {e}"))
            return

        jobs = data.get("jobs") or data.get("job-listings") or []
        created, updated = 0, 0

        for item in jobs:
            try:
                title = item.get("title") or "Untitled"
                company = item.get("company_name") or item.get("company") or "Unknown"
                url = item.get("url") or item.get("job_url")
                posted_raw = item.get("publication_date") or item.get("date") or item.get("created_at")

                if not url:
                    continue
                try:
                    posted_at = datetime.fromisoformat(posted_raw.replace("Z", "+00:00"))
                except Exception:
                    posted_at = datetime.now(timezone.utc)

                obj, is_created = Job.objects.update_or_create(
                    url=url,
                    defaults={
                        "title": title[:255],
                        "company": company[:255],
                        "posted_at": posted_at,
                    },
                )
                created += int(is_created)
                updated += int(not is_created)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Skip item error: {e}"))
                continue

        self.stdout.write(self.style.SUCCESS(f"Done. created={created}, updated={updated}"))

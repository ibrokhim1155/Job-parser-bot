from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import Job
from .serializers import JobSerializer

class JobViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Job.objects.order_by("-posted_at")
    serializer_class = JobSerializer
    permission_classes = [AllowAny]
    search_fields = ["title", "company"]
    ordering_fields = ["posted_at", "scraped_at", "title"]

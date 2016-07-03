from rest_framework import filters, viewsets

from .models import Monitoring
from .serializers import MonitoringSerializer


class MonitoringFilter(filters.FilterSet):
    class Meta:
        model = Monitoring
        fields = ['active', ]


class MonitoringViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (Monitoring.objects.
                prefetch_related('page_set').
                prefetch_related('institutions').
                prefetch_related('question_set').
                all())
    serializer_class = MonitoringSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = MonitoringFilter

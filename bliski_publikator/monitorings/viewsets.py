from rest_framework import filters, viewsets

from .models import Monitoring
from .serializers import MonitoringSerializer


class MonitoringFilter(filters.FilterSet):
    class Meta:
        model = Monitoring
        fields = ['active', 'institutions']


class MonitoringViewSet(viewsets.ModelViewSet):
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = MonitoringFilter

import django_filters
from rest_framework import filters, viewsets

from .models import Institution
from .serializers import InstitutionSerializer


class InstitutionFilter(filters.FilterSet):
    region = django_filters.CharFilter()

    class Meta:
        model = Institution
        fields = ['user', 'krs', 'regon']


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.prefetch_related('monitorings').all()
    serializer_class = InstitutionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = InstitutionFilter

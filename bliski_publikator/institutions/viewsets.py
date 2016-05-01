from rest_framework import filters, viewsets

from .models import Institution
from .serializers import InstitutionSerializer


class InstitutionFilter(filters.FilterSet):
    class Meta:
        model = Institution
        fields = ['region', 'user', 'krs', 'regon']


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = InstitutionFilter

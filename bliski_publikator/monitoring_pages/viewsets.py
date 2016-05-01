from rest_framework import filters, viewsets

from .models import Page
from .serializers import PageSerializer


class PageFilter(filters.FilterSet):
    class Meta:
        model = Page
        fields = ['monitoring', ]


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PageFilter

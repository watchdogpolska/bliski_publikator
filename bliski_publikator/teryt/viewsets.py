from rest_framework import filters, viewsets
from teryt_tree.models import Category, JednostkaAdministracyjna

from .models import JST
from .serializers import CategorySerializer, JSTSerializer


class JSTFilter(filters.FilterSet):
    class Meta:
        model = JST
        fields = ['name', 'category', 'category__level']


class JSTViewSet(viewsets.ModelViewSet):
    queryset = JST.objects.all()
    serializer_class = JSTSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = JSTFilter


class JednostkaAdministracyjnaViewSet(viewsets.ModelViewSet):
    queryset = JednostkaAdministracyjna.objects.all()
    serializer_class = JSTSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

from rest_framework import serializers

from .models import JST
from teryt_tree.models import Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ('name', )


class JSTSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    children = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='jst-detail'
    )

    class Meta:
        model = JST
        fields = ('url', 'parent', 'children', 'category', 'name', 'updated_on', 'active', 'level',)

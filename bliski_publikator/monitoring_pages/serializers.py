from rest_framework import serializers

from .models import Page


class PageSerializer(serializers.HyperlinkedModelSerializer):
    on_site = serializers.CharField(source='get_absolute_url', read_only=True)
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Page
        fields = ('on_site',
                  'url',
                  'slug',
                  'monitoring',
                  'title',
                  'content',
                  'ordering')

from rest_framework import serializers

from .models import Page


class PageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Page
        fields = ('url', 'monitoring', 'title', 'content', 'ordering')

from rest_framework import serializers

from .models import Monitoring


class MonitoringSerializer(serializers.HyperlinkedModelSerializer):
    on_site = serializers.CharField(source='get_absolute_url', read_only=True)
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Monitoring
        fields = ('on_site',
                  'slug',
                  'name',
                  'user',
                  'description',
                  'instruction',
                  'active',
                  'logo',
                  'institutions',
                  'page_set',
                  'question_set')

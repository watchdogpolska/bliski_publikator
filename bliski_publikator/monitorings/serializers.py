from rest_framework import serializers

from .models import Monitoring


class MonitoringSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Monitoring
        fields = ('name', 'user', 'description', 'active', 'logo', 'institutions', 'page_set')

from rest_framework import serializers

from .models import Institution


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = ('url', 'name', 'slug', 'user', 'email', 'region', 'regon', 'krs', 'monitorings')

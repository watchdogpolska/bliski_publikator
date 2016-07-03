from rest_framework import serializers

from .models import Institution


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    on_site = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Institution
        fields = ('on_site',
                  'url',
                  'name',
                  'slug',
                  'user',
                  'email',
                  'region',
                  'regon',
                  'krs',
                  'monitorings')
        extra_kwargs = {
            'region': {'view_name': 'jednostkaadministracyjna-detail'}
        }

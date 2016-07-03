from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    on_site = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('on_site', 'url', 'username', 'is_staff')

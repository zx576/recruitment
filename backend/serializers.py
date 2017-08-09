from rest_framework import serializers
from .models import Recruit, Firm, Proxy


class ProxySerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    head = serializers.CharField(required=True, max_length=255)
    addr = serializers.CharField(required=True, max_length=255)
    is_alive = serializers.BooleanField(required=False)
    is_http_and_https = serializers.BooleanField(required=False)

    def create(self, validated_data):

        return Proxy.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.head = validated_data.get('title', instance.head)
        instance.addr = validated_data.get('addr', instance.addr)
        instance.is_alive = validated_data.get('is_alive', instance.is_alive)
        instance.is_http_and_https = validated_data.get('is_http_and_https', instance.is_http_and_https)

        instance.save()
        return instance
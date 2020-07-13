from rest_framework import serializers
from .models import Nation


class NationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nation
        fields = ('id', 'name',)

    def create(self, validated_data):
        return Nation(**validated_data)

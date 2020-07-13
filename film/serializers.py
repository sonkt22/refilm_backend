from rest_framework import serializers
from .models import Film


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('id',
                  'name',
                  'title',
                  'producer_year',
                  'type',
                  'thumbnail',
                  'detail_picture',
                  'content',
                  'review_point',
                  'review_count'
                  )

    def create(self, validated_data):
        return Film(**validated_data)

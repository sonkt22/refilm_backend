from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id',
                  'user',
                  'name_film',
                  'title',
                  'like',
                  'dislike',
                  'content',
                  'comment_count'
                  )

    def create(self, validated_data):
        return Post(**validated_data)

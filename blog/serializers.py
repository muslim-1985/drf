from rest_framework import serializers
from .models import *


class UserSerializers(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'created_at', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title', 'slug')


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("title", "image", "created_at")


class PostSerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    tags = TagSerializers(many=True, read_only=True)
    category = CategorySerializers(read_only=True)

    class Meta:
        model = Post
        fields = ("title", "slug", "body", "created_at", "user", "tags", "category")

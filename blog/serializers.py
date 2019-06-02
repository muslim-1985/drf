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


class PostFileSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostFile
        fields = ("name", "path", "created_at")


class PostSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # UserSerializers(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())  # TagSerializers(many=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())  # CategorySerializers(read_only=True)
    files = PostFileSerializers(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("title", "slug", "body", "is_active", "created_at", "user", "tags", "category", "files")


class PostReturnSerializer(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    tags = TagSerializers(many=True)
    category = CategorySerializers(read_only=True)
    files = PostFileSerializers(many=True)

    class Meta:
        model = Post
        fields = ("title", "slug", "body", "is_active", "created_at", "user", "tags", "category", "files")


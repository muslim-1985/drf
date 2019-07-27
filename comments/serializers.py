from rest_framework import serializers
from users.serializers import UserSerializers
from rest_framework_recursive.fields import RecursiveField
from .models import *


class CommentReturnSerializer(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    # posts = PostSerializers(many=True)
    parent = RecursiveField(required=False, allow_null=True, many=True)

    class Meta:
        model = Comment
        fields = ("title", "body", "active", "created_at", "user", "parent",)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # posts = PostSerializers(many=True)
    parent = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ("title", "body", "active", "created_at", "user", "post", "parent",)


from rest_framework import serializers
from users.serializers import UserSerializers
from blog.serializers import PostSerializers
from rest_framework_recursive.fields import RecursiveField
from .models import *


class CommentReturnSerializer(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    # posts = PostSerializers(many=True)
    children = RecursiveField(required=False, allow_null=True, many=True)

    class Meta:
        model = Comment
        fields = ("title", "body", "active", "created_at", "user", "children",)

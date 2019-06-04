from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import parsers
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from blog.mixins.utils import ModelCreateFilesUpload
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.conf import settings
import os
from django.shortcuts import get_object_or_404

from blog.models import *
from blog.serializers import *


class Posts(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializers(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreatePost(APIView, ModelCreateFilesUpload):
    # IsAuthenticated
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser, parsers.FileUploadParser,)

    model = Post
    files_model = PostFile
    serializer = PostSerializers
    return_serializer = PostReturnSerializer
    instance_files_path = 'post'


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import parsers
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from blog.mixins.utils import ModelCreate
from rest_framework.generics import RetrieveUpdateDestroyAPIView
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.conf import settings
import os
from django.shortcuts import get_object_or_404

from blog.models import *
from blog.serializers import *


class Posts(APIView, ModelCreate):
    # IsAuthenticated
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser, parsers.FileUploadParser,)

    model = Post
    files_model = PostFile
    serializer = PostSerializers
    return_serializer = PostReturnSerializer


class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)
    serializer_class = PostSerializers

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.post)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data
        post = get_object_or_404(Post, id=kwargs.get('post'))

        serializer = PostSerializers(
            post, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


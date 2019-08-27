from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.settings import api_settings
from rest_framework import parsers
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from blog.mixins.utils import ModelCreate, ModelUpdate
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.conf import settings
import os
from django.shortcuts import get_object_or_404

from blog.models import *
from blog.serializers import *


class PostsList(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Post.objects.all()
    serializer_class = PostReturnSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'data': serializer.data})
        # Note the use of `get_queryset()` instead of `self.queryset`
        serializer = self.get_serializer(page, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class Posts(APIView, ModelCreate):
    # IsAuthenticated
    permission_classes = (permissions.IsAuthenticated,)  # (permissions.AllowAny,)
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser, parsers.FileUploadParser,)

    model = Post
    files_model = PostFile
    serializer = PostSerializers
    return_serializer = PostReturnSerializer


class PostRetrieveUpdateDestroyAPIView(ModelUpdate, RetrieveUpdateDestroyAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)
    serializer_class = PostSerializers

    model = Post
    files_model = PostFile
    serializer = PostSerializers
    return_serializer = PostReturnSerializer

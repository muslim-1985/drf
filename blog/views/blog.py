from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import parsers
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
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


class CreatePost(APIView):
    # IsAuthenticated
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser, parsers.FileUploadParser,)

    def post(self, request):
        data = request.data
        serializer = PostSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            files = request.FILES.getlist('files')
            post = Post.objects.latest('id')
            valid_extensions = ['.png', '.jpg', '.gif']
            for file in files:
                filename = default_storage.generate_filename(settings.MEDIA_ROOT + '/' + file.name)
                path = default_storage.save(filename, file)
                ext = os.path.splitext(path)[1]
                if not ext in valid_extensions:
                    raise ValidationError(u'File not supported!', code='invalid')
                try:
                    PostFile.objects.create(name=file.name, path=path, post=post)
                except ValueError:
                    return Response({'error': 'Value Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            serializer_post = PostReturnSerializer(instance=post)
            return Response({'data': serializer_post.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)

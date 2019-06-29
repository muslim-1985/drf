from rest_framework.response import Response
import os
from django.conf import settings
from django.core.files.storage import default_storage
import magic
from PIL import Image
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from blog.serializers import *
import os


class FilesUpload:
    valid_extensions = None
    files_model = None
    instance_files_path = None

    def __file_path_mime(self, file):
        mime = magic.from_buffer(file.read(1024), mime=True)
        return mime

    def files_upload(self, request, related_model):
        files = request.FILES.getlist('files')
        for file in files:
            try:
                self.files_model.objects.create(path=file, post=related_model)
            except ValueError:
                return Response({'error': 'Value Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ModelCreate(FilesUpload):
    model = None
    files_model = None
    serializer = None
    return_serializer = None

    def get(self, request):
        posts = self.model.objects.all()
        serializer = self.serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        # print(request.META.get('REMOTE_ADDR'))
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            related_model = self.model.objects.latest('id')
            if self.files_model:
                self.files_upload(request, related_model)
            serializer_post = self.return_serializer(instance=related_model)
            return Response({'data': serializer_post.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)


class ModelUpdate(FilesUpload):
    model = None
    files_model = None
    serializer = None
    return_serializer = None

    def get(self, request, *args, **kwargs):
        serializer = PostSerializers(request.post)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data
        post = get_object_or_404(self.model, id=kwargs.get('pk'))

        serializer = PostSerializers(
            post, data=serializer_data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            related_model = self.model.objects.latest('id')
            if self.files_model:
                self.files_upload(request, related_model)
            serializer_post = self.return_serializer(instance=related_model)
            return Response({'data': serializer_post.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(self.model, id=kwargs.get('pk'))
        for file in post.files.all():
            if os.path.isfile(file.full_path.name):
                os.remove(file.full_path.name)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

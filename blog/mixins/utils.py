from rest_framework.response import Response
from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image
from django.core.exceptions import ValidationError
from rest_framework import status
from blog.serializers import *
import os


class FilesUpload:
    valid_extensions = None
    files_model = None
    instance_files_path = None

    def files_upload(self, request, related_model):
        files = request.FILES.getlist('files')
        for file in files:
            filename = default_storage.generate_filename(settings.MEDIA_ROOT + '/user_' + str(
                related_model.user.id) + '/' + self.instance_files_path + '_' + str(related_model.id) + '/' + file.name)
            try:
                img = Image.open(file)
                img.verify()
                full_path = default_storage.save(filename, file)
                filename = full_path.split('/')[-1]
                path = '/user_' + str(
                    related_model.user.id) + '/' + self.instance_files_path + '_' + str(
                    related_model.id) + '/' + filename
            except:
                raise ParseError('Unsupported file type {file_type}'.format(file_type=file.name))
            try:
                self.files_model.objects.create(name=file.name, path=path, full_path=full_path, post=related_model)
            except ValueError:
                return Response({'error': 'Value Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ModelCreateFilesUpload(FilesUpload):
    model = None
    files_model = None
    serializer = None
    return_serializer = None
    instance_files_path = None

    def post(self, request):
        data = request.data
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            related_model = self.model.objects.latest('id')
            if self.files_model:
                self.files_upload(request, related_model)
            serializer_post = self.return_serializer(instance=related_model)
            return Response({'data': serializer_post.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)

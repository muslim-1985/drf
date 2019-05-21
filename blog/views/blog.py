from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import parsers
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
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser,)

    def post(self, request):
        data = request.data

        serializer = PostSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

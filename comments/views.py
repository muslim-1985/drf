from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import parsers
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from blog.mixins.utils import ModelCreate, ModelUpdate
from django.shortcuts import get_object_or_404
from comments.serializers import *
from .models import *


# Create your views here.

class Comments(APIView, ModelCreate):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentReturnSerializer(comments, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        # print(data.get('children'))
        # return Response({'data': 'hello'}, status=status.HTTP_201_CREATED)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            related_model = Comment.objects.latest('id')
            serializer_post = CommentReturnSerializer(instance=related_model)
            return Response({'data': serializer_post.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

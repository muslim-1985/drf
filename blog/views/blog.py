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
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser,)

    def post(self, request):
        post = request.data
        user = get_object_or_404(User, id=post['user'])
        cat = get_object_or_404(Category, id=post['cats'])
        # tag = Tag.objects.filter(pk__in=post.get('tags'))
        s = Post.objects.create(title=post['title'], body=post['body'], user=user, category=cat)
        s.tags.set(post.get('tags'))
        s.save()
        posts = Post.objects.all()
        serializer = PostSerializers(posts, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response('hello', status=status.HTTP_201_CREATED)


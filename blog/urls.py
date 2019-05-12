from django.urls import path
from .views import *

urlpatterns = [
    path('', Posts.as_view(), name='posts_list_url'),
    path('post/create', CreatePost.as_view()),
    path('user/create', CreateUserAPIView.as_view()),
    path('user/login', UserAuthenticate.as_view()),
    path('user/update', RetrieveUpdateAPIView.as_view())
]

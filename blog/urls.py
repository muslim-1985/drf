from django.urls import path
from .views import *

urlpatterns = [
    path('', Posts.as_view(), name='posts_list_url'),
    path('post/create', Posts.as_view()),
    path('post/update/<int:post>', PostRetrieveUpdateDestroyAPIView.as_view())
]

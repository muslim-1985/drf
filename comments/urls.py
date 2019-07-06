from django.urls import path
from .views import *

urlpatterns = [
    path('comments/', Comments.as_view(), name='posts_list_url'),
    # path('post/create', Posts.as_view()),
    # path('post/update/<int:pk>', PostRetrieveUpdateDestroyAPIView.as_view()),
    # path('post/delete/<int:pk>', PostRetrieveUpdateDestroyAPIView.as_view())
]
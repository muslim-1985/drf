from django.urls import path
from .views import *

urlpatterns = [
    path('create', CreateUserAPIView.as_view()),
    path('login', UserAuthenticate.as_view()),
    path('update', UserRetrieveUpdateAPIView.as_view())
]

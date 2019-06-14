from __future__ import unicode_literals
from django.db import models
from users.models import User
# Create your models here.


class BotUser(models.Model):
    chat_id = models.IntegerField()
    username = models.CharField(max_length=255, db_index=True)
    first_name = models.CharField(max_length=255, db_index=True)
    last_name = models.CharField(max_length=255, db_index=True)
    avatar = models.ImageField(max_length=255, db_index=True)
    watch = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class BotUserMessage(models.Model):
    subject = models.TextField(blank=True, db_index=True)
    chat_id = models.IntegerField()
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)


class BotMessageFiles(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    path = models.FilePathField(blank=True, default='')
    message = models.ForeignKey(BotUserMessage, on_delete=models.CASCADE, related_name='files')
    created_at = models.DateTimeField(auto_now_add=True)

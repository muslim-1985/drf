from django.db import models
from django.db import models
from users.models import User
from blog.models import Post


# Create your models here.

class Comment(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    body = models.TextField(blank=True, db_index=True)
    file = models.ImageField(max_length=255, db_index=True)
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

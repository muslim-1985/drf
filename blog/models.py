from __future__ import unicode_literals
from django.db import models
import sys
import os
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time
from PIL import Image
from rest_framework.exceptions import ParseError
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.core.files.storage import default_storage
from users.models import User
import magic


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Category(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    image = models.ImageField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = models.TextField(blank=True, db_index=True)
    is_active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})


class PostFile(models.Model):
    name = models.CharField(max_length=255, blank=True, db_index=True)
    path = models.ImageField(blank=True, default='')
    full_path = models.ImageField(blank=True, default='')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        related_model = Post.objects.latest('id')

        filename = default_storage.generate_filename(settings.MEDIA_ROOT + '/user_' + str(
            related_model.user.id) + '/' + 'post' + '_' + str(related_model.id) + '/' + self.path.name)
        full_path = default_storage.save(filename, self.path)

        name = full_path.split('/')[-1]
        path = '/user_' + str(
            related_model.user.id) + '/' + 'post' + '_' + str(
            related_model.id) + '/' + name
        if not self.id:
            self.name = name
            self.path = path
            self.full_path = full_path
            self.compress_image(full_path)
        super(PostFile, self).save(*args, **kwargs)

    def compress_image(self, path):
        # try:
        imageTemproary = Image.open(path)
        # imageTemproary.thumbnail((640, 480))
        imageTemproary.save(path, format=imageTemproary.format, optimize=True)
        # except:
        #     raise ParseError("Some files uploaded error")
        return path

# class PostFileAdmin(PostFile):
#     class Meta:
#         proxy = True
#
#     def save(self, *args, **kwargs):
#         related_model = Post.objects.latest('id')
#         filename = default_storage.generate_filename(settings.MEDIA_ROOT + '/user_' + str(
#             related_model.user.id) + '/' + 'post' + '_' + str(related_model.id) + '/' + self.path.name)
#         full_path = default_storage.save(filename, self.path)
#         name = full_path.split('/')[-1]
#         path = '/user_' + str(
#             related_model.user.id) + '/' + 'post' + '_' + str(
#             related_model.id) + '/' + name
#         if not self.id:
#             self.name = name
#             self.path = path
#             self.full_path = full_path
#             self.compres_image(full_path)
#         super(PostFileAdmin, self).save(*args, **kwargs)
#
#     def compres_image(self, path):
#         # try:
#         print(path)
#         imageTemproary = Image.open(path)
#         # imageTemproary.thumbnail((640, 480))
#         imageTemproary.save(path, format=imageTemproary.format, optimize=True)
#         # except:
#         #     raise ParseError("Some files uploaded error")
#         return path

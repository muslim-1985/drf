from django.contrib import admin
from .models import *


# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('title', 'body', 'user')


admin.site.register(Comment, CommentAdmin)

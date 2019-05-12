from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)


admin.site.register(Post, PostAdmin)


class TagAdmin(admin.ModelAdmin):
    filter_horizontal = ('posts',)


admin.site.register(Tag, TagAdmin)


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)

from django.contrib import admin
from .models import *


class PostFileAdmin(admin.TabularInline):
    model = PostFileAdmin
    exclude = ('full_path', 'name',)


# admin.site.register(PostFile, PostFileAdmin)


class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
    inlines = [PostFileAdmin]


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

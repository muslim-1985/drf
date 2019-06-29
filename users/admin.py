from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *


def ban_users(modeladmin, request, queryset):
    queryset.update(is_active=False)
    print(request.user.first_name)
    banned_user = BannedUser.objects.create(username=request.user.first_name, ip_address=request.user.ip_address,
                                            user_id=request.user.id)
    banned_user.save()


def remove_ban(modeladmin, request, queryset):
    queryset.update(is_active=True)


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'ip_address')
    # readonly_fields = ('first_name', ('last_name'), ('email'), ('username'))
    actions = [ban_users, remove_ban]


admin.site.register(User, UserAdmin)


class BannedUserAdmin(admin.ModelAdmin):
    model = BannedUser
    list_display = ('username', 'ip_address')
    exclude = ('username', 'ip_address',)


admin.site.register(BannedUser, BannedUserAdmin)

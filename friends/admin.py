from django.contrib import admin
from .models import User, Friendship


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    list_display_links = ('id', 'username')
    search_fields = ('id', 'username')


class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created_at', 'status')
    list_display_links = ('from_user', 'to_user', 'created_at', 'status')
    search_fields = ('from_user', 'to_user', 'created_at', 'status')


admin.site.register(User, UserAdmin)
admin.site.register(Friendship, FriendshipAdmin)

from django.contrib import admin

from accounts.models import User_key, User_login


# Register your models here.

@admin.register(User_key)
class UserKeyAdmin(admin.ModelAdmin):
    list_display = ("user_id", 'key', 'timestamp')


@admin.register(User_login)
class UserKeyAdmin(admin.ModelAdmin):
    list_display = ("user_id", 'verified', "is_subscribed")
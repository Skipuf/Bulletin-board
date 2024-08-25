from django.contrib import admin

from .models import SubscriptionMessages


@admin.register(SubscriptionMessages)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'data_published')

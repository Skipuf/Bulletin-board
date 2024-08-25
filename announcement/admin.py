from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'status', 'date_posted')
    list_filter = ('author', 'status', 'date_posted')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text', 'status', 'date_posted')
    list_filter = ('author', 'post', 'status', 'date_posted')

from django.contrib import admin
from blog.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "post", )

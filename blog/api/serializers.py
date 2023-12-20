from rest_framework import serializers

from blog.models import Comment, Post
from blog.service import CommentService, PostService


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "name",
            "email",
            "body",
        ]

    def update(self, instance, validated_data):
        return CommentService.update(
            instance, CommentService.CommentUpdateInput(**validated_data)
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = [
            "post_id",
            "name",
            "email",
            "body",
        ]

    def create(self, validated_data):
        return CommentService.create(
            CommentService.CommentCreateInput(**validated_data)
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "title",
            "body",
        ]

    def create(self, validated_data):
        return PostService.create(PostService.PostCreateInput(**validated_data))

    def update(self, instance, validated_data):
        return PostService.update(
            instance, PostService.PostUpdateInput(**validated_data)
        )

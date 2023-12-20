from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from blog.api.serializers import (
    CommentSerializer,
    CommentCreateSerializer,
    PostSerializer,
)
from blog.models import Comment, Post
from blog.service import CommentService, PostService
from blog.tools import get_serializer_class


class CommentView(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    serializer_classes = {"create": CommentCreateSerializer}

    def get_serializer_class(self):
        return get_serializer_class(self)

    def perform_destroy(self, instance):
        CommentService.delete(instance)


class PostView(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_destroy(self, instance):
        PostService.delete(instance)

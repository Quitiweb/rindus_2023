from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from blog.api.serializers import CommentSerializer, PostSerializer
from blog.models import Comment, Post


class CommentView(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostView(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer

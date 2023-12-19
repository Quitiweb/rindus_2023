from dataclasses import dataclass

from django.db.utils import IntegrityError

from blog.api.exceptions import DoesNotExistException
from blog.models import Comment, Post


class PostService:
    @dataclass
    class PostCreateInput:
        title: str
        body: str

    @dataclass
    class PostUpdateInput:
        title: str = None
        body: str = None

    @dataclass
    class PostCreateBulkInput:
        posts: list

    @staticmethod
    def create_bulk(data: PostCreateBulkInput):
        for post in data.posts:
            PostService.create(
                PostService.PostCreateInput(
                    title=post["title"],
                    body=post["body"],
                )
            )

    @staticmethod
    def create(data: PostCreateInput) -> Post:
        try:
            post = Post.objects.create(
                title=data.title,
                body=data.body,
            )

        except IntegrityError as exc:
            raise IntegrityError(str(exc)) from exc

        return post

    @staticmethod
    def update(instance: Post, data: PostUpdateInput) -> Post:
        instance.title = data.title
        instance.body = data.body
        instance.save(update_fields=["title", "body"])

        return instance


class CommentService:
    @dataclass
    class CommentCreateInput:
        post_id: int
        name: str
        email: str
        body: str

    @dataclass
    class CommentUpdateInput:
        name: str = None
        email: str = None
        body: str = None

    @dataclass
    class CommentCreateBulkInput:
        comments: list

    @staticmethod
    def create_bulk(data: CommentCreateBulkInput):
        for comment in data.comments:
            CommentService.create(
                CommentService.CommentCreateInput(
                    post_id=comment["postId"],
                    name=comment["name"],
                    email=comment["email"],
                    body=comment["body"],
                )
            )

    @staticmethod
    def create(data: CommentCreateInput) -> Comment:
        try:
            post = Post.objects.get(id=data.post_id)
        except Post.DoesNotExist as exc:
            raise DoesNotExistException(detail="The given post does not exist") from exc

        try:
            comment = Comment.objects.create(
                post=post,
                name=data.name,
                email=data.email,
                body=data.body,
            )

        except IntegrityError as exc:
            raise IntegrityError(str(exc)) from exc

        return comment

    @staticmethod
    def update(instance: Comment, data: CommentUpdateInput) -> Comment:
        instance.name = data.name
        instance.email = data.email
        instance.body = data.body
        instance.save(update_fields=["name", "email", "body"])

        return instance

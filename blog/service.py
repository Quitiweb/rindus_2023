from dataclasses import dataclass

from django.db.utils import IntegrityError
from django.forms.models import model_to_dict

from blog.api.exceptions import DoesNotExistException
from blog.models import Comment, Post
from blog.tools import synchronise


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
    def create_bulk(data: PostCreateBulkInput) -> None:
        for post in data.posts:
            PostService.create(
                PostService.PostCreateInput(
                    title=post["title"],
                    body=post["body"],
                ),
                is_bulk=True,
            )

    @staticmethod
    def create(data: PostCreateInput, is_bulk=False) -> Post:
        try:
            post = Post.objects.create(
                title=data.title,
                body=data.body,
            )

        except IntegrityError as exc:
            raise IntegrityError(str(exc)) from exc

        if not is_bulk:
            synchronise(type(post).__name__.lower(), model_to_dict(post), "c")

        return post

    @staticmethod
    def update(instance: Post, data: PostUpdateInput) -> Post:
        instance.title = data.title
        instance.body = data.body
        instance.save(update_fields=["title", "body"])
        synchronise(type(instance).__name__.lower(), model_to_dict(instance), "u")

        return instance

    @staticmethod
    def delete(post: Post) -> None:
        post.delete()
        synchronise(type(post).__name__.lower(), model_to_dict(post), "d")


class CommentService:
    @dataclass
    class CommentCreateInput:
        post_id: int
        name: str
        email: str
        body: str

    @dataclass
    class CommentUpdateInput:
        post: Post = None
        name: str = None
        email: str = None
        body: str = None

    @dataclass
    class CommentCreateBulkInput:
        comments: list

    @staticmethod
    def create_bulk(data: CommentCreateBulkInput) -> None:
        for comment in data.comments:
            CommentService.create(
                CommentService.CommentCreateInput(
                    post_id=comment["postId"],
                    name=comment["name"],
                    email=comment["email"],
                    body=comment["body"],
                ),
                is_bulk=True,
            )

    @staticmethod
    def create(data: CommentCreateInput, is_bulk=False) -> Comment:
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

        if not is_bulk:
            synchronise(type(comment).__name__.lower(), model_to_dict(comment), "c")

        return comment

    @staticmethod
    def update(instance: Comment, data: CommentUpdateInput) -> Comment:
        instance.name = data.name
        instance.email = data.email
        instance.body = data.body
        instance.save(update_fields=["name", "email", "body"])
        synchronise(type(instance).__name__.lower(), model_to_dict(instance), "u")

        return instance

    @staticmethod
    def delete(comment: Comment) -> None:
        comment.delete()
        synchronise(type(comment).__name__.lower(), model_to_dict(comment), "d")

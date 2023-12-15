from dataclasses import dataclass
from typing import Dict

from rest_framework.exceptions import ValidationError

from blog.api.exceptions import AlreadyExistsException
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
    def create_bulk(data: PostCreateBulkInput) -> Dict:
        result = {"success": [], "errors": []}

        for post in data.posts:
            try:
                PostService.create(
                    PostService.PostCreateInput(
                        title=post["title"],
                        body=post["body"],
                    )
                )
                result["success"].append(post["title"])

            except AlreadyExistsException:
                result["errors"].append(post["title"])

            except ValueError as exc:
                raise ValidationError(str(exc)) from exc

        return result

    @staticmethod
    def create(data: PostCreateInput) -> Post:
        post = Post.objects.create(
            title=data.title,
            body=data.body,
        )

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
    def create_bulk(data: CommentCreateBulkInput) -> Dict:
        result = {"success": [], "errors": []}

        for comment in data.comments:
            try:
                CommentService.create(
                    CommentService.CommentCreateInput(
                        post_id=comment["postId"],
                        name=comment["name"],
                        email=comment["email"],
                        body=comment["body"],
                    )
                )
                result["success"].append(comment["name"])

            except AlreadyExistsException:
                result["errors"].append(comment["name"])

            except ValueError as exc:
                raise ValidationError(str(exc)) from exc

        return result

    @staticmethod
    def create(data: CommentCreateInput) -> Comment:
        post = Comment.objects.create(
            post_id=data.post_id,
            name=data.name,
            email=data.email,
            body=data.body,
        )

        return post

    @staticmethod
    def update(instance: Comment, data: CommentUpdateInput) -> Comment:
        instance.name = data.name
        instance.email = data.email
        instance.body = data.body
        instance.save(update_fields=["name", "email", "body"])

        return instance

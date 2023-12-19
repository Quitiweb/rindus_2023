from django.db.utils import IntegrityError
from django.test import TestCase

from blog.api.exceptions import DoesNotExistException
from blog.models import Post, Comment
from blog.service import PostService, CommentService


class PostServiceTest(TestCase):
    def test_create_post(self):
        post_data = PostService.PostCreateInput(title="Test Post", body="Test Body")
        post = PostService.create(post_data)
        self.assertTrue(isinstance(post, Post))

    def test_update_post(self):
        post = Post.objects.create(title="Original Title", body="Original Body")
        update_data = PostService.PostUpdateInput(
            title="Updated Title", body="Updated Body"
        )
        updated_post = PostService.update(post, update_data)
        self.assertEqual(updated_post.title, "Updated Title")
        self.assertEqual(updated_post.body, "Updated Body")

    def test_create_bulk_posts(self):
        posts_data = PostService.PostCreateBulkInput(
            posts=[
                {"title": "Bulk Post 1", "body": "Body 1"},
                {"title": "Bulk Post 2", "body": "Body 2"},
            ]
        )
        PostService.create_bulk(posts_data)
        self.assertEqual(Post.objects.count(), 2)
        self.assertTrue(Post.objects.filter(title="Bulk Post 1").exists())
        self.assertTrue(Post.objects.filter(title="Bulk Post 2").exists())

    def test_create_bulk_posts_with_invalid_data(self):
        posts_data = PostService.PostCreateBulkInput(
            posts=[{"title": None, "body": "Body"}]
        )
        with self.assertRaises(IntegrityError):
            PostService.create_bulk(posts_data)


class CommentServiceTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title="Test Post", body="Test Body")

    def test_create_comment(self):
        comment_data = CommentService.CommentCreateInput(
            post_id=self.post.id,
            name="Test User",
            email="test@example.com",
            body="Test Comment",
        )
        comment = CommentService.create(comment_data)
        self.assertTrue(isinstance(comment, Comment))

    def test_update_comment(self):
        comment = Comment.objects.create(
            post=self.post,
            name="Original Name",
            email="original@example.com",
            body="Original Body",
        )
        update_data = CommentService.CommentUpdateInput(
            name="Updated Name", email="updated@example.com", body="Updated Body"
        )
        updated_comment = CommentService.update(comment, update_data)
        self.assertEqual(updated_comment.name, "Updated Name")
        self.assertEqual(updated_comment.email, "updated@example.com")
        self.assertEqual(updated_comment.body, "Updated Body")

    def test_create_bulk_comments(self):
        post = Post.objects.create(title="Test Post", body="Test Body")
        comments_data = CommentService.CommentCreateBulkInput(
            comments=[
                {
                    "postId": post.id,
                    "name": "User 1",
                    "email": "user1@example.com",
                    "body": "Comment 1",
                },
                {
                    "postId": post.id,
                    "name": "User 2",
                    "email": "user2@example.com",
                    "body": "Comment 2",
                },
            ]
        )
        CommentService.create_bulk(comments_data)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertTrue(Comment.objects.filter(name="User 1").exists())
        self.assertTrue(Comment.objects.filter(name="User 2").exists())

    def test_create_bulk_comments_with_invalid_data(self):
        post = Post.objects.create(title="Test Post", body="Test Body")
        comments_data = CommentService.CommentCreateBulkInput(
            comments=[
                {"postId": post.id, "name": None, "email": "invalid-email", "body": ""}
            ]
        )
        with self.assertRaises(IntegrityError):
            CommentService.create_bulk(comments_data)

    def test_create_comment_with_nonexistent_post(self):
        with self.assertRaises(DoesNotExistException):
            CommentService.create(
                CommentService.CommentCreateInput(
                    post_id=9999,
                    name="Test User",
                    email="test@example.com",
                    body="Test Comment",
                )
            )

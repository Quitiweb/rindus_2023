from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from blog.models import Post, Comment


class ImportDataCommandTest(TestCase):
    @patch("blog.service.PostService.create_bulk")
    @patch("blog.service.CommentService.create_bulk")
    def test_import_data_without_existing_data(
        self, mock_comment_bulk_create, mock_post_bulk_create
    ):
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(Comment.objects.count(), 0)

        call_command("import_data")

        mock_post_bulk_create.assert_called_once()
        mock_comment_bulk_create.assert_called_once()

    @patch("blog.service.PostService.create_bulk")
    @patch("blog.service.CommentService.create_bulk")
    def test_no_import_with_existing_data(
        self, mock_comment_bulk_create, mock_post_bulk_create
    ):
        Post.objects.create(title="Existing Post", body="Existing Body")
        Comment.objects.create(
            post=Post.objects.first(),
            name="Existing Comment",
            email="existing@example.com",
            body="Existing Body",
        )

        call_command("import_data")

        mock_comment_bulk_create.assert_not_called()
        mock_post_bulk_create.assert_not_called()

    @patch("blog.service.PostService.create_bulk")
    @patch("blog.service.CommentService.create_bulk")
    def test_force_reset_option(self, mock_comment_bulk_create, mock_post_bulk_create):
        Post.objects.create(title="Existing Post", body="Existing Body")
        Comment.objects.create(
            post=Post.objects.first(),
            name="Existing Comment",
            email="existing@example.com",
            body="Existing Body",
        )

        call_command("import_data", "--force_reset")

        mock_post_bulk_create.assert_called_once()
        mock_comment_bulk_create.assert_called_once()
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(Comment.objects.count(), 0)

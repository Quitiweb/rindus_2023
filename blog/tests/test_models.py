from django.test import TestCase

from blog.models import Post, Comment


class PostModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title="Test Post", body="This is a test post.")

    def test_post_creation(self):
        self.assertTrue(isinstance(self.post, Post))

    def test_post_fields(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.body, "This is a test post.")

    def test_post_str(self):
        expected_object_name = f"Post - {self.post.pk}: {self.post.title}"
        self.assertEqual(str(self.post), expected_object_name)


class CommentModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title="Test Post", body="This is a test post.")
        self.comment = Comment.objects.create(
            post=self.post,
            name="Tester",
            email="tester@example.com",
            body="This is a test comment.",
        )

    def test_comment_creation(self):
        self.assertTrue(isinstance(self.comment, Comment))

    def test_comment_fields(self):
        self.assertEqual(self.comment.name, "Tester")
        self.assertEqual(self.comment.email, "tester@example.com")
        self.assertEqual(self.comment.body, "This is a test comment.")

    def test_comment_post_relation(self):
        self.assertEqual(self.comment.post, self.post)

    def test_comment_str(self):
        expected_object_name = f"Comment - {self.comment.pk}: {self.comment.name}"
        self.assertEqual(str(self.comment), expected_object_name)

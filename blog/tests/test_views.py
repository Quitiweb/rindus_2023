from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from blog.models import Post, Comment


class PostViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.key)
        self.post = Post.objects.create(title="Test Post", body="Test Body")
        self.url = reverse("blog:post-list")

    def test_get_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        data = {"title": "New Post", "body": "New Body"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_specific_post(self):
        url = reverse("blog:post-detail", kwargs={"pk": self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.post.title)

    def test_update_post(self):
        url = reverse("blog:post-detail", kwargs={"pk": self.post.pk})
        data = {"title": "Updated Post", "body": "Updated Body"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Post")

    def test_delete_post(self):
        url = reverse("blog:post-detail", kwargs={"pk": self.post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())


class CommentViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.key)
        self.post = Post.objects.create(title="Test Post", body="Test Body")
        self.comment = Comment.objects.create(
            post=self.post, name="Tester", email="test@example.com", body="Test Comment"
        )
        self.url = reverse("blog:comment-list")

    def test_get_comments(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment(self):
        data = {
            "post": self.post.id,
            "name": "New Commenter",
            "email": "commenter@example.com",
            "body": "New Comment",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_specific_comment(self):
        url = reverse("blog:comment-detail", kwargs={"pk": self.comment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.comment.name)

    def test_update_comment(self):
        url = reverse("blog:comment-detail", kwargs={"pk": self.comment.pk})
        data = {
            "post": self.post.id,
            "name": "Updated Commenter",
            "email": "updated@example.com",
            "body": "Updated Comment",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.name, "Updated Commenter")

    def test_delete_comment(self):
        url = reverse("blog:comment-detail", kwargs={"pk": self.comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

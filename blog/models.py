from django.db import models


class Post(models.Model):
    user = models.IntegerField(default=99999942)
    title = models.CharField(max_length=250)
    body = models.TextField()

    def __str__(self):
        return f"{self.__class__.__name__} - {self.pk}: {self.title}"

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comment_posts"
    )
    name = models.CharField(max_length=250)
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return f"{self.__class__.__name__} - {self.pk}: {self.name}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

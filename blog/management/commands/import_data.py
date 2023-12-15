from django.core.management.base import BaseCommand

from blog.models import Comment, Post
from blog.service import PostService, CommentService
from blog.tools import get_fake_data, reset_blog_data


class Command(BaseCommand):
    help = """
    Import data from JsonPlaceholder Free Fake Rest API to the local models.

    If there is already some data created, it won't work as this command is intended
    to be run only once at the very beginning.

    You can run the --force_reset option to reset the blog models if needed.
    """

    def add_arguments(self, parser):
        required = parser.add_argument_group("Action flags")

        required.add_argument("--force_reset", action="store_true",
                              help="Reset the data from blog models before the import")

    def handle(self, *args, **kwargs):
        posts = Post.objects.all()
        comments = Comment.objects.all()

        if kwargs["force_reset"]:
            reset_blog_data(comments, posts)

        if not posts and not comments:
            self.import_from_fake_to_local()

        return

    @staticmethod
    def import_from_fake_to_local():
        # Posts
        posts = get_fake_data("posts")
        PostService.create_bulk(
            PostService.PostCreateBulkInput(posts)
        )

        # Comments
        comments = get_fake_data("comments")
        CommentService.create_bulk(
            CommentService.CommentCreateBulkInput(comments)
        )

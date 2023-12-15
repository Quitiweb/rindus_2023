from rest_framework import routers

from blog.api.views import CommentView, PostView

app_name = "blog"

router = routers.DefaultRouter()
router.register("comment", CommentView, basename="comment")
router.register("post", PostView, basename="post")

urlpatterns = router.urls

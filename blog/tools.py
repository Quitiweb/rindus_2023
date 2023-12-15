"""
Common tools for Blog App to reuse them if needed
"""
import json

import requests
from django.core.management.color import no_style
from django.db import connection
from rest_framework import status

from blog.models import Comment, Post

API_URL = "https://jsonplaceholder.typicode.com/"
ALLOWED_MODELS = ["posts", "comments", ]


def reset_blog_data(comments, posts):
    comments.delete()
    posts.delete()

    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Comment, Post])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)


def get_fake_data(model):
    """
    Gets the data from JsonPlaceholder Free Fake Rest API

    Args:
        :model: which data do we want to get? posts or comments
    Returns:
        - None if there was an error
        - A list with the fake generated content
    """
    if model in ALLOWED_MODELS:
        r = requests.get(API_URL + model)
        if r.status_code == status.HTTP_200_OK:
            return json.loads(r.content)

    return

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
ALLOWED_MODELS = [
    "posts",
    "comments",
]


def synchronise(model, data, operation):
    """
    This function make requests to Fake API to synchronise the data
    between both systems.
    :param model: the model name to sync (post or comment)
    :param data: json data for the request
    :param operation:
        - c: create
        - u: update
        - d: delete
    """
    url = API_URL + model + "s/"
    if operation == "c":
        requests.post(url, json=data)
    if operation == "u":
        requests.put(url + str(data["id"]), json=data)
    if operation == "d":
        requests.delete(url + str(data["id"]))


def reset_blog_data(comments, posts):
    """
    Deletes all the data from the blog app and reset the table indexes
    :param comments: Comments.objects.all() queryset
    :param posts: Post.objects.all() queryset
    """
    comments.delete()
    posts.delete()

    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Comment, Post])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)


def get_fake_data(model):
    """
    Gets the data from JsonPlaceholder Free Fake Rest API

    :param model: which data do we want to get? posts or comments
    :return:
        - None if there was an error
        - A list with the fake generated content
    """
    if model in ALLOWED_MODELS:
        r = requests.get(API_URL + model)
        if r.status_code == status.HTTP_200_OK:
            return json.loads(r.content)

    return


def get_serializer_class(view):
    if not hasattr(view, "action") or view.action not in view.serializer_classes:
        return view.serializer_class

    return view.serializer_classes[view.action]

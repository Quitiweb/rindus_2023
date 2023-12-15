from rest_framework import status
from rest_framework.exceptions import APIException


class AlreadyExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "There is an element with the same identifier"
    default_code = "already_exists"

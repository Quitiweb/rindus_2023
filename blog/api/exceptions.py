from rest_framework.exceptions import APIException


class DoesNotExistException(APIException):
    default_detail = "The given element does not exist"
    default_code = "does_not_exist"

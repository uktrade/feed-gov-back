"""
Custom API exceptions
"""
from rest_framework.exceptions import APIException, ValidationError
from rest_framework import status


class NotFoundApiExceptions(APIException):
    status_code = status.HTTP_404_NOT_FOUND


class InvalidRequestParams(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class RequestValidationError(ValidationError):
    status_code = status.HTTP_400_BAD_REQUEST


class ServerError(APIException):
    """
    Generic 500 error
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

from rest_framework.response import Response
from rest_framework import status


class ResponseSuccess(Response):
    """
    Common response object, managing a standard response format
    for all API calls.
    """
    def __init__(self, data=None, http_status=None, content_type=None):
        _status = http_status or status.HTTP_200_OK
        data = data or {}
        reply = {"response": {"success": True}}
        reply['response'].update(data)
        super().__init__(data=reply, status=_status, content_type=content_type)

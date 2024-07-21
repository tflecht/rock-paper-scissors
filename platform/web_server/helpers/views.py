import logging
from typing import Dict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


logger = logging.getLogger(__name__)


# https://stackoverflow.com/questions/30528088/django-rest-exceptions
def default_exception_handler(e: Exception, context: Dict[str, str]) -> Response:
    response = exception_handler(e, context)
    if not response:
        logger.exception(f"unhandled exception: {e}")
        response = Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={'detail': 'internal server error'},
        )
    else:
        logger.exception(f"handled exception: {e}")
    return response

import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    logger.exception(exc)

    if isinstance(exc, Exception):
        return Response(
            {"error": str(exc)},
            status=(
                response.status_code
                if response
                else status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
        )

    return response

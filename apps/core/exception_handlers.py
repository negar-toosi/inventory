import logging
from django.http import Http404
from django.core.exceptions import (
    PermissionDenied,
    ValidationError as DjangoValidationError,
)
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied as DRFPermissionDenied,
    NotFound,
    ValidationError,
    Throttled,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_default_handler

from apps.core.custom_response import CustomResponse
from apps.core.exceptions import InventoryError

logger = logging.getLogger(__name__)


def inventory_exception_handler(exc: Exception, context: dict) -> Response:

    if isinstance(exc, InventoryError):
        message = str(exc.detail)
        return CustomResponse(message, exc.extra, exc.status_code)

    if isinstance(exc, Http404):
        exc = NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = DRFPermissionDenied()
    elif isinstance(exc, DjangoValidationError):
        exc = ValidationError(
            detail=exc.message_dict if hasattr(exc, "message_dict") else exc.messages
        )

    drf_response = drf_default_handler(exc, context)

    if drf_response is not None:
        return CustomResponse(
            message=_drf_message(exc),
            extra=drf_response.data,
            http_status=drf_response.status_code,
        )

    logger.exception("Unhandled exception", exc_info=exc)
    return CustomResponse(
        message="An unexpected internal error occurred. Please try again later.",
        extra={},
        http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def _drf_message(exc: Exception) -> str:
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        return "Authentication credentials were not provided or are invalid."
    if isinstance(exc, DRFPermissionDenied):
        return "You do not have permission to perform this action."
    if isinstance(exc, NotFound):
        return "The requested resource was not found."
    if isinstance(exc, Throttled):
        return f"Request was throttled. Expected available in {exc.wait} seconds."
    if isinstance(exc, ValidationError):
        return "Invalid input. Please check the provided data."
    if isinstance(exc, APIException):
        detail = exc.detail
        if isinstance(detail, str):
            return detail
        if isinstance(detail, list) and detail and isinstance(detail[0], str):
            return str(detail[0])
        return str(detail)
    return "An error occurred."

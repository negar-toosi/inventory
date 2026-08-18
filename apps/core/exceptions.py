import logging

from rest_framework import status
from rest_framework.exceptions import APIException


logger = logging.getLogger(__name__)


class InventoryError(APIException):
    default_detail = "An application error occurred."
    default_code = "app_error"

    def __init__(
        self,
        message: str | None = None,
        http_status: int = status.HTTP_400_BAD_REQUEST,
        extra: dict | None = None,
    ):
        self.status_code = http_status
        self.extra = extra or {}
        super().__init__(detail=message or self.default_detail)

    @classmethod
    def bad_request(
        cls,
        message: str = "Bad request.",
        extra: dict | None = None,
    ):
        return cls(
            message=message, http_status=status.HTTP_400_BAD_REQUEST, extra=extra
        )

    @classmethod
    def service_unavailable(
        cls,
        message: str = "The requested service is temporarily unavailable.",
        extra: dict | None = None,
    ):
        return cls(
            message=message,
            http_status=status.HTTP_503_SERVICE_UNAVAILABLE,
            extra=extra,
        )

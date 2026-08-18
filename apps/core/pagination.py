from rest_framework.pagination import (
    LimitOffsetPagination as _LimitOffsetPagination,
    PageNumberPagination as _PageNumberPagination,
)

from apps.core.custom_response import CustomResponse


def get_paginated_response(
    *,
    message,
    pagination_class,
    serializer_class,
    queryset,
    request,
    view,
):
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)

    return CustomResponse(
        data=serializer.data,
        message=message,
    )


class CustomPageNumberPagination(_PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

    def get_paginated_response(self, data):
        return CustomResponse(
            data=data,
            message="Data retrieved successfully.",
            extra={
                "total": self.page.paginator.count,
                "page": self.page.number,
                "page_size": self.page.paginator.per_page,
                "total_pages": self.page.paginator.num_pages,
            },
        )


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

    def get_paginated_response(self, data):
        return CustomResponse(
            data=data,
            message="Data retrieved successfully.",
            extra={
                "limit": self.limit,
                "offset": self.offset,
                "count": self.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
        )

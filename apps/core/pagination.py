from rest_framework.pagination import PageNumberPagination as _PageNumberPaginaton
from apps.core.custom_response import CustomResponse


def get_paginated_response(*, message, serializer_class, queryset, request, view):
    paginator = PageNumberPagination()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)
    return CustomResponse(data=serializer.data, message=message)


class PageNumberPagination(_PageNumberPaginaton):
    page_size = 10

    def get_paginated_response(self, data):
        return CustomResponse(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )

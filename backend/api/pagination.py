from rest_framework.pagination import PageNumberPagination

from common.constants import DEFAULT_PAGE_SIZE, PAGE_SIZE_QUERY_PARAM


class LimitPageNumberPagination(PageNumberPagination):
    """Кастомный пагинатор с фильтрации и параметру limit."""

    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = PAGE_SIZE_QUERY_PARAM

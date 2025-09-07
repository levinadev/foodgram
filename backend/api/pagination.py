from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    """Кастомный пагинатор с фильтрации и параметру limit."""

    page_size = 6
    page_size_query_param = "limit"

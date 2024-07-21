from rest_framework import pagination


class GlobalPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page'

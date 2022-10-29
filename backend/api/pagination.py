from rest_framework import pagination

# API Backend by : Habibul Rahman Qalbi


class LargeSetPagination(pagination.PageNumberPagination):
    page_size = 1000
    page_size_query_param = "page_size"
    max_page_size = 2000


class StandardSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 200


class SmallSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 20

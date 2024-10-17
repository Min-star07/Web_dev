from rest_framework.pagination import PageNumberPagination


class ListPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "size"
    page_size = 8

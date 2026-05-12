"""
API Pagination - Custom pagination classes.
"""
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination - 20 ta element har sahifada.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class LargeResultsSetPagination(PageNumberPagination):
    """
    Katta natijalar uchun pagination - 50 ta element.
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200

from rest_framework.pagination import PageNumberPagination

from cookingcrafts.constants import Common as C


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = C.PAGE_SIZE

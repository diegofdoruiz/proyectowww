from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10

    def get_paginated_response(self, data):
        context = {
            'pag_links': self.get_html_context(),
            'results': data,
        }
        return Response(context)


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        context = {
            'search_text': self.request.GET.get('search_text', None),
            'pag_links': self.get_html_context(),
            'rows': data,
        }
        return Response(context)


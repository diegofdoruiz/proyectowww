from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


<<<<<<< HEAD
class CustomLimitOffsetPagination(LimitOffsetPagination):
=======
class UserLimitOffsetPagination(LimitOffsetPagination):
>>>>>>> b781bbc5447e812b65f01e1b63d8aeebb665fe0f
    default_limit = 10
    max_limit = 10

    def get_paginated_response(self, data):
        context = {
            'pag_links': self.get_html_context(),
            'results': data,
        }
        return Response(context)


<<<<<<< HEAD
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5
=======
class UserPageNumberPagination(PageNumberPagination):
    page_size = 1
>>>>>>> b781bbc5447e812b65f01e1b63d8aeebb665fe0f

    def get_paginated_response(self, data):
        context = {
            'search_text': self.request.GET.get('search_text', None),
            'pag_links': self.get_html_context(),
<<<<<<< HEAD
            'rows': data,
=======
            'users': data,
>>>>>>> b781bbc5447e812b65f01e1b63d8aeebb665fe0f
        }
        return Response(context)


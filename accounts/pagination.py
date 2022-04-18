from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'p'

    def get_paginated_response(self, data):
        return Response({
            
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })

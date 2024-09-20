from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    """
    Custom Pagination for customizing pagination data
    """

    def get_paginated_response(self, data):
        return Response(
            {
                "pagination": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "count": self.page.paginator.count,
                    "total_page": self.page.paginator.num_pages,
                    "current_page": self.page.number,
                },
                "results": data,
            }
        )

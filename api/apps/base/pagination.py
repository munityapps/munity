from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100000

    def get_page_size(self, request):
        if self.page_size_query_param:
            page_size = min(
                int(request.query_params.get(self.page_size_query_param, self.page_size)), self.max_page_size
            )
            if page_size > 0:
                return page_size
            elif page_size == 0:
                return None
            else:
                pass
        return self.page_size

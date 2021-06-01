import threading

class RequestMiddleware(object):
    def __init__(self, get_response, thread_local=threading.local()):
        self.get_response = get_response
        self.thread_local = thread_local

    def __call__(self, request):
        self.thread_local.current_request = request
        setattr(self.thread_local.current_request, "workspace_slug", request.META.get("HTTP_X_WORKSPACE"))
        response = self.get_response(request)

        return response

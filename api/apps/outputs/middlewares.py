import datetime
import threading

from outputs.slack import send_slack_log_message


class SlackErrorReportingMiddleware(object):

    # ErrorMiddleware initialization
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    # Handle all exeption
    def process_exception(self, request, exception):
        # securilty access to request body
        try:
            body = str(request.body)
        except:
            body = "DRF does not allow to read the body again !"

        try:
            text = "*Exception*"
            attachments = [
                {
                    "text": f'*Workspace*: {request.META.get("HTTP_X_WORKSPACE")}\n'
                    f"*Path*: {request.path}\n"
                    f'*Datetime*: {datetime.datetime.now().isoformat(" ")}\n'
                    f"*Method*: {request.method}\n"
                    f'*JWT*: ``` {request.META.get("HTTP_AUTHORIZATION", "noAuth")} ```'
                    f"*Request*: ``` {body} ```"
                    f"*Exeption*: ``` {str(exception)}```",
                    "color": "#FF0000",
                }
            ]
            send_slack_log_message(text, attachments)
        except:
            pass

    # Handle all response
    def process_template_response(self, request, response):
        # securilty access to request body
        try:
            body = str(request.body)
        except:
            body = "DRF does not allow to read the body again !"
        try:
            if response.status_code >= 400:
                text = f"Error: *{response.status_code}* "
                attachments = [
                    {
                        "text": f'*Workspace*: {request.META.get("HTTP_X_WORKSPACE")}\n'
                        f"*Path*: {request.path}\n"
                        f'*Datetime*: {datetime.datetime.now().isoformat(" ")}\n'
                        f"*Method*: {request.method}\n"
                        f'*JWT*: ``` {request.META.get("HTTP_AUTHORIZATION", "noAuth")} ```'
                        f"*Request*: ``` {body} ```"
                        f"*Resonse*: ``` {str(response.data)}```",
                        "color": "#FF8000",
                    }
                ]
                send_slack_log_message(text, attachments)
        except:
            pass
        return response

        return self.process_template_response(request, response)


class RequestMiddleware(object):
    def __init__(self, get_response, thread_local=threading.local()):
        self.get_response = get_response
        self.thread_local = thread_local

    def __call__(self, request):
        self.thread_local.current_request = request
        setattr(self.thread_local.current_request, "workspace_slug", request.META.get("HTTP_X_WORKSPACE"))
        response = self.get_response(request)

        return response

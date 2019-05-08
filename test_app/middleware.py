import datetime

from test_app.models import RequestLog


class UsersActivityMiddleware:
    """
    Saves all user requests to the database
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        requests_log = RequestLog()
        response = self.get_response(request)
        start_request = datetime.datetime.now()
        self.get_response(request)
        end_request = datetime.datetime.now()
        execution_time = datetime.datetime.strptime(
            str(end_request - start_request), '%H:%M:%S.%f'
        )
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        requests_log.user = request.user
        requests_log.method = request.method
        requests_log.path = request.path
        requests_log.ip_address = ip_address
        requests_log.status = response.status_code
        requests_log.execution_time = execution_time.time()
        requests_log.save()
        return response

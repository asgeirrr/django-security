try:
    from importlib import import_module
except ImportError:  # For Django < 1.8
    from django.utils.importlib import import_module

from django.utils.encoding import force_text
from django.core.urlresolvers import get_callable
from django.core.exceptions import ImproperlyConfigured

from ipware.ip import get_ip

from .models import InputLoggedRequest
from .exception import ThrottlingException
from .config import SECURITY_DEFAULT_THROTTLING_VALIDATORS, SECURITY_THROTTLING_FAILURE_VIEW, SECURITY_LOG_IGNORE_IP


try:
    THROTTLING_VALIDATORS_MODULE, THROTTLING_VALIDATORS_VAR = SECURITY_DEFAULT_THROTTLING_VALIDATORS.rsplit('.', 1)
    THROTTLING_VALIDATORS = getattr(import_module(THROTTLING_VALIDATORS_MODULE), THROTTLING_VALIDATORS_VAR)
except ImportError:
    raise ImproperlyConfigured('Configuration DEFAULT_THROTTLING_VALIDATORS does not contain valid module')


class LogMiddleware(object):

    def process_request(self, request):
        if get_ip(request) not in SECURITY_LOG_IGNORE_IP:
            request._logged_request = InputLoggedRequest.objects.prepare_from_request(request)

    def _render_throttling(self, request, exception):
        return get_callable(SECURITY_THROTTLING_FAILURE_VIEW)(request, exception)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if getattr(request, '_logged_request', False):

            # Exempt all logs
            if getattr(callback, 'log_exempt', False):
                del request._logged_request

            # TODO: this is not the best solution if the request throw exception inside process_request of some Middleware
            # the bode will be included (But I didn't have better solution now)
            if getattr(callback, 'hide_request_body', False):
                request._logged_request.request_body = ''

            # Check if throttling is not exempted
            if not getattr(callback, 'throttling_exempt', False):
                try:
                    for validator in THROTTLING_VALIDATORS:
                        validator.validate(request)
                except ThrottlingException as exception:
                    return self.process_exception(request, exception)

    def process_response(self, request, response):
        if hasattr(request, '_logged_request'):
            request._logged_request.update_from_response(response)
            request._logged_request.save()
        return response

    def process_exception(self, request, exception):
        if hasattr(request, '_logged_request'):
            logged_request = request._logged_request
            logged_request.error_description = force_text(exception)
            logged_request.exception_name = exception.__class__.__name__
            if isinstance(exception, ThrottlingException):
                logged_request.type = InputLoggedRequest.THROTTLED_REQUEST
                return self._render_throttling(request, exception)

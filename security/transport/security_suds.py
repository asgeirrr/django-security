from six.moves.urllib.parse import urlparse, parse_qs
import six
from django.utils import timezone
from django.template.defaultfilters import truncatechars
from django.utils.encoding import force_text

from suds.transport.https import HttpAuthenticated
from suds.transport.http import HttpTransport
from suds.client import Client as DefaultClient

from security.compatibility import extract_headers
from security.config import LOG_REQUEST_BODY_LENGTH, LOG_RESPONSE_BODY_LENGTH
from security.models import LoggedRequest, OutputLoggedRequest


def stringify_dict(d):
    def stringify(value):
        if isinstance(value, six.binary_type):
            return force_text(value)
        elif isinstance(value, dict):
            return stringify_dict(value)
        else:
            return value

    return {k: stringify(v) for k, v in d.items()}


class SecurityHttpTransportMixin:

    def log_and_send(self, request, slug, related_objects):
        parsed_url = urlparse(request.url)
        logged_kwargs = {
            'is_secure': parsed_url.scheme == 'https',
            'host': parsed_url.netloc,
            'path': parsed_url.path,
            'method': 'POST',
            'queries': parse_qs(parsed_url.query),
            'slug': self.slug,
            'request_timestamp': timezone.now(),
            'request_headers': request.headers.copy(),
            'request_body': truncatechars(force_text(request.message[:LOG_REQUEST_BODY_LENGTH + 1],
                                                     errors='replace'), LOG_REQUEST_BODY_LENGTH),
        }
        try:
            resp = HttpTransport.send(self, request)
            logged_kwargs.update({
                'response_timestamp': timezone.now(),
                'response_code': resp.code,
                'response_headers': extract_headers(resp).copy(),
                'response_body': truncatechars(force_text(resp.message[:LOG_RESPONSE_BODY_LENGTH + 1],
                                                          errors='replace'), LOG_RESPONSE_BODY_LENGTH),
                'status': LoggedRequest.get_status(resp.code)
            })
            return resp
        except Exception as ex:
            logged_kwargs.update({
                'error_description': force_text(ex),
                'status': LoggedRequest.CRITICAL,
                'exception_name': ex.__class__.__name__
            })
            raise
        finally:
            # TODO: remove suds is fixed. (This is here to prevent nasty Python 3 related bugs with str vs. bytes.)
            logged_kwargs = stringify_dict(logged_kwargs)
            output_logged_request = OutputLoggedRequest.objects.create(**logged_kwargs)
            for obj in self.related_objects or ():
                output_logged_request.related_objects.create(content_object=obj)
            self.related_objects = []


class SecurityHttpAuthenticated(SecurityHttpTransportMixin, HttpAuthenticated):

    def __init__(self, slug=None, related_objects=None, *args, **kwargs):
        self.slug = slug
        self.related_objects = related_objects or []
        HttpAuthenticated.__init__(self, *args, **kwargs)

    def add_related_objects(self, *related_objects):
        self.related_objects += list(related_objects)

    def send(self, request):
        self.addcredentials(request)
        return self.log_and_send(request, self.slug, self.related_objects)


class Client(DefaultClient):

    def __init__(self, url, slug=None, related_objects=None, transport=None, **kwargs):
        transport = transport or SecurityHttpAuthenticated(slug=slug, related_objects=related_objects)
        DefaultClient.__init__(self, url, transport=transport, **kwargs)

    def add_related_objects(self, *related_objects):
        self.options.transport.add_related_objects(*related_objects)

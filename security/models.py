from __future__ import unicode_literals

import json

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.template.defaultfilters import truncatechars
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey

from jsonfield import JSONField

from ipware.ip import get_ip

from chamber.utils import keep_spacing

from security.config import LOG_REQUEST_BODY_LENGTH, LOG_RESPONSE_BODY_LENGTH, LOG_RESPONSE_BODY_CONTENT_TYPES
from security.utils import get_headers


# Prior to Django 1.5, the AUTH_USER_MODEL setting does not exist.
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


def get_full_host(request):
    host = request.META['SERVER_NAME']
    port = request.META['SERVER_PORT']
    if (request.is_secure() and port != '443') or (not request.is_secure() and port != '80'):
        return '{}:{}'.format(host, port)
    else:
        return host


class InputLoggedRequestManager(models.Manager):
    """
    Create new LoggedRequest instance from HTTP request
    """

    def prepare_from_request(self, request):
        user = hasattr(request, 'user') and request.user.is_authenticated() and request.user or None
        path = truncatechars(request.path, 200)
        request_body = truncatechars(force_text(request.body[:LOG_REQUEST_BODY_LENGTH + 1],
                                     errors='replace'), LOG_REQUEST_BODY_LENGTH)
        return self.model(request_headers=get_headers(request), request_body=request_body, user=user,
                          method=request.method.upper()[:7], host=get_full_host(request),
                          path=path, queries=request.GET.dict(), is_secure=request.is_secure(),
                          ip=get_ip(request), request_timestamp=timezone.now())


@python_2_unicode_compatible
class LoggedRequest(models.Model):

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    STATUS_CHOICES = (
        (INFO, _('Info')),
        (WARNING, _('Warning')),
        (ERROR, _('Error')),
        (DEBUG, _('Debug')),
        (CRITICAL, _('Critical')),
    )

    host = models.CharField(_('host'), max_length=255, null=False, blank=False)
    method = models.CharField(_('method'), max_length=7, null=False, blank=False)
    path = models.CharField(_('URL path'), max_length=255, null=False, blank=False)
    queries = JSONField(_('queries'), null=True, blank=True)
    is_secure = models.BooleanField(_('HTTPS connection'), default=False, null=False, blank=False)

    # Request information
    request_timestamp = models.DateTimeField(_('request timestamp'), null=False, blank=False, db_index=True)
    request_headers = JSONField(_('request headers'), null=True, blank=True)
    request_body = models.TextField(_('request body'), null=False, blank=True)

    # Response information
    response_timestamp = models.DateTimeField(_('response timestamp'), null=True, blank=True)
    response_code = models.PositiveSmallIntegerField(_('response code'), null=True, blank=True)
    response_headers = JSONField(_('response headers'), null=True, blank=True)
    response_body = models.TextField(_('response body'), null=True, blank=True)

    status = models.PositiveSmallIntegerField(_('status'), choices=STATUS_CHOICES, null=False, blank=False)
    error_description = models.TextField(_('error description'), null=True, blank=True)
    exception_name = models.CharField(_('exception name'), null=True, blank=True, max_length=255)

    def _get_json_field_humanized(self, field_name):
        return keep_spacing(json.dumps(getattr(self, field_name), indent=4, ensure_ascii=False, cls=DjangoJSONEncoder))

    def get_request_headers_humanized(self):
        return self._get_json_field_humanized('request_headers')

    def get_response_headers_humanized(self):
        return self._get_json_field_humanized('response_headers')

    def get_queries_humanized(self):
        return self._get_json_field_humanized('queries')

    def get_request_body_humanized(self):
        return keep_spacing(self.request_body) if self.request_body is not None else None

    def get_response_body_humanized(self):
        return keep_spacing(self.response_body) if self.response_body is not None else None

    @classmethod
    def get_status(cls, status_code):
        if status_code >= 500:
            return LoggedRequest.ERROR
        elif status_code >= 400:
            return LoggedRequest.WARNING
        else:
            return LoggedRequest.INFO

    def response_time(self):
        return ('%s ms' % ((self.response_timestamp - self.request_timestamp).microseconds / 1000)
                if self.response_timestamp else None)
    response_time.short_description = _('Response time')

    def short_path(self):
        return truncatechars(self.path, 20)
    short_path.short_description = _('Path')
    short_path.filter_by = 'path'
    short_path.order_by = 'path'

    def __str__(self):
        return self.path

    class Meta:
        abstract = True


class InputLoggedRequest(LoggedRequest):
    COMMON_REQUEST = 1
    THROTTLED_REQUEST = 2
    SUCCESSFUL_LOGIN_REQUEST = 3
    UNSUCCESSFUL_LOGIN_REQUEST = 4

    TYPE_CHOICES = (
        (COMMON_REQUEST, _('Common request')),
        (THROTTLED_REQUEST, _('Throttled request')),
        (SUCCESSFUL_LOGIN_REQUEST, _('Successful login request')),
        (UNSUCCESSFUL_LOGIN_REQUEST, _('Unsuccessful login request'))
    )

    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_('user'), null=True, blank=True, on_delete=models.SET_NULL)
    ip = models.GenericIPAddressField(_('IP address'), null=False, blank=False)
    type = models.PositiveSmallIntegerField(_('type'), choices=TYPE_CHOICES, default=COMMON_REQUEST, null=False,
                                            blank=False)

    objects = InputLoggedRequestManager()

    def update_from_response(self, response):
        self.response_timestamp = timezone.now()
        self.status = self.get_status(response.status_code)
        self.response_code = response.status_code
        self.response_headers = dict(response.items())

        if not response.streaming and response.get('content-type', '').split(';')[0] in LOG_RESPONSE_BODY_CONTENT_TYPES:
            response_body = truncatechars(force_text(response.content[:LOG_RESPONSE_BODY_LENGTH + 1],
                                                     errors='replace'), LOG_RESPONSE_BODY_LENGTH)
        else:
            response_body = ''

        self.response_body = response_body

    class Meta:
        verbose_name = _('input logged request')
        verbose_name_plural = _('input logged requests')
        ordering = ('-request_timestamp',)


class OutputLoggedRequest(LoggedRequest):
    slug = models.SlugField(_('slug'), null=True, blank=True)

    class Meta:
        verbose_name = _('output logged request')
        verbose_name_plural = _('output logged requests')
        ordering = ('-request_timestamp',)


class OutputLoggedRequestRelatedObjects(models.Model):
    output_logged_request = models.ForeignKey(OutputLoggedRequest, verbose_name=_('output logged requests'), null=False,
                                              blank=False, related_name='related_objects')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def display_object(self, request):
        from is_core.utils import render_model_object_with_link

        return render_model_object_with_link(request, self.content_object) if self.content_object else None
    display_object.short_description = _('object')

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class HelperError(APIException):
    pass


class TimeframeError(HelperError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('invalid timeframe')
    default_code = _('invalid_timeframe')


class RandomlyError(HelperError):
    pass


class MoreSelectionsThanOptions(RandomlyError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('more selections than options')
    default_code = _('more_selections_than_options')


class InvalidOperation(HelperError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('Invalid operation')
    default_code = _('invalid_operation')

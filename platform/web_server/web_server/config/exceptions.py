from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class ConfigError(APIException):
    pass


class MissingSetting(ConfigError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('missing setting')
    default_code = _('missing_setting')

    def __init__(self, setting_name: str):
        self.detail = f"missing required setting {setting_name}"

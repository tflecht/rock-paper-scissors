import json
import logging
import requests

from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, status

from helpers.typing import JsonBlob


logger = logging.getLogger(__name__)


class HeaderError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('header error')
    default_code = _('header_error')

    def __init__(self, detail='header error'):
        self.detail = detail



def boolean_string(string_rep: str) -> bool:
    string_rep = str(string_rep).lower()
    if 'true' == string_rep:
        return True
    if 'false' == string_rep:
        return False
    raise ValueError(f"could not convert '{string_rep}' into a boolean")


def get_header(request, header_name):
    header_value = request.META.get(header_name)
    if not header_value:
        raise HeaderError(f"missing header {header_name}")
    return header_value


def get_json_from_header(request, header_name) -> JsonBlob:
    serialized_data = get_header(request, header_name)
    try:
        return json.loads(serialized_data)
    except json.JSONDecodeError:
        raise HeaderError(detail="invalid data in {header_name}")


def get_mandatory_typed_list(listable, *, key: str, value_type):
    value_list = get_optional_typed_list(listable, key=key, value_type=value_type)
    if value_list is None:
        raise exceptions.ValidationError(f"Missing required list '{key}'")
    return value_list


def get_mandatory_typed_value(from_dict, *, key: str, value_type):
    value = get_optional_typed_value(from_dict, key=key, value_type=value_type)
    if value is None:
        raise exceptions.ValidationError(f"Key '{key}' missing and it is mandatory.")
    return value


def get_optional_typed_list(listable, *, key: str, value_type):
    value_list = listable.getlist(key)
    if value_list is None:
        return None
    try:
        return [value_type(value) for value in value_list]
    except ValueError as e:
        raise exceptions.ValidationError(f"Value '{e.args}' from list '{key}' can't be converted to expected type {value_type}.")


def get_optional_typed_value(from_dict, *, key: str, value_type):
    value = from_dict.get(key)
    if value is None:
        return None
    if value_type == bool and type(value) == str:
        value = boolean_string(value)
    try:
        return value_type(value)
    except ValueError:
        raise exceptions.ValidationError(f"Value '{value}' for Key '{key}' can't be converted to expected type {value_type}.")


def assert_success(response: requests.Response):
    #TODO: Check the response type and log based on that.
    if not response.ok:
        logger.warn(f"[{response.status_code}] With content: {response.content}")
    
        response.raise_for_status()

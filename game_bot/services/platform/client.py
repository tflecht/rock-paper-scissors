import discord
import json
from json import JSONDecodeError
import requests
from typing import List, Optional
from urllib.parse import quote

from . import exceptions as service_exceptions, utils
import settings
from utils.typing import JsonBlob


def headers(
        *,
        guild: Optional[discord.Guild] = None,
        text_channel: Optional[discord.TextChannel] = None,
        user: Optional[discord.User] = None,
) -> JsonBlob:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-API-KEY": settings.PLATFORM_API_KEY,
    }
    if guild:
        headers['X-DISCORD-GUILD'] = json.dumps(utils.guild_dict(guild))
    if text_channel:
        headers['X-DISCORD-TEXT-CHANNEL'] = json.dumps(utils.text_channel_dict(text_channel))
    if user:
        headers['X-DISCORD-USER'] = json.dumps(utils.user_dict(user))
    return headers


def delete(
        *,
        acceptable_status_codes: Optional[List[int]] = [200],
        endpoint: str,
        headers: Optional[JsonBlob] = headers(),
        query_params: Optional[JsonBlob] = None,
) -> requests.Response:
    response = requests.delete(
        url_for(endpoint=endpoint, query_params=query_params),
        headers=headers,
    )
    validate_response(response, acceptable_status_codes=acceptable_status_codes)
    return response


def get(
        *,
        endpoint: str,
        headers: Optional[JsonBlob] = headers(),
        query_params: Optional[JsonBlob] = None,
        acceptable_status_codes: Optional[List[int]] = [200],
) -> requests.Response:
    response = requests.get(
        url_for(endpoint=endpoint, query_params=query_params),
        headers=headers,
    )
    validate_response(response, acceptable_status_codes=acceptable_status_codes)
    return response


def post(
        *,
        data: Optional[JsonBlob] = None,
        endpoint: str,
        headers: Optional[JsonBlob] = headers(),
        query_params: Optional[JsonBlob] = None,
        acceptable_status_codes: Optional[List[int]] = [200],
) -> requests.Response:
    response = requests.post(
        url_for(endpoint=endpoint, query_params=query_params),
        headers=headers,
        data=data,
    )
    validate_response(response, acceptable_status_codes=acceptable_status_codes)
    return response


def put(
        *,
        data: Optional[JsonBlob] = None,
        endpoint: str,
        headers: Optional[JsonBlob] = headers(),
        query_params: Optional[JsonBlob] = None,
        acceptable_status_codes: Optional[List[int]] = [200],
) -> requests.Response:
    response = requests.put(
        url_for(endpoint=endpoint, query_params=query_params),
        headers=headers,
        data=data,
    )
    validate_response(response, acceptable_status_codes=acceptable_status_codes)
    return response


def patch(
        *,
        data: Optional[JsonBlob] = None,
        endpoint: str,
        headers: Optional[JsonBlob] = headers(),
        query_params: Optional[JsonBlob] = None,
        acceptable_status_codes: Optional[List[int]] = [200],
) -> Optional[JsonBlob]:
    response = requests.patch(
        url_for(endpoint=endpoint, query_params=query_params),
        headers=headers,
        data=data,
    )
    validate_response(response, acceptable_status_codes=acceptable_status_codes)
    return response


def url_for(
        *,
        endpoint: str,
        query_params: Optional[JsonBlob] = {},
) -> str:
    url = endpoint
    if 'http' != endpoint[0:4].lower():
        url = f"{settings.PLATFORM_URL}{endpoint}"
    if query_params:
        qp_list = [f"{quote(k)}={quote(str(v))}" for k, v in query_params.items()]
        qp_string = '&'.join(qp_list)
        url += f"?{qp_string}"
    return url


def validate_response(response, acceptable_status_codes: Optional[List[int]] = [200]):
    if response.status_code not in acceptable_status_codes:
        error_string = str(response)
        error_detail = error_string
        try:
            error_string = response.json()
            error_detail = error_string['detail']
        except JSONDecodeError:
            pass
        raise service_exceptions.BadRequest(error_detail)

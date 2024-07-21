import logging
import requests
from typing import Optional

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from discord import models
from discord.domain import users
from helpers import request as request_helpers
from web_server import settings


logger = logging.getLogger(__name__)


#https://testdriven.io/blog/custom-permission-classes-drf/
def assert_from_discord_bot(request: requests.Request):
    # This passes the header correctly:
    #     curl -H "Content-Type: application/json" \
    #          -H "X-API-KEY: vagrant-gamers-bot-api-key" \
    #          -X POST http://192.168.61.7:9000/gamers/
    api_key = settings.GAME_DISCORD_BOT_API_KEY
    assert_correct_api_key(request, api_key)


def assert_correct_api_key(request: requests.Request, expected_api_key: str):
    try:
        api_key = request_helpers.get_header(request, 'HTTP_X_API_KEY')
    except request_helpers.HeaderError as e:
        raise PermissionDenied(detail=str(e))
    if api_key != expected_api_key:
        logger.info(f"received API KEY '{api_key}, expected '{expected_api_key}'")
        raise PermissionDenied(detail="incorrect API key")


def inject_discord_user(request: requests.Request) -> Optional[models.User]:
    try:
        user_data = request_helpers.get_json_from_header(request, 'HTTP_X_DISCORD_USER')
    except request_helpers.HeaderError as e:
        return None
    user, _ = users.from_request(**user_data)
    request.discord_user = user
    return user


class FromDiscordBot(permissions.BasePermission):
    def has_permission(self, request: requests.Request, view) -> bool:
        assert_from_discord_bot(request)
        inject_discord_user(request)
        return True


class FromDiscordUser(FromDiscordBot):
    def has_permission(self, request: requests.Request, view) -> bool:
        super().has_permission(request, view)
        if not hasattr(request, 'discord_user'):
            raise PermissionDenied("missing discord user header.")
        return True

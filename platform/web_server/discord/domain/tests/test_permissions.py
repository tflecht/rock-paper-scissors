import json
from typing import Dict

import pytest
from pytest import raises

from rest_framework.exceptions import PermissionDenied

from discord import exceptions, models
from discord.domain import permissions
from helpers.typing import JsonBlob
from web_server import settings


class MockRequest:
    def __init__(self, headers):
        self.META = headers


def mock_request_with_headers(headers: Dict[str, str]={}) -> MockRequest:
    return MockRequest(headers)


################################################################################
# inject_discord_guild
################################################################################


################################################################################
# inject_discord_user
################################################################################
@pytest.mark.django_db
def test_inject_discord_user_fails_for_inactive_guild(discord_headers_from_user: JsonBlob):
    mock_request = mock_request_with_headers(discord_headers_from_user)
    permissions.inject_discord_user(mock_request)
    mock_request.discord_user.is_active = False
    mock_request.discord_user.save()
    with raises(exceptions.UserGone):
        permissions.inject_discord_user(mock_request)


################################################################################
# FromDiscordBot
################################################################################
@pytest.mark.django_db
def test_from_discord_bot_succeeds(discord_headers_from_bot: JsonBlob):
    mock_request = mock_request_with_headers(discord_headers_from_bot)
    permissions.FromDiscordBot().has_permission(mock_request, None)
    assert mock_request.command_prerequisite is None


@pytest.mark.django_db
def test_from_discord_bot_injects_command_prerequisite(
        discord_headers_from_bot_with_command_prerequisite:JsonBlob,
):
    mock_request = mock_request_with_headers(discord_headers_from_bot_with_command_prerequisite)
    permissions.FromDiscordBot().has_permission(mock_request, None)
    assert mock_request.command_prerequisite == (
        discord_headers_from_bot_with_command_prerequisite['HTTP_X_DISCORD_COMMAND_PREREQUISITE']
    )
    

@pytest.mark.django_db
def test_from_discord_bot_injects_guild_if_provided(discord_headers_from_guild: JsonBlob):
    mock_request = mock_request_with_headers(discord_headers_from_guild)
    assert not hasattr(mock_request, 'discord_guild')
    permissions.FromDiscordBot().has_permission(mock_request, None)
    assert mock_request.discord_guild is not None


@pytest.mark.django_db
def test_from_discord_bot_injects_user_if_provided(discord_headers_from_user: JsonBlob):
    mock_request = mock_request_with_headers(discord_headers_from_user)
    permissions.FromDiscordBot().has_permission(mock_request, None)
    assert mock_request.discord_user is not None


@pytest.mark.django_db
def test_from_discord_bot_injects_channel_if_provided_with_guild(
        discord_headers_from_channel: JsonBlob,
):
    mock_request = mock_request_with_headers(discord_headers_from_channel)
    permissions.FromDiscordBot().has_permission(mock_request, None)
    assert mock_request.discord_channel is not None


@pytest.mark.django_db
def test_from_discord_bot_creates_association_if_provided_guild_and_user(
        discord_headers_user_from_guild: JsonBlob,
):
    assert not models.GuildAssociation.objects.exists()
    mock_request = mock_request_with_headers(discord_headers_user_from_guild)
    permissions.FromDiscordBot().has_permission(mock_request, None)
    # 1 association for owner, 1 for user
    #assert models.GuildAssociation.objects.count() == 2
    assert models.GuildAssociation.objects.count() == 1
    assert models.GuildAssociation.objects.filter(
        guild=mock_request.discord_guild,
        user=mock_request.discord_user,
    ).exists()
    

def test_from_discord_bot_fails_without_api_key():
    mock_request = mock_request_with_headers()
    try:
        permissions.FromDiscordBot().has_permission(mock_request, None)
    except PermissionDenied as e:
        assert e.detail == "missing header HTTP_X_API_KEY"
        return
    assert False


def test_from_discord_bot_fails_with_incorrect_api_key():
    wrong_api_key = settings.GAMERS_DISCORD_BOT_API_KEY + "WRONG"
    mock_request = mock_request_with_headers({ 'HTTP_X_API_KEY': wrong_api_key})
    try:
        permissions.FromDiscordBot().has_permission(mock_request, None)
    except PermissionDenied as e:
        assert e.detail == "incorrect API key"
        return
    assert False
    

@pytest.mark.django_db
def test_from_discord_bot_does_not_inject_provided_channel_without_guild(
        discord_text_channel_data: JsonBlob,
):
    headers = {
        'HTTP_X_API_KEY': settings.GAMERS_DISCORD_BOT_API_KEY,
        'HTTP_X_DISCORD_TEXT_CHANNEL': json.dumps(discord_text_channel_data),
    }
    mock_request = mock_request_with_headers(headers)
    permissions.FromDiscordBot().has_permission(mock_request, None)
    assert not hasattr(mock_request, 'discord_guild')


################################################################################
# FromDiscordGuild
################################################################################
@pytest.mark.django_db
def test_from_discord_guild_succeeds(discord_headers_from_guild: JsonBlob):
    mock_request = mock_request_with_headers(discord_headers_from_guild)
    permissions.FromDiscordGuild().has_permission(mock_request, None)
    assert mock_request.discord_guild is not None


@pytest.mark.django_db
def test_from_discord_guild_fails_without_guild_provided():
    headers = {
        'HTTP_X_API_KEY': settings.GAMERS_DISCORD_BOT_API_KEY,
    }
    mock_request = mock_request_with_headers(headers)
    with raises(permissions.PermissionDenied):
        permissions.FromDiscordGuild().has_permission(mock_request, None)


################################################################################
# UserFromDiscordGuild
################################################################################
@pytest.mark.django_db
def test_user_from_discord_guild_user_succeeds(discord_headers_user_from_guild: JsonBlob):
    mock_request = mock_request_with_headers(discord_headers_user_from_guild)
    permissions.UserFromDiscordGuild().has_permission(mock_request, None)
    assert mock_request.discord_guild is not None
    assert mock_request.discord_user is not None


@pytest.mark.django_db
def test_user_from_discord_guild_fails_without_guild_provided(discord_headers_from_user: JsonBlob):
    mock_request = mock_request_with_headers(discord_headers_from_user)
    with raises(permissions.PermissionDenied):
        permissions.UserFromDiscordGuild().has_permission(mock_request, None)


@pytest.mark.django_db
def test_user_from_discord_guild_fails_without_user_provided(discord_headers_from_guild: JsonBlob):
    mock_request = mock_request_with_headers(discord_headers_from_guild)
    with raises(permissions.PermissionDenied):
        permissions.UserFromDiscordGuild().has_permission(mock_request, None)


################################################################################
# FromDiscordTextChannel
################################################################################
@pytest.mark.django_db
def test_from_discord_text_channel_succeeds(discord_headers_user_from_channel: JsonBlob):
    mock_request = mock_request_with_headers(discord_headers_user_from_channel)
    permissions.FromDiscordTextChannel().has_permission(mock_request, None)
    assert mock_request.discord_channel is not None
    assert mock_request.discord_guild is not None
    assert mock_request.discord_user is not None


@pytest.mark.django_db
def test_from_discord_text_channel_fails_without_user_provided(discord_headers_from_channel: JsonBlob):
    mock_request = mock_request_with_headers(discord_headers_from_channel)
    with raises(permissions.PermissionDenied):
        permissions.FromDiscordTextChannel().has_permission(mock_request, None)


@pytest.mark.django_db
def test_from_discord_text_channel_fails_without_channel_provided(
        discord_headers_user_from_guild: JsonBlob,
):
    mock_request = mock_request_with_headers(discord_headers_user_from_guild)
    with raises(permissions.PermissionDenied):
        permissions.FromDiscordTextChannel().has_permission(mock_request, None)


@pytest.mark.django_db
def test_from_discord_text_channel_fails_without_guild_provided(
        discord_text_channel_data: JsonBlob,
        discord_user_data: JsonBlob,
):
    headers = {
        'HTTP_X_API_KEY': settings.GAMERS_DISCORD_BOT_API_KEY,
        'HTTP_X_DISCORD_USER': json.dumps(discord_user_data),
        'HTTP_X_DISCORD_TEXT_CHANNEL': json.dumps(discord_text_channel_data),
    }
    mock_request = mock_request_with_headers(headers)
    with raises(permissions.PermissionDenied):
        permissions.FromDiscordTextChannel().has_permission(mock_request, None)


################################################################################
# FromDiscordUser 
################################################################################
@pytest.mark.django_db
def test_from_discord_user_succeeds(discord_headers_from_user: JsonBlob):
    assert not models.ProfileLinkage.objects.exists()
    mock_request = mock_request_with_headers(discord_headers_from_user)
    permissions.FromDiscordUser().has_permission(mock_request, None)


@pytest.mark.django_db
def test_from_discord_user_fails_without_user_provided():
    headers = {
        'HTTP_X_API_KEY': settings.GAMERS_DISCORD_BOT_API_KEY,
    }
    mock_request = mock_request_with_headers(headers)
    with raises(permissions.PermissionDenied):
        permissions.FromDiscordUser().has_permission(mock_request, None)

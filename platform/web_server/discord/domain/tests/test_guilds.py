import pytest

from django.utils.timezone import datetime, timedelta

from discord import models
from discord.domain import guilds
from helpers.typing import JsonBlob


###############################################################################
# deactivate
###############################################################################
@pytest.mark.django_db
def test_deactivate_succeeds(discord_channel: models.Channel):
    guild = discord_channel.guild
    assert guild.discord_guild_created_at is not None
    assert guild.icon_url != ''
    assert guild.is_active is True
    assert guild.member_count > 0
    assert guild.name != ''
    assert guild.verification_level > 0
    guilds.deactivate(guild)
    guild.refresh_from_db()
    assert guild.discord_guild_created_at is None
    assert guild.icon_url is None 
    assert guild.is_active is False
    assert guild.member_count == 0
    assert guild.name == ''
    assert guild.verification_level == 0


###############################################################################
# from_request
###############################################################################
@pytest.mark.skip('Skipped until we are allowed to use Discord member intents')
@pytest.mark.django_db
def test_from_request_creates_guild_and_owner_if_they_do_not_exist(discord_guild_data: JsonBlob):
    assert not models.Guild.objects.exists()
    assert not models.ProfileLinkage.objects.exists()
    guild, created = guilds.from_request(**discord_guild_data)
    assert guild is not None
    assert created
    assert models.Guild.objects.count() == 1
    assert models.ProfileLinkage.objects.count() == 1
    assert guild.owner == models.ProfileLinkage.objects.first()


@pytest.mark.django_db
def test_from_request_updates_its_info(discord_guild_data: JsonBlob):
    guild, _ = guilds.from_request(**discord_guild_data)
    guild.description += "WITH_MORE_LETTERS"
    guild.discord_guild_created_at += timedelta(days=100)
    guild.icon_url += "WITH_MORE_LETTERS"
    guild.member_count += 10
    guild.name += "WITH_MORE_LETTERS"
    guild.owner = None
    guild.verification_level += 1
    guild.save()
    guild, created = guilds.from_request(**discord_guild_data)
    assert not created
    assert guild.description == discord_guild_data['description']
    assert guild.discord_guild_created_at == datetime.fromisoformat(
        discord_guild_data['created_at'],
    )
    assert guild.icon_url == discord_guild_data['icon_url']
    assert guild.member_count == discord_guild_data['member_count']
    assert guild.name == discord_guild_data['guild_name']
    #assert guild.owner == models.ProfileLinkage.objects.get(
    #    discord_user_id=discord_guild_data['owner_discord_id'],
    #)
    assert guild.verification_level == discord_guild_data['verification_level']
    
import discord
from typing import Dict


def guild_dict(guild: discord.Guild) -> Dict[str, str]:
    return {
        'created_at': guild.created_at.isoformat(),
        'description': guild.description,
        'guild_id': str(guild.id),
        'guild_name': guild.name,
        'icon_url': guild.icon.url if guild.icon else '',
        'member_count': guild.member_count,
        #'owner_discord_id': str(guild.owner.id),
        #'owner_discord_name': guild.owner.name,
        'verification_level': guild.verification_level.value,
    }


def text_channel_dict(channel: discord.TextChannel) -> Dict[str, str]:
    return {
        'name': channel.name,
        'id': channel.id,
    }


def user_dict(user: discord.Member):
    return {
        'avatar_hash': user.avatar.key if user.avatar else '',
        'id': user.id,
        'name': user.name,
    }

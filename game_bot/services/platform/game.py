"""cards-related calls to gamers_service"""
import discord
import json

from services.platform import client
from utils.typing import JsonBlob


class GameAlreadyOver(Exception):
    pass


def choose(
    *,
    choice: str,
    game_id: int,
    guild: discord.Guild,
    user: discord.User,
) -> JsonBlob:
    response = client.post(
        headers=client.headers(guild=guild, user=user),
        endpoint=f"game/choose/{game_id}/",
        data=json.dumps(
            {
                "choice": choice,
            },
        ),
    )
    return response.json()


def play(
    *,
    guild: discord.Guild,
    user: discord.User,
) -> JsonBlob:
    response = client.post(
        headers=client.headers(guild=guild, user=user),
        endpoint=f"game/play/",
    )
    return response.json()


def status(
    *,
    game_id: int,
    guild: discord.Guild,
    user: discord.User,
) -> JsonBlob:
    response = client.get(
        headers=client.headers(guild=guild, user=user),
        endpoint=f"game/status/{game_id}/",
    )
    return response.json()

from typing import Tuple

from discord import models
from discord.domain import user
from helpers.typing import JsonBlob


def from_request(
        *,
        avatar_hash: str,
        id: str,
        name: str,
) -> Tuple[models.User, bool]:
    return user.ensure(
        {
            'avatar': avatar_hash,
            'id': id,
            'username': name,
        }
    )

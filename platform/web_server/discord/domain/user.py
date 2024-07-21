import logging
from typing import List, Tuple

from django.contrib.auth.models import User as AuthUser
from django.db import transaction
from django.db.models import QuerySet
from django.utils.timezone import now

from discord import exceptions, models
from helpers.typing import JsonBlob


logger = logging.getLogger(__name__)


@transaction.atomic
def ensure(user_info: JsonBlob) -> Tuple[models.User, bool]:
    try:
        discord_user_id = user_info['id']
        discord_user_name = user_info['username']
    except KeyError as e:
        raise exceptions.DiscordInteractionError(
            f"user info response from discord missing {e}:({user_info})",
        )
    avatar_hash = user_info.get('avatar', '')
    if avatar_hash is None:
        avatar_hash = ''
    user, created = models.User.objects.get_or_create(
        discord_user_id=discord_user_id,
        defaults={
            'avatar_hash': avatar_hash,
            'discord_user_name': discord_user_name,
        }
    )
    if not created:
        if avatar_hash:
            user.avatar_hash = avatar_hash
        if discord_user_name:
            user.discord_user_name = discord_user_name
    if not user.auth_user:
        auth_user, _ = AuthUser.objects.get_or_create(username=str(discord_user_id))
        user.auth_user = auth_user
    user.save()
    return user, created

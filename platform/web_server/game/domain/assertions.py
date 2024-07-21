import logging

from discord.models import User as DiscordUser
from game import exceptions, models


logger = logging.getLogger(__name__)


def not_complete(game: models.Game):
    if game.is_complete:
        raise exceptions.GameAlreadyComplete(game)


def not_in_game(user: DiscordUser):
    if models.Game.objects.filter(is_complete=False, players__user=user).exists():
        raise exceptions.UserAlreadyInGame(user)

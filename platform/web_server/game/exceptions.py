from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException

from discord.models import User as DiscordUser
from game import models


class GameError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('Error in game app')
    default_code = _('game_error')

    def __init__(self, *, detail=None):
        self.detail=detail


class GameAlreadyComplete(GameError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('This game has already been completed')
    default_code = _('game_already_complete')

    def __init__(self, game: models.Game):
        super().__init__(
            detail={
                'code': self.default_code,
                'message': f"Game already complete",
            },
        )


class UserAlreadyInGame(GameError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('This Discord user is already in a game')
    default_code = _('discord_user_already_in_game')

    def __init__(self, user: DiscordUser):
        super().__init__(
            detail={
                'code': self.default_code,
                'message': f"Discord user {user} is already in a game",
            },
        )

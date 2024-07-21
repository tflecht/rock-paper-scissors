from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class DiscordInteractionError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('Error interacting with Discord')
    default_code = _('discord_interaction_error')
    def __init__(self, detail=None):
        if detail:
            self.detail=detail


class DiscordUserAlreadyRegistered(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('This Discord user has already been registered')
    default_code = _('discord_user_already_registered')


class UsernameAlreadyExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('This username has already been registered')
    default_code = _('username_already_registered')

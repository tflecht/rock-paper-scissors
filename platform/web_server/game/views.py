import logging

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from discord.domain import permissions as discord_permissions
from game import models, serializers
from game.domain import game as game_domain
from helpers import request as request_helpers


logger = logging.getLogger(__name__)


class Choose(generics.CreateAPIView):
    permission_classes = (
        discord_permissions.FromDiscordUser,
    )

    serializer_class = serializers.GameSerializer

    def create(self, request: Request, *args, **kwargs):
        game_id = request_helpers.get_mandatory_typed_value(
            self.kwargs,
            key='game_id',
            value_type=int,
        )
        choice = request_helpers.get_mandatory_typed_value(
            request.data,
            key='choice',
            value_type=str,
        )
        game = models.Game.objects.get(id=game_id, user=self.request.discord_user)
        game = game_domain.choose(choice=choice, game=game)
        return Response(
            data=self.get_serializer(game).data,
            status=status.HTTP_200_OK,
        )


class PlayGame(generics.CreateAPIView):
    permission_classes = (
        discord_permissions.FromDiscordUser,
    )

    serializer_class = serializers.GameSerializer

    def create(self, request: Request, *args, **kwargs):
        game = game_domain.create_or_resume_game(request.discord_user)
        return Response(
            data=self.get_serializer(game).data,
            status=status.HTTP_200_OK,
        )

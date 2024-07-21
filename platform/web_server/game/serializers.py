from rest_framework import serializers

from discord.serializers import UserSerializer
from . import models


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game

        fields = (
            'id',
            'is_complete',
            'opponent_choice',
            'result',
            'user',
            'user_choice',
        )

    user = UserSerializer()

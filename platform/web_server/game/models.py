import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.mixins import TimestampedModelMixin


logger = logging.getLogger(__name__)


class Game(TimestampedModelMixin):
    is_complete = models.BooleanField(default=False)

    opponent_choice = models.TextField(
        blank=False,
        null=True,
    )

    result = models.TextField(
        blank=False,
        null=True,
    )

    user = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='game_participations',
        to='discord.User',
    )

    user_choice = models.TextField(
        blank=False,
        null=True,
    )

    def __str__(self) -> str:
        s = f"Game initiated by {self.user} at {self.created_at}"
        if self.is_complete:
            s += f" completed at {self.updated_at} result: {self.result}"
            s += f" user choice '{self.user_choice}' opponent chose {self.opponent_choice}'"
        else:
            s += " (in progress)"
        return s

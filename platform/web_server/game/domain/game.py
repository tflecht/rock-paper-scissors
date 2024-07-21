import logging

from django.db import transaction

from discord.models import User as DiscordUser
from helpers import randomly
from game import exceptions, models
from game.domain import assertions


logger = logging.getLogger(__name__)


LOSS = 'loss'
PAPER = 'paper'
ROCK = 'rock'
SCISSORS = 'scissors'
TIE = 'tie'
WIN = 'win'
CHOICES = [ROCK, PAPER, SCISSORS]


def result(user_choice: str, opponent_choice: str) -> str:
    if user_choice not in CHOICES:
        raise exceptions.GameError
    if opponent_choice not in CHOICES:
        raise exceptions.GameError
    if user_choice == opponent_choice:
        return TIE
    if user_choice== ROCK:
        return WIN if opponent_choice == SCISSORS else LOSS
    elif user_choice == PAPER:
        return WIN if opponent_choice == ROCK else LOSS
    else: # SCISSORS
        return WIN if opponent_choice == PAPER else LOSS


def choose(
    *,
    choice: str,
    game: models.Game,
) -> models.Game:
    assertions.not_complete(game)
    opponent_choice = CHOICES[randomly.random_integer(0, len(CHOICES))]
    game.is_complete = True
    game.opponent_choice = opponent_choice
    game.result = result(choice, opponent_choice)
    game.user_choice = choice
    game.save()
    return game


@transaction.atomic
def create_or_resume_game(user: DiscordUser) -> models.Game:
    game = models.Game.objects.filter(is_complete=False, user=user).first()
    if not game:
        game = models.Game.objects.create(user=user)
    return game

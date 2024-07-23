from dotenv import load_dotenv
import json
import logging
import os
from random import randint
import requests
import time
from typing import Dict, Optional


load_dotenv()
logger = logging.getLogger(__name__)


HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}
JsonBlob = Dict[str, str]
PLATFORM_HOSTNAME = os.getenv('PLATFORM_HOSTNAME')

LOSS = 'loss'
PAPER = 'paper'
ROCK = 'rock'
SCISSORS = 'scissors'
TIE = 'tie'
WIN = 'win'
CHOICES = [ROCK, PAPER, SCISSORS]


def get_pending_game() -> Optional[JsonBlob]:
	try:
		return requests.get(
			f"{PLATFORM_HOSTNAME}/game/pending/",
			headers=HEADERS,
		)
	except Exception as e:
		logger.error(f"pending game request failed: {e}")


def play_game(game_data: JsonBlob):
	print(f"play_game({game_data})")
	opponent_choice = CHOICES[randint(0, len(CHOICES)-1)]
	try:
		requests.post(
			f"{PLATFORM_HOSTNAME}/game/complete/",
			headers=HEADERS,
			data=json.dumps(
				{
					'game_id': game_data['id'],
					'opponent_choice': opponent_choice,
				}
			)
		)
	except Exception as e:
		logger.error(f"complete game request failed: {e}")


while 1:
	response = get_pending_game()
	if not response:
		continue
	if response.status_code not in [200, 204]:
		logger.error("bad response from pending games endpoint")
	elif response.status_code == 200:
		play_game(response.json())
		break
	time.sleep(1)

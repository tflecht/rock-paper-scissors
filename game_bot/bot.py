from sentry_sdk import capture_exception
import discord
import logging

import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


intents = discord.Intents.default()
bot = discord.Bot(
    command_prefix='.',
    intents=intents,
)


def run():
    bot.run(settings.BOT_TOKEN)

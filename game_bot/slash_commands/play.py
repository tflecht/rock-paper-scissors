"""Slash command for querying for games that have cards"""
from discord import ApplicationContext

import bot
from services import platform
from ui import views


@bot.bot.slash_command(
        description="play a game"
)
async def play(ctx: ApplicationContext):
    """Play a game"""
    if not ctx.channel:
            await ctx.respond("please play from a channel")
            return
    await views.game_state.respond_to(ctx.interaction)

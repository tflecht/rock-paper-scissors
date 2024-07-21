import logging

import discord

from utils.typing import JsonBlob


logger = logging.getLogger(__name__)


def play(user_data: JsonBlob) -> discord.Embed:
    embed = discord.Embed(title="Rock Paper Scissors")
    description = f"""
        Choose your weapon `{user_data['discord_user_name']}`!
    """
    embed.description = description
    embed.set_image(url='https://miro.medium.com/v2/resize:fit:1338/format:webp/0*3oJdSb7B26rt3xjJ')
    embed.set_thumbnail(url=user_data['avatar_image_url'])
    return embed

def summary(game_data: JsonBlob) -> discord.Embed:
    result = game_data['result']
    user_data = game_data['user']
    title = description = ''
    if result == 'win':
        title = "You won! 😍"
        description = f"Congratulations `{user_data['discord_user_name']}`, you pwned your opponent."
    elif result  == 'tie':
        title = "You tied."
        description = "You tied. 😐"
    else:
        title = "You lost. 😦"
    embed = discord.Embed()
    embed.title = title
    embed.description = description
    embed.add_field(name="You chose", value=game_data['user_choice'], inline=True)
    embed.add_field(name="They chose", value=game_data['opponent_choice'], inline=True)
    return embed

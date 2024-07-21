from typing import Optional

import discord

from services import platform
from ui import embeds
from utils.typing import JsonBlob


async def respond_to(interaction: discord.Interaction):
    view = View(interaction)
    await view.respond()


class View(discord.ui.View):
    def __init__(
            self,
            interaction: discord.Interaction,
            *,
            data: Optional[JsonBlob]=None,
    ):
        super().__init__()
        if not data:
            data = platform.game.play(guild=interaction.guild, user=interaction.user)
        self.data = data
        self.game_id = data['id']
        self.is_complete = data['is_complete']
        self.result = data['result']
        self.user_data = data['user']
        self.interaction = interaction
        self.add_buttons()

    def _configure_play(self):
        self.add_buttons()

    def add_buttons(self):
        rock_button = discord.ui.Button(
            disabled=self.is_complete,
            emoji="🪨",
            label="Rock",
            row=1,
            style=discord.ButtonStyle.blurple,
        )
        rock_button.callback = self.callback_rock
        self.add_item(rock_button)
        paper_button = discord.ui.Button(
            disabled=self.is_complete,
            emoji="📰",
            label="Paper",
            row=1,
            style=discord.ButtonStyle.grey,
        )
        paper_button.callback = self.callback_paper
        self.add_item(paper_button)
        scissors_button = discord.ui.Button(
            disabled=self.is_complete,
            emoji="✂️",
            label="Scissors",
            row=1,
            style=discord.ButtonStyle.green,
        )
        scissors_button.callback = self.callback_scissors
        self.add_item(scissors_button)

    async def callback_rock(self, interaction: discord.Interaction):
        data = platform.game.choose(
            choice='rock',
            game_id=self.game_id,
            guild=interaction.guild,
            user=interaction.user,
        )
        await self.replace(data=data, interaction=interaction)

    async def callback_paper(self, interaction: discord.Interaction):
        data = platform.game.choose(
            choice='paper',
            game_id=self.game_id,
            guild=interaction.guild,
            user=interaction.user,
        )
        await self.replace(data=data, interaction=interaction)

    async def callback_scissors(self, interaction: discord.Interaction):
        data = platform.game.choose(
            choice='scissors',
            game_id=self.game_id,
            guild=interaction.guild,
            user=interaction.user,
        )
        await self.replace(data=data, interaction=interaction)

    async def replace(self, *, data: JsonBlob, interaction: discord.Interaction):
        view = View(data=data, interaction=interaction)
        await interaction.response.edit_message(
            embed=view.embed,
            view=view,
        )

    async def respond(self):
        await self.interaction.response.send_message(
            embed=self.embed,
            view=self,
            ephemeral=True,
        )
    
    @property
    def embed(self):
        if self.is_complete:
            return embeds.game_state.summary(self.data)
        return embeds.game_state.play(self.user_data)

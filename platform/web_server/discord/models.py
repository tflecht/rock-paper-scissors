import logging

from django.contrib.auth.models import User as AuthUser
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from helpers.mixins import TimestampedModelMixin


logger = logging.getLogger(__name__)


class Channel(TimestampedModelMixin):
    discord_channel_id = models.TextField(
        blank=False,
        db_index=True,
        help_text=_('discord-defined id for this '),
        unique=True,
    )

    guild = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='channels',
        to='discord.Guild',
    )

    name = models.TextField(
        blank=False,
        help_text=_('The name of the discord guild'),
    )

    def __str__(self):
        return f"{self.guild.name}:{self.name}({self.discord_channel_id})"


class Guild(TimestampedModelMixin):
    description = models.TextField(
        blank=True,
        help_text=_("the guild's description"),
        null=True,
    )

    discord_guild_created_at = models.DateTimeField(
        help_text=_('the creation date time of the guild'),
        null=True,
    )

    discord_guild_id = models.TextField(
        blank=False,
        db_index=True,
        help_text=_('discord-defined id for this guild'),
        unique=True,
    )

    icon_url = models.TextField(
        help_text=_('the icon image url for this guild'),
        null=True,
    )

    member_count = models.PositiveIntegerField(
        help_text=_('a snapshot count of the members in the guild'),
    )

    name = models.TextField(
        blank=False,
        help_text=_('The name of the discord guild'),
    )

    owner = models.ForeignKey(
        null=True,
        on_delete=models.SET_NULL,
        related_name='owned_guilds',
        to='discord.User',
    )

    verification_level = models.PositiveIntegerField(
        help_text=_('what level of verification this guild requires of its users'),
    )

    def __str__(self):
        return f"{self.name}({self.discord_guild_id})"


class GuildAssociation(TimestampedModelMixin):
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['guild', 'user'],
                name="there can at most be one association between a discord user and guild",
            ),
        ]

    guild = models.ForeignKey(
        null=False,
        on_delete=models.CASCADE,
        related_name='user_associations',
        to='discord.Guild',
    )

    most_recent_assocation = models.DateTimeField(
        auto_now_add=True,
        help_text=_('the most recent time this user did something in assocation with this guild'),
    )

    user = models.ForeignKey(
        null=False,
        on_delete=models.CASCADE,
        related_name='guild_associations',
        to='discord.User',
    )

    def __str__(self):
        return f"{self.guild.name} <=> {self.user.discord_user_name}"


class User(TimestampedModelMixin):
    auth_user = models.OneToOneField(
        AuthUser,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='user',
    )

    avatar_hash = models.TextField(
        blank=True,
        help_text=_('used to look up the user avatar image'),
    )

    discord_user_id = models.TextField(
        blank=False,
        db_index=True,
        help_text=_('associated Discord user ID'),
        unique=True,
    )

    discord_user_name = models.TextField(
        blank=False,
        default='friend',
        help_text=_('associated Discord user name'),
    )

    email_address = models.EmailField(
        blank=True,
        default='',
        help_text=_('the email address associated with this discord account'),
    )

    @property
    def avatar_image_url(self) -> str:
        return f"https://cdn.discordapp.com/avatars/{self.discord_user_id}/{self.avatar_hash}.png"

    def __str__(self):
        return f"{self.auth_user} <=> {self.discord_user_name}:{self.discord_user_id}"

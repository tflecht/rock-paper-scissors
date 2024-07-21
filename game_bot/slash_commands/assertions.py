from discord import ApplicationContext, User

from . import exceptions


def in_channel(ctx: ApplicationContext):
    if not ctx.channel:
        raise exceptions.NotRunFromChannel()


def in_guild(ctx: ApplicationContext):
    if not ctx.guild:
        raise exceptions.NotRunFromGuild()


def is_administrator(ctx: ApplicationContext):
    in_guild(ctx)
    if not _is_user_administrator(ctx.author):
        raise exceptions.NotAdministrator()


def _is_user_administrator(user: User) -> bool:
    if not hasattr(user, 'guild_permissions'):
        return False
    return user.guild_permissions.administrator

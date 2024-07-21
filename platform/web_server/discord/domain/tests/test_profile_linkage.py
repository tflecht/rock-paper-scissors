import pytest

from discord import models
from discord.domain import user


###############################################################################
# deactivate
###############################################################################
@pytest.mark.django_db
def test_deactivate_succeeds(discord_linkage: models.ProfileLinkage):
    assert discord_linkage.avatar_hash != ''
    assert discord_linkage.discord_user_name != ''
    assert discord_linkage.email_address != ''
    assert discord_linkage.is_active is True
    assert discord_linkage.profile is not None
    user.deactivate(discord_linkage)
    assert discord_linkage.avatar_hash == ''
    assert discord_linkage.discord_user_name == ''
    assert discord_linkage.email_address == ''
    assert discord_linkage.is_active is False
    assert discord_linkage.profile is None

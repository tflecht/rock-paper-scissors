from rest_framework import serializers

from . import models


class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Guild

        fields = (
            'id',
            'discord_guild_id',
            'icon_url',
            'name',
        )


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Channel

        fields = (
            'id',
            'discord_channel_id',
            'name',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User

        fields = (
            'avatar_image_url',
            'discord_user_id',
            'discord_user_name',
            'guild_associations',
        )

    avatar_image_url = serializers.SerializerMethodField()
    guild_associations = serializers.SerializerMethodField()

    def get_avatar_image_url(self, linkage):
        return linkage.avatar_image_url

    def get_guild_associations(self, linkage):
        guild_ids = linkage.guild_associations.values_list('guild_id', flat=True)
        guilds = models.Guild.objects.filter(id__in=guild_ids)
        return GuildSerializer(guilds, many=True).data

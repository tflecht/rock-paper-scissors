# Generated by Django 3.2.25 on 2024-07-21 02:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, help_text="the guild's description", null=True)),
                ('discord_guild_created_at', models.DateTimeField(help_text='the creation date time of the guild', null=True)),
                ('discord_guild_id', models.TextField(db_index=True, help_text='discord-defined id for this guild', unique=True)),
                ('icon_url', models.TextField(help_text='the icon image url for this guild', null=True)),
                ('member_count', models.PositiveIntegerField(help_text='a snapshot count of the members in the guild')),
                ('name', models.TextField(help_text='The name of the discord guild')),
                ('verification_level', models.PositiveIntegerField(help_text='what level of verification this guild requires of its users')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('avatar_hash', models.TextField(blank=True, help_text='used to look up the user avatar image')),
                ('discord_user_id', models.TextField(db_index=True, help_text='associated Discord user ID', unique=True)),
                ('discord_user_name', models.TextField(default='friend', help_text='associated Discord user name')),
                ('email_address', models.EmailField(blank=True, default='', help_text='the email address associated with this discord account', max_length=254)),
                ('auth_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GuildAssociation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('most_recent_assocation', models.DateTimeField(auto_now_add=True, help_text='the most recent time this user did something in assocation with this guild')),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_associations', to='discord.guild')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guild_associations', to='discord.user')),
            ],
        ),
        migrations.AddField(
            model_name='guild',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_guilds', to='discord.user'),
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('discord_channel_id', models.TextField(db_index=True, help_text='discord-defined id for this ', unique=True)),
                ('name', models.TextField(help_text='The name of the discord guild')),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channels', to='discord.guild')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='guildassociation',
            constraint=models.UniqueConstraint(fields=('guild', 'user'), name='there can at most be one association between a discord user and guild'),
        ),
    ]

from celery.schedules import crontab
from dotenv import load_dotenv
import os


load_dotenv()

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://@localhost")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://@localhost")

# Celery (non-environment specific) settings
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# Store tasks in our db, so we can return them for polling by clients
CELERY_RESULT_BACKEND = 'django-db'


# https://crontab.guru/
CELERY_BEAT_SCHEDULE = {
    "award_passive_earnings": {
        "task": "rewards_program.tasks.award_passive_earnings",
        "schedule": crontab(minute='0', hour="2"), # Run at 2am every day 
    },
    "conclude_lotteries": {
        "task": "lottery.tasks.conclude_lotteries",
        "schedule": 60.0,
    },
    "refresh_token_metadata": {
        "task": "hl_token.tasks.refresh_metadata",
        "schedule": crontab(minute='5,15,25,35,45,55'),
    },
    "update_eth_to_usd": {
        "task": "blockchain.tasks.update_eth_to_usd",
        "schedule": crontab(minute='1'), # Run at the 1st minute of every hour
    },
    "update_psn_gamer": {
        "task": "psn.tasks.update_one",
        "schedule": 1.0,
    },
    "update_token_types": {
        "task": "hl_token.tasks.update_token_types",
        "schedule": 60.0,
    },
    "update_wei_balances": {
        "task": "blockchain.tasks.update_wei_balances",
        "schedule": crontab(minute='0', hour="*/4"), # Run at the 0th minute of every 4th hour
    },
    "update_xbox_gamer_account_details": {
        "task": "xbox.tasks.periodic_user_detail_ingestion",
        "schedule": 15.0,
    },
    "update_xbox_gamer_achievements": {
        "task": "xbox.tasks.periodic_seasonal_achievement_ingestion",
        "schedule": 15.0,
    },
    "update_xbox_gamer_playtime_data": {
        "task": "xbox.tasks.periodic_playtime_ingestion",
        "schedule": 15.0,
    },
    "update_steam_gamer_account_details": {
        "task": "steam.tasks.periodic_user_detail_ingestion",
        "schedule": 60.0,
    },
    "update_steam_gamer_achievements": {
        "task": "steam.tasks.periodic_recent_achievement_ingestion",
        "schedule": 10.0,
    },
    "update_steam_title_details": {
        "task": "steam.tasks.periodic_title_detail_ingestion",
        "schedule": 5.0,
    },
    "update_steam_gamer_gameplay_details": {
        "task": "steam.tasks.periodic_playtime_ingestion",
        "schedule": 10.0,
    }
}

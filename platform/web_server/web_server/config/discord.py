from dotenv import load_dotenv
import os


load_dotenv()

# used to authenticate between game bot and django server
GAME_DISCORD_BOT_API_KEY = os.environ.get('GAME_DISCORD_BOT_API_KEY')

# used to authenticate with the Discord API
GAME_DISCORD_BOT_API_TOKEN = os.environ.get('GAME_DISCORD_BOT_API_TOKEN')

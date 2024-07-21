from dotenv import load_dotenv
import os


load_dotenv()

BOT_TOKEN = os.getenv('GAME_BOT_TOKEN')

DEBUG = (os.environ.get("DEBUG", 'FALSE') == 'TRUE')

PLATFORM_API_KEY = os.getenv('PLATFORM_API_KEY')
PLATFORM_HOSTNAME = os.getenv('PLATFORM_HOSTNAME')
PLATFORM_ENDPOINT = os.getenv('PLATFORM_ENDPOINT')
PLATFORM_URL = PLATFORM_HOSTNAME + PLATFORM_ENDPOINT

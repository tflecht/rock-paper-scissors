from dotenv import load_dotenv
import os

load_dotenv()

# https://reinout.vanrees.org/weblog/2017/03/08/logging-verbosity-managment-commands.html
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.getenv('LOG_LEVEL', 'WARNING'),
    },
}

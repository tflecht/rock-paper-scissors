from . import retrieve_secrets


def db_settings():
    return retrieve_secrets.get_secret()

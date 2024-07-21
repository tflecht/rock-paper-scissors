from web_server import exceptions, settings

def ensure_settings_compatibility():
    ensure_production_and_debug_compatibility()

def ensure_production_and_debug_compatibility():
    if settings.DEBUG and settings.PRODUCTION:
        raise exceptions.CompatibilityError(f"Can't run in debug mode in production")

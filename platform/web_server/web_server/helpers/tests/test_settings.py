import pytest
from pytest import raises

from web_server import exceptions, settings
from web_server.helpers import check


def test_running_without_debug_and_without_production_succeeds():
    settings.DEBUG = False 
    settings.PRODUCTION = False
    check.ensure_settings_compatibility()

def test_running_with_debug_and_without_production_succeeds():
    settings.DEBUG = True
    settings.PRODUCTION = False
    check.ensure_settings_compatibility()

def test_running_without_debug_and_with_production_succeeds():
    settings.DEBUG = False 
    settings.PRODUCTION = True 
    check.ensure_settings_compatibility()

def test_running_with_debug_and_with_production_fails():
    with raises(exceptions.CompatibilityError):
        settings.DEBUG = settings.PRODUCTION = True
        check.ensure_settings_compatibility()

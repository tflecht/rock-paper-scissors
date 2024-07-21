import pytest

from django.apps import apps
from django.db import connection
from django.db.models.base import ModelBase


from helpers import mixins


APP_NAME = 'test'


@pytest.fixture
def timeframe_model(db) -> mixins.TimeframeModelMixin:
    '''
        The model lookup is needed because if we just make the model every time, there is a warning
        emitted that the model is already registered.
    '''
    #https://stackoverflow.com/questions/4281670/django-best-way-to-unit-test-an-abstract-model
    #https://stackoverflow.com/questions/8702772/django-get-list-of-models-in-application

    model_name = 'timeframe_concrete_model'
    model = None
    app = apps.all_models.get(APP_NAME)
    if app: 
        model = app.get(model_name)

    class Meta:
        def __init__(self, app_label):
            self.app_label = app_label

    if not model:
        model = ModelBase(
            model_name,
            (
                mixins.TimeframeModelMixin,
            ),
            {
                '__module__': mixins.TimeframeModelMixin.__module__,
                'Meta': Meta(APP_NAME),
            },
        )
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(model)
    return model

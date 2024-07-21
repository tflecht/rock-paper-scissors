import typing

# For model-specific QuerySet typing, see:
#    https://stackoverflow.com/questions/42397502/how-to-use-python-type-hints-with-django-queryset

# https://stackoverflow.com/questions/51291722/define-a-jsonable-type-using-mypy-pep-526
JsonBlob = typing.Dict[str, object]
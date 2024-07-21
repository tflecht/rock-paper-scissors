import random
from typing import List, Optional

from django.db.models import Model, QuerySet

from helpers import exceptions


def random_integer(min:int, max:int) -> int:
    """
        Generates a random integer i in the range min <= i < max.
        - `min`: (inclusive)
        - `max`: (exclusive)
    """
    return random.randint(min, max-1)


def select_from_query_set(query_set: QuerySet, generator=None) -> Optional[Model]:
    if not generator:
        generator = random_integer
    if query_set.count() > 0:
        return query_set[generator(0, query_set.count())]
    return None


def select_from_weighted_query_set(query_set: QuerySet, weights: int) -> Optional[Model]:
    if query_set.count() > 0:
        return random.choices(query_set, weights)[0]
    return None


def select_n_from_query_set(
        query_set: QuerySet,
        *,
        number_of_selections: int,
) -> QuerySet:
    ids = list(query_set.values_list('id', flat=True))
    selections = _select_distinct_ids_from(ids, number_of_selections)
    return query_set.filter(id__in=selections)


def _select_distinct_ids_from(selections: List[int], number_of_selections) -> List[int]:
    if number_of_selections > len(selections):
        raise exceptions.MoreSelectionsThanOptions
    return random.sample(selections, number_of_selections)

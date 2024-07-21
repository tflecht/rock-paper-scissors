import typing
from itertools import islice


def batch(sequence: typing.Iterable, *, size: int):
    if size < 1:
        raise ValueError('Size must be greater than 0')
    it = iter(sequence)
    while (batch := list(islice(it, size))):
        yield batch

from typing import List


def integer_sequence_generator(sequence: List[int]):
    return IntegerGenerator(sequence)


class IntegerGenerator(object):
    def __init__(self, sequence: List[int]):
        if len(sequence) == 0:
            raise Exception("can't generate from an empty sequence")
        self.counter = 0
        self.sequence = sequence

    def __call__(self, *args):
        print('generator')
        idx = self.counter % len(self.sequence)
        self.counter += 1
        return self.sequence[idx]

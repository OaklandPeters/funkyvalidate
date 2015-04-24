import functools
import pdb

def splat(fn):
    """
    Combinator. ~Decorator turning another function into a mapper.
    """
    @functools.wraps(fn)
    def wrapped(iterable):
        return map(fn, iterable)
    return wrapped


def get(attr):
    """ record.__getitem__(attr) """
    def wrapped(record):
        return record[attr]
    return wrapped

inventories = [
  { 'apples': 0, 'oranges': 144, 'eggs': 36 },
  { 'apples': 240, 'oranges': 54, 'eggs': 12 },
  { 'apples': 24, 'oranges': 12, 'eggs': 42 }
]
assert get('apples')(inventories[0]) == 0

assert splat(get('oranges'))(inventories) == [144, 54, 12]

def _and(left):
    """ ~ currying for and operation """
    def wrapped(right):
        return bool(left) && bool(right)

def _or(left):
    def wrapped(right):
        return bool(left) or bool(right)

def _not(left):
    return not bool(left)

def checker(fn):
    """Combinator for isinstance check,
    fn: logical function"""
    @functools.wraps(fn)
    def wrapper():
        """terms: logical functions """

        def wrapped(*):


checker(Sequence)(_and)()

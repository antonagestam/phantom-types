from phantom.interval import Exclusive
from phantom.interval import ExclusiveInclusive
from phantom.interval import Inclusive
from phantom.interval import InclusiveExclusive


class Inc(float, Inclusive, low=0, high=100):
    ...


class Exc(int, Exclusive, low=0, high=100):
    ...


class IncExc(float, InclusiveExclusive, low=0, high=100):
    ...


class ExcInc(int, ExclusiveInclusive, low=0, high=100):
    ...

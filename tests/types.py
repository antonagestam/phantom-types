from phantom.interval import Exclusive
from phantom.interval import ExclusiveInclusive
from phantom.interval import Inclusive
from phantom.interval import InclusiveExclusive


class FloatInc(float, Inclusive, low=0, high=100): ...


class IntInc(int, Inclusive, low=0, high=100): ...


class FloatExc(float, Exclusive, low=0, high=100): ...


class IntExc(int, Exclusive, low=0, high=100): ...


class FloatIncExc(float, InclusiveExclusive, low=0, high=100): ...


class IntIncExc(int, InclusiveExclusive, low=0, high=100): ...


class FloatExcInc(float, ExclusiveInclusive, low=0, high=100): ...


class IntExcInc(int, ExclusiveInclusive, low=0, high=100): ...

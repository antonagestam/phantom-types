from typing import Protocol
from typing import TypeVar

T_contra = TypeVar("T_contra", contravariant=True)
U_co = TypeVar("U_co", covariant=True)


class SupportsLt(Protocol[T_contra]):
    def __lt__(self, other: T_contra) -> bool:
        ...


class SupportsLe(Protocol[T_contra]):
    def __le__(self, other: T_contra) -> bool:
        ...


class SupportsGt(Protocol[T_contra]):
    def __gt__(self, other: T_contra) -> bool:
        ...


class SupportsGe(Protocol[T_contra]):
    def __ge__(self, other: T_contra) -> bool:
        ...


class SupportsEq(Protocol):
    def __eq__(self, other: object) -> bool:
        ...


class Comparable(
    SupportsLt[T_contra],
    SupportsLe[T_contra],
    SupportsGt[T_contra],
    SupportsGe[T_contra],
    SupportsEq,
    Protocol[T_contra],
):
    ...


class SupportsLeGe(SupportsLe[T_contra], SupportsGe[T_contra], Protocol[T_contra]):
    ...


class SupportsLeGt(SupportsLe[T_contra], SupportsGt[T_contra], Protocol[T_contra]):
    ...


class SupportsLtGe(SupportsLt[T_contra], SupportsGe[T_contra], Protocol[T_contra]):
    ...


class SupportsLtGt(SupportsLt[T_contra], SupportsLeGt[T_contra], Protocol[T_contra]):
    ...


class SupportsMod(Protocol[T_contra, U_co]):
    def __mod__(self, other: T_contra) -> U_co:
        ...

from typing import TypeVar

from numerary.types import CachingProtocolMeta  # type: ignore[attr-defined]
from typing_extensions import Protocol
from typing_extensions import runtime_checkable

T_contra = TypeVar("T_contra", contravariant=True)
U_co = TypeVar("U_co", covariant=True)


@runtime_checkable
class _SupportsLt(Protocol[T_contra]):
    def __lt__(self, other: T_contra) -> bool:
        ...


class SupportsLt(
    _SupportsLt[T_contra],
    Protocol[T_contra],
    metaclass=CachingProtocolMeta,
):
    ...


@runtime_checkable
class _SupportsLe(Protocol[T_contra]):
    def __le__(self, other: T_contra) -> bool:
        ...


class SupportsLe(
    _SupportsLe[T_contra],
    Protocol[T_contra],
    metaclass=CachingProtocolMeta,
):
    ...


@runtime_checkable
class _SupportsGt(Protocol[T_contra]):
    def __gt__(self, other: T_contra) -> bool:
        ...


class SupportsGt(
    _SupportsGt[T_contra],
    Protocol[T_contra],
    metaclass=CachingProtocolMeta,
):
    ...


@runtime_checkable
class _SupportsGe(Protocol[T_contra]):
    def __ge__(self, other: T_contra) -> bool:
        ...


class SupportsGe(
    _SupportsGe[T_contra],
    Protocol[T_contra],
    metaclass=CachingProtocolMeta,
):
    ...


@runtime_checkable
class _SupportsEq(Protocol):
    def __eq__(self, other: object) -> bool:
        ...


class SupportsEq(Protocol, metaclass=CachingProtocolMeta):
    ...


@runtime_checkable
class _Comparable(
    SupportsLt[T_contra],
    SupportsLe[T_contra],
    SupportsGt[T_contra],
    SupportsGe[T_contra],
    SupportsEq,
    Protocol[T_contra],
):
    ...


class Comparable(
    _Comparable[T_contra],
    Protocol[T_contra],
    metaclass=CachingProtocolMeta,
):
    ...


@runtime_checkable
class _SupportsLeGe(SupportsLe[T_contra], SupportsGe[T_contra], Protocol[T_contra]):
    ...


class SupportsLeGe(
    _SupportsLeGe[T_contra],
    Protocol[T_contra],
    metaclass=CachingProtocolMeta,
):
    ...


@runtime_checkable
class _SupportsLeGt(SupportsLe[T_contra], SupportsGt[T_contra], Protocol[T_contra]):
    ...


class SupportsLeGt(
    _SupportsLeGt[T_contra],
    Protocol[T_contra],
    metaclass=CachingProtocolMeta,
):
    ...


@runtime_checkable
class _SupportsLtGe(SupportsLt[T_contra], SupportsGe[T_contra], Protocol[T_contra]):
    ...


class SupportsLtGe(
    _SupportsLtGe[T_contra],
    Protocol[T_contra],
    metaclass=CachingProtocolMeta,
):
    ...


class _SupportsLtGt(SupportsLt[T_contra], SupportsGt[T_contra], Protocol[T_contra]):
    ...


class SupportsLtGt(
    _SupportsLtGt[T_contra],
    Protocol[T_contra],
    metaclass=CachingProtocolMeta,
):
    ...


@runtime_checkable
class _SupportsMod(Protocol[T_contra, U_co]):
    def __mod__(self, other: T_contra) -> U_co:
        ...


class SupportsMod(
    _SupportsMod[T_contra, U_co],
    Protocol[T_contra, U_co],
    metaclass=CachingProtocolMeta,
):
    ...

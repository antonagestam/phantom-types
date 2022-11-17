from typing import TYPE_CHECKING

# Workaround for mypy crash, see:
#   https://github.com/antonagestam/phantom-types/issues/243
if TYPE_CHECKING:

    class CachingProtocolMeta(type):
        ...

else:
    try:
        from numerary.protocol import CachingProtocolMeta
    except ImportError:
        from numerary.types import CachingProtocolMeta


__all__ = ("CachingProtocolMeta",)

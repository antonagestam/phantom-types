"""
Use ``Phantom`` to create arbitrary phantom types using boolean predicates.

.. code-block:: python

    from phantom import Phantom


    def is_big(value: int) -> bool:
        return value > 5


    class Big(int, Phantom, predicate=is_big):
        ...


    assert isinstance(10, Big)  # this passes
"""
from ._base import Phantom
from ._base import PhantomBase
from ._base import PhantomMeta
from .bounds import get_bound_parser
from .errors import BoundError
from .predicates import Predicate

__version__ = "1.0.0"
__all__ = (
    "BoundError",
    "Phantom",
    "PhantomBase",
    "PhantomMeta",
    "get_bound_parser",
    "Predicate",
)

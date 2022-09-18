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
from ._base import BoundError
from ._base import Phantom
from ._base import PhantomBase
from ._base import PhantomMeta
from ._base import get_bound_parser
from .predicates import Predicate

__version__ = "0.17.1"
__all__ = (
    "BoundError",
    "Phantom",
    "PhantomBase",
    "PhantomMeta",
    "get_bound_parser",
    "Predicate",
)

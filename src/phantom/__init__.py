"""
Use ``Phantom`` to create arbitrary phantom types using boolean predicates.

.. code-block:: python

    import phantom


    def is_big(value: int) -> bool:
        return value > 5


    class Big(int, Phantom, predicate=is_big):
        ...


    assert isinstance(10, Big)  # this passes
"""
from .base import Phantom
from .base import PhantomBase
from .base import PhantomMeta
from .base import get_bound_parser
from .predicates.base import Predicate

__version__ = "0.14.0"
__all__ = ("PhantomBase", "Phantom", "Predicate", "get_bound_parser", "PhantomMeta")

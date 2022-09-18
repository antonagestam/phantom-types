Pydantic Support
================

phantom-types supports pydantic_ out of the box by providing a
:func:`__get_validators__() <phantom.Phantom.__get_validators__>` hook
on the base :class:`Phantom <phantom.Phantom>` class. Most of the shipped types also
implements full JSON Schema and OpenAPI support.

.. _pydantic: https://pydantic-docs.helpmanual.io/

To make a phantom type compatible with pydantic, all you need to do is override
:func:`Phantom.__schema__() <phantom.Phantom.__schema__>`:

.. code-block:: python

    from phantom import Phantom
    from phantom.schema import Schema


    class Name(str, Phantom, predicate=...):
        @classmethod
        def __schema__(cls) -> Schema:
            return super().__schema__() | Schema(
                description="A type for names",
                format="name-format",
            )

As can be seen in the example, ``__schema__()`` implementations are expected to return a
dict extending its ``super().__schema__()``, however this is not a requirement and any
:class:`Schema <phantom.schema.Schema>`-compatible ``dict`` can be returned.

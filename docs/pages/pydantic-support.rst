Pydantic Support
================

phantom-types supports pydantic_ out of the box by providing
:func:`__get_pydantic_core_schema__() <phantom.Phantom.__get_pydantic_core_schema__>`
and :func:`__get_pydantic_json_schema__() <phantom.schema.SchemaField.__get_pydantic_json_schema__>`
hooks on the base :class:`Phantom <phantom.Phantom>` class. Most of the shipped types also
implement full JSON Schema and OpenAPI support.

.. _pydantic: https://docs.pydantic.dev/

To customize the JSON schema representation of a phantom type, override
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

.. note::

    phantom-types 3.0.2 supported Pydantic v1 via the ``__get_validators__()`` hook.
    As of phantom-types 3.1.0, only Pydantic v2 is supported. If you need Pydantic v1
    support, pin to ``phantom-types<3.1``.

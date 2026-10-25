Pydantic Support
================

phantom-types supports pydantic_ out of the box by providing
:func:`__get_pydantic_core_schema__() <phantom.Phantom.__get_pydantic_core_schema__>`
and
:func:`__get_pydantic_json_schema__() <phantom.Phantom.__get_pydantic_json_schema__>`
hooks on the base :class:`Phantom <phantom.Phantom>` class. Most of the shipped types
also implement full JSON Schema and OpenAPI support.

.. _pydantic: https://docs.pydantic.dev/

pydantic first decodes input into the bound of a phantom type, by its own rules and
respecting its strict mode, and then passes the decoded value to the type's
:func:`parse() <phantom.Phantom.parse>` method. Every value a field produces is
therefore a valid instance of the phantom type. A
:class:`TZAware <phantom.datetime.TZAware>` field, for instance, parses strings with
pydantic's datetime parser, and doesn't need python-dateutil. Parametrized types like
``NonEmpty[int]`` decode into a tuple of their type argument. A ``TypeError`` raised by
``parse()`` is reported as a validation error of type ``type_error``.

The JSON schema of a phantom type is the schema of what it decodes into, extended with
the keys returned from :func:`Phantom.__schema__() <phantom.Phantom.__schema__>`. To
customize it, override ``__schema__()``:

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

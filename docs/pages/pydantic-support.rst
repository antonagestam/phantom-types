Pydantic Support
================

phantom-types supports pydantic_ out of the box by providing a
:func:`__get_validators__() <phantom.Phantom.__get_validators__>` hook
on the base :class:`Phantom <phantom.Phantom>` class. Most of the shipped types also
implements full JSON Schema and OpenAPI support.

.. _pydantic: https://pydantic-docs.helpmanual.io/

To make a phantom type compatible with pydantic, all you need to do is override
:func:`Phantom.__schema__() <phantom.Phantom.__schema__>`::

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

Caveats
-------

Sized containers are currently only partially supported. Their validation is accurate
but their schemas aren't propagating their inner type. This likely won't be possible to
support until pydantic exposes its ``ModelField`` to ``__modify_schema__``. To work
around this subclasses of :class:`PhantomSized <phantom.sized.PhantomSized>` can specify
``"items"`` like so::

    class LimitedSize(PhantomSized[int], len=numeric.greater(10)):
        @classmethod
        def __schema__(cls) -> Schema:
            return super().__schema__() | Schema(
                minItems=10,
                items={"type": "integer"},
            )

As seen in the example, phantom sized types also currently need to manually specify
``"minItems"`` and ``"maxItems"``. This is planned to be remedied by introducing an
intermediary ``BoundedSize`` type that provides introspection capabilities for those
attributes.

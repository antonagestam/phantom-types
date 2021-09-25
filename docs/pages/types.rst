.. _types:

Types
=====

Base classes
------------

.. automodule:: phantom

.. autoclass:: Phantom
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :special-members: __schema__, __modify_schema__, __get_validators__, __bound__

Boolean
-------

.. automodule:: phantom.boolean
    :members:
    :undoc-members:
    :show-inheritance:

Country codes
-------------

.. automodule:: phantom.iso3166
    :members:
    :undoc-members:
    :show-inheritance:

Datetime
--------

.. automodule:: phantom.datetime
    :members:
    :undoc-members:
    :show-inheritance:

.. _numeric-intervals:

Numeric intervals
-----------------

.. automodule:: phantom.interval

Base classes
^^^^^^^^^^^^

.. autoclass:: phantom.interval.Interval
    :members: __check__
    :undoc-members:
    :show-inheritance:

.. autoclass:: phantom.interval.Open
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: phantom.interval.Closed
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: phantom.interval.OpenClosed
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: phantom.interval.ClosedOpen
    :members:
    :undoc-members:
    :show-inheritance:

Concrete interval types
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: phantom.interval.Natural
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: phantom.interval.NegativeInt
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: phantom.interval.Portion
    :members:
    :undoc-members:
    :show-inheritance:

Regular expressions
-------------------

.. automodule:: phantom.re
    :members:
    :undoc-members:
    :show-inheritance:

Sized collections
-----------------

.. automodule:: phantom.sized
    :members:
    :undoc-members:
    :show-inheritance:

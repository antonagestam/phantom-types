External wrappers
=================

A collection of phantom types that wraps functionality of well maintained
implementations of third-party validation libraries. Importing from ``phantom.ext.*``
should be a hint that more dependencies need to be installed.

Phone numbers
-------------

.. automodule:: phantom.ext.phonenumbers

Types
^^^^^

.. autoclass:: phantom.ext.phonenumbers.PhoneNumber
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: phantom.ext.phonenumbers.FormattedPhoneNumber
    :members:
    :undoc-members:
    :show-inheritance:

Functions
^^^^^^^^^

.. autofunction:: phantom.ext.phonenumbers.is_phone_number

.. autofunction:: phantom.ext.phonenumbers.is_formatted_phone_number

.. autofunction:: phantom.ext.phonenumbers.normalize_phone_number


Exceptions
^^^^^^^^^^

.. autoexception:: phantom.ext.phonenumbers.InvalidPhoneNumber
    :show-inheritance:

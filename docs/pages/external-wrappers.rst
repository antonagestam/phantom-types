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

Country codes
-------------

.. automodule:: phantom.ext.iso3166

Types
^^^^^

.. autoclass:: phantom.ext.iso3166.Alpha2
    :members:
    :undoc-members:
    :show-inheritance:

Functions
^^^^^^^^^

.. autofunction:: phantom.ext.iso3166.normalize_alpha2_country_code

Exceptions
^^^^^^^^^^

.. autoexception:: phantom.ext.iso3166.InvalidCountryCode
    :show-inheritance:

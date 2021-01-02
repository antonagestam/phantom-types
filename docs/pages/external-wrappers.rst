External wrappers
=================

A collection of phantom types that wraps functionality of well maintained
implementations of third-party validation libraries. Importing from ``phantom.ext.*``
should be a hint that more dependencies need to be installed.

Phone numbers
-------------

``phantom.ext.phonenumbers.*``

Requires the phonenumbers_ package which can be installed with:

.. _phonenumbers: https://pypi.org/project/phonenumbers/

.. code-block:: bash

    $ python3 -m pip install phantom-types[phonenumbers]

Types
^^^^^

* ``PhoneNumber``
* ``FormattedPhoneNumber``
   * ``FormattedPhoneNumber.parse()`` normalizes numbers using
     ``PhoneNumberFormat.E164`` and raises ``InvalidPhoneNumber``.

Functions
^^^^^^^^^

* ``is_phone_number: Predicate[str]``
* ``is_formatted_phone_number: Predicate[str]``
* ``normalize_phone_number(phone_number: str, country_code: Optional[str]=None) -> FormattedPhoneNumber``
  normalizes numbers using ``PhoneNumberFormat.E164`` and raises ``InvalidPhoneNumber``.

Exceptions
^^^^^^^^^^

* ``InvalidPhoneNumber``

Country codes
-------------

``phantom.ext.iso3166.*``

Requires the iso3166_ package which can be installed with:

.. _iso3166: https://pypi.org/project/iso3166/

.. code-block:: bash

    $ python3 -m pip install phantom-types[iso3166]

Types
^^^^^

* ``Alpha2``
  - ``Alpha2.parse()`` normalizes mixed case codes.
* ``CountryCode`` alias of ``Alpha2``

Functions
^^^^^^^^^

* ``normalize_alpha2_country_code(country_code: str) -> Alpha2`` normalizes mixed case
  country codes and raises ``InvalidCountryCode``.

Exceptions
^^^^^^^^^^

* ``InvalidCountryCode``


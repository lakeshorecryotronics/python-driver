.. _installation:

Installation
============

Python version
--------------
The Lake Shore Python driver is compatible with Python 2.7 and above. We recommend using the latest version of Python 3.

Dependencies
------------
The following distributions will be installed automatically when installing LakeShore:
* `pySerial`_ is a package that provides tools for serial communications. It is used to talk to the instruments over a USB connection.
* `iso8601`_ is a simple module that parses ISO 8601 formatted data strings into Python datetime objects.

.. _pySerial: https://pythonhosted.org/pyserial/
.. _iso8601: https://pypi.org/project/iso8601/

Install the Lake Shore Python driver
------------------------------------
To install the driver simply open a terminal (command prompt) window and type::

    pip install lakeshore

The driver is now installed! Now take a look through :ref:`getting_started` to begin communicating with your instrument(s).

If you are using Python 2 you may need to `install pip`_.

.. _install pip: https://www.w3schools.com/python/python_pip.asp
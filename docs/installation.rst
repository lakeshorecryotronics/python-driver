.. _installation:

Installation
============

Python version
--------------
The Lake Shore Python driver is compatible with Python 3.7 and above.

Install the Lake Shore Python driver
------------------------------------
To install the driver simply open a terminal (command prompt) window and type::

    pip install lakeshore


Installing the driver through Spyder
----------------------------------------------------------
The driver can be installed directly within the Spyder IDE. To do this, first ensure that Spyder is using
version 7.3 or greater of IPython. You can check the version by looking at the console window when opening the IDE,
see image below for details:

.. image:: _static/IPython_info.PNG

If the version is below 7.3, open an anaconda prompt and type::

    pip install IPython --upgrade

Back in the Spyder console, type::

    pip install lakeshore

The driver is now installed! Now take a look through :ref:`getting_started` to begin communicating with your instrument(s).

Updating the driver
^^^^^^^^^^^^^^^^^^^

If you have an old version of the Lake Shore Python driver and want to upgrade to the newest version, open
a terminal (command prompt) window and type::

    pip install --upgrade lakeshore



.. _install pip: https://www.w3schools.com/python/python_pip.asp
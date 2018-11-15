.. _getting_started:

Getting Started
===============
This page assumes that you have completed :ref:`installation` of the Lake Shore Python driver. It is intended to give a basic understanding of how to use the driver to communicate with an instrument.

A simple example
----------------
::

    from lakeshore import PrecisionSource

    my_instrument = PrecisionSource()
    print(my_instrument.query('*IDN?'))

Making Connections
------------------
Connecting to a specific instrument
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The driver attempts to connect to an instrument when an instrument class object is created. When no arguments are passed, the driver will connect to the first available instrument.

If multiple instruments are connected you may target a specific device in one of two ways. Either by specifying the serial number of the instrument::

    from lakeshore import Teslameter

    my_specific_instrument = Teslameter(serial_number='LSA12AB')

or the COM port it is connected to::

    from lakeshore import FastHall

    my_specific_instrument = FastHall(com_port='COM7')

Connecting over TCP
~~~~~~~~~~~~~~~~~~~
By default, the driver will try to connect to the instrument over a serial USB connection.

Connecting to an instrument over TCP requires knowledge of its IP address. On a XIP instrument the IP address can be found through the front panel interface and used like so::

    from lakeshore import PrecisionSource

    my_network_connected_instrument = PrecisionSource(ip_address='10.1.2.34')

Commands and queries
--------------------
All Lake Shore instruments supported by the Python driver have :func:`~lakeshore.xip_instrument.command` and :func:`~lakeshore.xip_instrument.query` methods.

The Python driver makes it simple to send the instrument a command or query::

    from lakeshore import PrecisionSource

    my_instrument = PrecisionSource()

    my_instrument.command('SOURCE:FUNCTION:MODE SIN')
    print(my_instrument.query('SOURCE:FUNCTION:MODE?'))

Grouping multiple commands & queries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To simplify, speed up, or simultaneously send multiple commands or queries simply separate them with commas::

    from lakeshore import Teslameter

    my_instrument = Teslameter()
    # Set the averaging window to 250 ms, get the dC field measurement, and get the temperature measurement.
    response = my_instrument.query('SENSE:AVERAGE:COUNT 25', 'FETCH:DC?', 'FETCH:TEMP?')

The commands will execute in the order they are listed. The response to each query will be delimited by semicolons in the order they are listed.

Checking for SCPI errors
~~~~~~~~~~~~~~~~~~~~~~~~
Both the command and query methods will automatically check the SCPI error queue for invalid commands or parameters. If you would like to disable error checking, such as in situations where you need a faster response rate, it can be turned off with an optional argument::

    from lakeshore import Teslameter

    my_instrument = Teslameter()
    z_axis_measurement = my_instrument.query('FETCH:DC? Z', check_errors=False)


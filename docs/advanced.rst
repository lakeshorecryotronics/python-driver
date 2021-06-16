.. _advanced:

Advanced
========

Thread Safety
-------------

While an instrument can only be instantiated once, all methods on an instrument are thread safe. Multiple python treads with a reference to an instrument may simultaneously call the instrument methods.

Logging
-------

For debugging your application, it can be useful to see a log of transactions with the instrument(s). All commands/queries are logged to a logger named *lakeshore*.

For example, you can print this log to stdout like this::

    import logging
    import sys

    lake_shore_log = logging.getLogger('lakeshore')
    lake_shore_log.addHandler(logging.StreamHandler(stream=sys.stdout))
    lake_shore_log.setLevel(logging.INFO)

Status Registers
----------------
Every XIP instrument implements the SCPI status system which is derived from the status system called out in chapter 11 of the IEEE 488.2 standard. This system is useful for efficiently monitoring the state of an instrument. However the system is also fairly complex. Refer to the instrument manual available on `our website`_ before diving in.

.. _our website: https://www.lakeshore.com

Reading a register
~~~~~~~~~~~~~~~~~~
Each register and register mask can be read by a corresponding *get* function. The function returns an object that contains the state of each register bit. For example::

    from lakeshore import Teslameter

    my_instrument = Teslameter()
    print(dut.get_operation_events())

will return the following::

    {'no_probe': False, 'overload': False, 'ranging': False, 'ramp_done': False, 'no_data_on_breakout_adapter': False}

Modifying a register mask
~~~~~~~~~~~~~~~~~~~~~~~~~
Modifying a register mask can be done in one of two ways. Either by using the *modify* functions like so::

    from lakeshore import PrecisionSource

    my_instrument = PrecisionSource()
    my_instrument.modify_standard_event_register_mask('command_error', True)

or by using the *set* functions to define the states of all bits in the register::

    from lakeshore import PrecisionSource, PrecisionSourceQuestionableRegister

    my_instrument = PrecisionSource()
    register_mask = PrecisionSourceQuestionableRegister(voltage_source_in_current_limit=True,
                                         current_source_in_voltage_compliance=True,
                                         calibration_error=False,
                                         inter_processor_communication_error=False)

    my_instrument.set_questionable_event_enable_mask(register_mask)

Instrument initialization options
---------------------------------
Keep communication errors on initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
By default the error flags or queue will be reset upon connecting to an instrument. If this behavior is not desired use the following optional parameter like so::

        from lakeshore import Teslameter

        my_instrument = Teslameter(clear_errors_on_init=False)

Python 2 compatibility
----------------------
Python 2 is no longer supported by the python software foundation. The most recent version of this driver that is fully compatible with python 2 is version 1.4.
If your application requires the use of the python 2 interpreter, use version 1.4.

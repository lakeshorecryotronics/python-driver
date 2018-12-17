.. _advanced:

Advanced Functions
==================
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

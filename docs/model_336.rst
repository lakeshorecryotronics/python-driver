.. _model_336:

Model 336 Cryogenic Temperature Controller
==========================================
The Model 336 measures and controls cryogenic temperature environments.

More information about the instrument can be found `on our website`_ including the manual which has a list of all commands and queries.

.. _on our website: https://www.lakeshore.com/products/categories/overview/temperature-products/cryogenic-temperature-controllers/model-335-cryogenic-temperature-controller

Example Scripts
===============
Below are a few example scripts for the Model 336 that use the Lake Shore Python driver.

Using calibration curves with a temperature instrument
------------------------------------------------------
.. literalinclude:: examples/temperature_monitor_curve_example.py

Setting up heater outputs on the Model 336
------------------------------------------
.. literalinclude:: examples/336_heater_setup_example.py

Instrument methods
------------------
.. module:: lakeshore.model_336

.. autoclass:: Model336
    :member-order: bysource
    :members:
    :inherited-members:

Instrument Classes
------------------
This page outlines the classes used to interact with methods which return or
accept an argument of a class object, specific to the Lake Shore model 336.

.. autoclass:: Model336InputSensorSettings
    :members:

    .. automethod:: __init__

.. autoclass:: Model336ControlLoopZoneSettings
    :members:

    .. automethod:: __init__

.. autoclass:: Model336AlarmSettings
    :members:

    .. automethod:: __init__

.. autoclass:: Model336CurveHeader
    :members:

    .. automethod:: __init__

Enum classes for the model 336
------------------------------
This page describes the Enum type objects that have been created to represent
various settings of the model 336 that are used as an argument or return to
the instrument. The purpose of these enum types is to make the settings more
descriptive and obvious to the user rather than interpreting the ints taken by
the instrument.

.. autoclass:: Model336InputChannel
    :members:
    :undoc-members:

.. autoclass:: Model336DisplaySetupMode
    :members:
    :undoc-members:

.. autoclass:: Model336DisplaySetupCustom
    :members:
    :undoc-members:

.. autoclass:: Model336DisplaySetupAllInputs
    :members:
    :undoc-members:

.. autoclass:: Model336InputSensorType
    :members:
    :undoc-members:

.. autoclass:: Model336DiodeRange
    :members:
    :undoc-members:

.. autoclass:: Model336RTDRange
    :members:
    :undoc-members:

.. autoclass:: Model336ThermocoupleRange
    :members:
    :undoc-members:

.. autoclass:: Model336HeaterOutputMode
    :members:
    :undoc-members:

.. autoclass:: Model336HeaterRange
    :members:
    :undoc-members:

.. autoclass:: Model336HeaterVoltageRange
    :members:
    :undoc-members:

.. autoclass:: Model336DisplayUnits
    :members:
    :undoc-members:

.. autoclass:: Model336RelayControlMode
    :members:
    :undoc-members:

.. autoclass:: Model336RelayControlAlarm
    :members:
    :undoc-members:

.. autoclass:: Model336InterfaceMode
    :members:
    :undoc-members:

.. autoclass:: Model336HeaterError
    :members:
    :undoc-members:

.. autoclass:: Model336CurveFormat
    :members:
    :undoc-members:

.. autoclass:: Model336CurveTemperatureCoefficients
    :members:
    :undoc-members:

.. autoclass:: Model336AutoTuneMode
    :members:
    :undoc-members:

.. autoclass:: Model336HeaterResistance
    :members:
    :undoc-members:

.. autoclass:: Model336Polarity
    :members:
    :undoc-members:

.. autoclass:: Model336DiodeCurrent
    :members:
    :undoc-members:

.. autoclass:: Model336HeaterOutputUnits
    :members:
    :undoc-members:

.. autoclass:: Model336InputSensorUnits
    :members:
    :undoc-members:

.. autoclass:: Model336ControlTypes
    :members:
    :undoc-members:

.. autoclass:: Model336LanStatus
    :members:
    :undoc-members:

.. autoclass:: Model336Interface
    :members:
    :undoc-members:

.. autoclass:: Model336CurveHeader
    :members:
    :undoc-members:

.. autoclass:: Model336AlarmSettings
    :members:
    :undoc-members:

Register classes used with the model 335
----------------------------------------
This page describes the register objects. Each bit in the register
is represented as a member of the register's class

.. autoclass:: Model336StandardEventRegister
    :members:
    :undoc-members:

.. autoclass:: Model336StatusByteRegister
    :members:
    :undoc-members:

.. autoclass:: Model336ServiceRequestEnable
    :members:
    :undoc-members:

.. autoclass:: Model336OperationEvent
    :members:
    :undoc-members:

.. autoclass:: Model336InputReadingStatus
    :members:
    :undoc-members:

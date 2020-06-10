.. _model_372:

Model 372 AC Resistance Bridge
==============================
The Model 372 is both an AC resistance bridge and temperature controller designed for measurements below 100 milliKelvin.

More information about the instrument can be found `on our website`_ including the manual which has a list of all commands and queries.

.. _on our website: https://www.lakeshore.com/products/categories/overview/temperature-products/ac-resistance-bridges/model-372-ac-resistance-bridge-temperature-controller

Example Scripts
===============
Below are a few example scripts for the Model 372 that use the Lake Shore Python driver.

Using enums to configure an input sensor
----------------------------------------
.. literalinclude:: examples/372_input_setup_example.py

Setting up a control loop with the model 372
--------------------------------------------
.. literalinclude:: examples/372_control_loop_example.py


Instrument methods
------------------
.. module:: lakeshore.model_372

.. autoclass:: Model372
    :member-order: bysource
    :members:
    :inherited-members:

Instrument classes
------------------
This page describes the classes used throughout the 372 methods to interact
with instrument settings and other methods that use objects and classes.

.. autoclass:: Model372InputChannelSettings
    :members:

    .. automethod:: __init__

.. autoclass:: Model372InputSetupSettings
    :members:

    .. automethod:: __init__

.. autoclass:: Model372HeaterOutputSettings
    :members:

    .. automethod:: __init__

.. autoclass:: Model372ControlLoopZoneSettings
    :members:

    .. automethod:: __init__

.. autoclass:: Model372AlarmParameters
    :members:

    .. automethod:: __init__

.. autoclass:: Model372CurveHeader
    :members:

    .. automethod:: __init__

.. autoclass:: CurveHeader
    :members:

    .. automethod:: __init__

.. autoclass:: Model372StandardEventRegister
    :members:

.. autoclass:: StandardEventRegister
    :members:

.. autoclass:: Model372ReadingStatusRegister
    :members:

.. autoclass:: Model372StatusByteRegister
    :members:

.. autoclass:: Model372ServiceRequestEnable
    :members:

Enum Types
----------
This page describes the Enum type objects that have been created to represent
various settings of the model 372 that are inputted as an int or single character
to the instrument. The purpose of these enum types is to make the settings more
descriptive and obvious to the user rather than interpreting the ints taken by
the instrument.

.. autoclass:: Model372OutputMode
    :members:
    :undoc-members:

.. autoclass:: Model372InputChannel
    :members:
    :undoc-members:

.. autoclass:: Model372SensorExcitationMode
    :members:
    :undoc-members:

.. autoclass:: Model372AutoRangeMode
    :members:
    :undoc-members:

.. autoclass:: Model372InputSensorUnits
    :members:
    :undoc-members:

.. autoclass:: Model372MonitorOutputSource
    :members:
    :undoc-members:

.. autoclass:: Model372RelayControlMode
    :members:
    :undoc-members:

.. autoclass:: Model372DisplayMode
    :members:
    :undoc-members:

.. autoclass:: Model372DisplayInfo
    :members:
    :undoc-members:

.. autoclass:: Model372CurveFormat
    :members:
    :undoc-members:

.. autoclass:: Model372DisplayFieldUnits
    :members:
    :undoc-members:

.. autoclass:: Model372SampleHeaterOutputRange
    :members:
    :undoc-members:

.. autoclass:: Model372InputFrequency
    :members:
    :undoc-members:

.. autoclass:: Model372MeasurementInputVoltageRange
    :members:
    :undoc-members:

.. autoclass:: Model372MeasurementInputCurrentRange
    :members:
    :undoc-members:

.. autoclass:: Model372ControlInputCurrentRange
    :members:
    :undoc-members:

.. autoclass:: Model372MeasurementInputResistance
    :members:
    :undoc-members:

.. autoclass:: Model372CurveTemperatureCoefficient
    :members:
    :undoc-members:

.. autoclass:: Model372InterfaceMode
    :members:
    :undoc-members:

.. autoclass:: Model372DisplayFields
    :members:
    :undoc-members:

.. autoclass:: Model372Polarity
    :members:
    :undoc-members:

.. autoclass:: Model372HeaterOutputUnits
    :members:
    :undoc-members:

.. autoclass:: Model372BrightnessLevel
    :members:
    :undoc-members:

.. autoclass:: Model372HeaterError
    :members:
    :undoc-members:

.. autoclass:: Model372HeaterResistance
    :members:
    :undoc-members:

.. autoclass:: Model372Interface
    :members:
    :undoc-members:

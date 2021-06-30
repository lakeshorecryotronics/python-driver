.. _model_372:

Model 372 AC Resistance Bridge
==============================
The Model 372 is both an AC resistance bridge and temperature controller designed for measurements below 100 milliKelvin.

More information about the instrument can be found `on our website`_ including the manual which has a list of all commands and queries.

.. _on our website: https://www.lakeshore.com/products/categories/overview/temperature-products/ac-resistance-bridges/model-372-ac-resistance-bridge-temperature-controller

Example scripts
_______________

Setting a temperature curve
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/temperature_monitor_curve_example.py

Using enums to configure an input sensor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/372_input_setup_example.py

Setting up a control loop with the model 372
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/372_control_loop_example.py

Instrument class methods
________________________

.. module:: lakeshore.model_372

.. autoclass:: Model372
    :member-order: bysource
    :members:
    :inherited-members:

Instrument settings classes and registers
_________________________________________

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

Enumeration objects
___________________
This section describes the Enum type objects that have been created to name
various settings of the model 372 that are represented as an int or single character
to the instrument. The purpose of these objects is to make the settings more
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

.. _model_224:

Model 224 Temperature Monitor
=============================
The Lake Shore Model 224 measures up to 12 temperature sensor channels.

More information about the instrument can be found `on our website`_ including the manual which has a list of all commands and queries.

.. _on our website: https://www.lakeshore.com/products/categories/overview/temperature-products/cryogenic-temperature-monitors/model-224-temperature-monitor

Example Scripts
_______________
Below is an example script for the Model 224 that uses the Lake Shore Python driver.

Configuring the model 224 with a temperature curve
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/temperature_monitor_curve_example.py

Classes and methods
-------------------
Instrument class methods
~~~~~~~~~~~~~~~~~~~~~~~~
.. module:: lakeshore.model_224

.. autoclass:: Model224
    :member-order: bysource
    :members:
    :inherited-members:


Settings classes
~~~~~~~~~~~~~~~~

.. autoclass:: Model224AlarmParameters
    :members:

    .. automethod:: __init__

.. autoclass:: Model224InputSensorSettings
    :members:

    .. automethod:: __init__

.. autoclass:: Model224CurveHeader
    :members:

    .. automethod:: __init__

Status registers
~~~~~~~~~~~~~~~~

.. autoclass:: Model224StandardEventRegister
    :members:
    :undoc-members:

.. autoclass:: Model224ServiceRequestRegister
    :members:
    :undoc-members:

.. autoclass:: Model224StatusByteRegister
    :members:
    :undoc-members:

.. autoclass:: Model224ReadingStatusRegister
    :members:
    :undoc-members:

Enumeration objects
~~~~~~~~~~~~~~~~~~~
This section describes the Enum type objects that have been created to represent
various settings of the Model 224 series that are represented as an int or single character
to the instrument. The purpose of these enum types is to make the settings more
descriptive and obvious to the user rather than interpreting the ints taken by
the instrument.

.. autoclass:: Model224InputSensorType
    :members:
    :undoc-members:

.. autoclass:: Model224InputSensorUnits
    :members:
    :undoc-members:

.. autoclass:: Model224DiodeExcitationCurrent
    :members:
    :undoc-members:

.. autoclass:: Model224DiodeSensorRange
    :members:
    :undoc-members:

.. autoclass:: Model224PlatinumRTDSensorResistanceRange
    :members:
    :undoc-members:

.. autoclass:: Model224NTCRTDSensorResistanceRange
    :members:
    :undoc-members:

.. autoclass:: Model224InterfaceMode
    :members:
    :undoc-members:

.. autoclass:: Model224RemoteInterface
    :members:
    :undoc-members:

.. autoclass:: Model224DisplayFieldUnits
    :members:
    :undoc-members:

.. autoclass:: Model224InputChannel
    :members:
    :undoc-members:

.. autoclass:: Model224DisplayMode
    :members:
    :undoc-members:

.. autoclass:: Model224NumberOfFields
    :members:
    :undoc-members:

.. autoclass:: Model224RelayControlAlarm
    :members:
    :undoc-members:

.. autoclass:: Model224RelayControlMode
    :members:
    :undoc-members:

.. autoclass:: Model224CurveFormat
    :members:
    :undoc-members:

.. autoclass:: Model224CurveTemperatureCoefficients
    :members:
    :undoc-members:

.. autoclass:: Model224SoftCalSensorTypes
    :members:
    :undoc-members:

.. _model_336:

Model 336 Cryogenic Temperature Controller
==========================================
The Model 336 measures and controls cryogenic temperature environments.

More information about the instrument can be found `on our website`_ including the manual which has a list of all commands and queries.

.. _on our website: https://www.lakeshore.com/products/categories/overview/temperature-products/cryogenic-temperature-controllers/model-336-cryogenic-temperature-controller

Example Scripts
_______________
Below are a few example scripts for the Model 336 that use the Lake Shore Python driver.

Using calibration curves with a temperature instrument
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/temperature_monitor_curve_example.py

Setting up heater outputs on the Model 336
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/336_heater_setup_example.py

Instrument class methods
________________________
.. module:: lakeshore.model_336

.. autoclass:: Model336
    :member-order: bysource
    :inherited-members: Model336Enums, TemperatureControllerEnums
    :members:
    :no-index:

Settings classes
________________
This section outlines the classes used to interact with methods which return or
accept an argument of a class object, specific to the Lake Shore model 336.

.. autoclass:: Model336InputSensorSettings
    :members:
    :special-members: __init__

.. autoclass:: Model336ControlLoopZoneSettings
    :members:
    :special-members: __init__

.. autoclass:: Model336AlarmSettings
    :members:
    :special-members: __init__

.. autoclass:: lakeshore.temperature_controllers.AlarmSettings
    :members:
    :special-members: __init__

.. autoclass:: Model336CurveHeader
    :members:
    :special-members: __init__

.. autoclass:: lakeshore.temperature_controllers.CurveHeader
    :members:
    :special-members: __init__

Status Register Classes
_______________________
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

Enumeration objects
___________________
This section describes the Enum type objects that have been created to name
various settings of the Model 336 series that are represented as an int or single character
to the instrument. The purpose of these enum types is to make the settings more
descriptive and obvious to the user rather than interpreting the ints taken by
the instrument.

.. autoclass:: lakeshore.temperature_controllers_enums.TemperatureControllerEnums
    :members:
    :undoc-members:
    :no-index:

.. autoclass:: Model336Enums
    :members:
    :undoc-members:

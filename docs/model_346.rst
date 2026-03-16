.. _model_346:

Model 346 Cryogenic Temperature Controller
==========================================
The Model 346 measures and controls cryogenic temperature environments.

More information about the instrument can be found `on our website`_ including the manual which has a list of all commands and queries.

.. _on our website: https://www.lakeshore.com/products/categories/temperature-products/cryogenic-temperature-controllers

Example Scripts
_______________
Below are a few example scripts for the Model 346 that use the Lake Shore Python driver.

Using calibration curves with a temperature instrument
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/temperature_monitor_curve_example.py

Setting up outputs on the Model 346
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/346_output_setup_example.py

Setting up options cards on the Model 346
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/346_option_card_sensor_setup_example.py

Instrument class methods
________________________
.. module:: lakeshore.model_346

.. autoclass:: Model346
    :member-order: bysource
    :members:
    :inherited-members: Model346Enums

Settings classes
________________
This section outlines the classes used to interact with methods which return or
accept an argument of a class object, specific to the Lake Shore model 346.

.. autoclass:: Model346InputSensorSettings
    :members:
    :special-members: __init__

.. autoclass:: Model346AlarmSettings
    :members:
    :special-members: __init__

.. autoclass:: Model346CurveHeader
    :members:
    :special-members: __init__


Enumeration objects
___________________
This section describes the Enum type objects that have been created to name
various settings of the Model 346 series that are represented as an int or single character
to the instrument. The purpose of these enum types is to make the settings more
descriptive and obvious to the user rather than interpreting the ints taken by
the instrument.

.. autoclass:: Model346Enums
    :members:
    :undoc-members:

Register Classes
________________
This page describes the register objects. Each bit in the register
is represented as a member of the register's class

.. autoclass:: Model346StandardEventRegister
    :members:
    :undoc-members:

.. autoclass:: lakeshore.xip_instrument.StandardEventRegister
    :members:
    :undoc-members:

.. autoclass:: Model346StatusByteRegister
    :members:
    :undoc-members:

.. autoclass:: lakeshore.xip_instrument.StatusByteRegister
    :members:
    :undoc-members:

.. autoclass:: Model346OperationRegister
    :members:
    :undoc-members:

.. autoclass:: Model346QuestionableRegister
    :members:
    :undoc-members:

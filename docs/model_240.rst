.. _model_240:

Model 240 Input Modules
=======================
The 240 Series Input Modules employ distributed PLC control for large scale cryogenic temperature monitoring.

More information about the instrument can be found `on our website`_ including the manual which has a list of all commands and queries.

.. _on our website: https://www.lakeshore.com/products/categories/overview/temperature-products/cryogenic-temperature-modules/240-series-input-modules

Example Scripts
_______________

Model 240 Input Channel Setup Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/240_measurement_setup_example.py

Model 240 Profibus Configuration Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/240_profislot_config_example.py

Instrument class methods
________________________
.. module:: lakeshore.model_240

.. autoclass:: Model240
    :member-order: bysource
    :members:
    :inherited-members:

Settings classes
________________
This page describes the classes used throughout the 240 methods that interact
with instrument settings and other methods that use objects and classes.

.. autoclass:: lakeshore.model_240.Model240CurveHeader
    :members:

    .. automethod:: __init__

.. autoclass:: lakeshore.model_240.Model240InputParameter
    :members:

    .. automethod:: __init__

.. autoclass:: lakeshore.model_240.Model240ProfiSlot
    :members:

    .. automethod:: __init__

Enumeration objects
___________________
This section describes the Enum type objects that have been created to name
various settings of the Model 240 series that are represented as an int or single character
to the instrument. The purpose of these enum types is to make the settings more
descriptive and obvious to the user rather than interpreting the ints taken by
the instrument.

.. autoclass:: Model240Units
    :members:
    :undoc-members:

.. autoclass:: Model240CurveFormat
    :members:
    :undoc-members:

.. autoclass:: Model240Coefficients
    :members:
    :undoc-members:

.. autoclass:: Model240SensorTypes
    :members:
    :undoc-members:

.. autoclass:: Model240BrightnessLevel
    :members:
    :undoc-members:

.. autoclass:: Model240TemperatureCoefficient
    :members:
    :undoc-members:

.. autoclass:: Model240InputRange
    :members:
    :undoc-members:

.. _model_335:

Model 335 Cryogenic Temperature Controller
==========================================
The Model 335 measures and controls cryogenic temperature environments.

More information about the instrument can be found `on our website`_ including the manual which has a list of all commands and queries.

.. _on our website: https://www.lakeshore.com/products/categories/overview/temperature-products/cryogenic-temperature-controllers/model-335-cryogenic-temperature-controller

Example Scripts
_______________

Setting a temperature curve
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/temperature_monitor_curve_example.py

Recording data with the Model 335
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/335_record_data_example.py

Setting up autotune on the Model 335
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/335_autotune_example.py

Instrument class methods
________________________
.. module:: lakeshore.model_335

.. autoclass:: Model335
    :member-order: bysource
    :members:
    :inherited-members: Model335Enums

Settings classes
________________

.. autoclass:: Model335InputSensorSettings
    :members:

    .. automethod:: __init__

.. autoclass:: Model335ControlLoopZoneSettings
    :members:

    .. automethod:: __init__

Enumeration objects
___________________
This section describes the Enum type objects that have been created to name
various settings of the Model 335 series that are represented as an int or single character
to the instrument. The purpose of these enum types is to make the settings more
descriptive and obvious to the user rather than interpreting the ints taken by
the instrument.

.. autoclass:: Model335Enums
    :members:
    :undoc-members:

Status register classes
_______________________
This section describes the register objects. Each bit in the register
is represented as a member of the register's class

.. autoclass:: Model335StatusByteRegister
    :members:

.. autoclass:: Model335ServiceRequestEnable
    :members:

.. autoclass:: Model335StandardEventRegister
    :members:

.. autoclass:: lakeshore.temperature_controllers.StandardEventRegister
    :members:

.. autoclass:: Model335OperationEvent
    :members:

.. autoclass:: lakeshore.temperature_controllers.OperationEvent
    :members:

.. autoclass:: Model335InputReadingStatus
    :members:

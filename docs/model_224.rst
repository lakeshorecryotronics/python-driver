.. _model_224:

Model 224 Temperature Monitor
=============================
The Lake Shore Model 224 measures up to 12 temperature sensor channels.

More information about the instrument can be found `on our website`_ including the manual which has a list of all commands and queries.

For an example script, check out :ref:`example_scripts`.

.. _on our website: https://www.lakeshore.com/products/categories/overview/temperature-products/cryogenic-temperature-monitors/model-224-temperature-monitor

Instrument methods
------------------
.. module:: lakeshore.model_224

.. autoclass:: Model224
    :member-order: bysource
    :members:
    :inherited-members:


Instrument classes
------------------

This page describes the objects used to interact with methods, settings and registers of the Model 224.

.. autoclass:: Model224AlarmParameters
    :members:

    .. automethod:: __init__

.. autoclass:: Model224InputSensorSettings
    :members:

    .. automethod:: __init__

.. autoclass:: Model224CurveHeader
    :members:

    .. automethod:: __init__

Instrument enums
----------------

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

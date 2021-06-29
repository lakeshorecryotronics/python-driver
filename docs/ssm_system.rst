.. _ssm_system:

M81 Synchronous Source Measure System
=====================================

Instrument methods are grouped into three classes: SSMsystem, SourceModule, and MeasureModule

Example Scripts
_______________
Below are a few example scripts for the M81 SSM system that use the Lake Shore Python driver.

Making a lock in measurement of resistance using a BCS-10 and VM-10
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/M81_lock_in_resistance_measurement.py

List settings profiles and restore a profile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/ssm_profiles_example.py

Classes and methods
___________________

SSMS instrument methods
~~~~~~~~~~~~~~~~~~~~~~~

.. module:: lakeshore.ssm_system

.. autoclass:: SSMSystem
    :member-order: bysource
    :members:
    :inherited-members:

Source Module methods
~~~~~~~~~~~~~~~~~~~~~

.. module:: lakeshore.ssm_source_module

.. autoclass:: SourceModule
    :member-order: bysource
    :members:
    :inherited-members:

Measure Module methods
~~~~~~~~~~~~~~~~~~~~~~

.. module:: lakeshore.ssm_measure_module

.. autoclass:: MeasureModule
    :member-order: bysource
    :members:
    :inherited-members:

Settings Profiles methods
~~~~~~~~~~~~~~~~~~~~~~~~~

.. module:: lakeshore.ssm_settings_profiles

.. autoclass:: SettingsProfiles
    :member-order: bysource
    :members:
    :inherited-members:

Instrument registers
~~~~~~~~~~~~~~~~~~~~

This page outlines the registers used to interact with various settings and
methods of the M81.

.. autoclass:: lakeshore.ssm_system.SSMSystemOperationRegister
    :members:

.. autoclass:: lakeshore.ssm_system.SSMSystemQuestionableRegister
    :members:

.. autoclass:: lakeshore.ssm_base_module.SSMSystemModuleQuestionableRegister
    :members:

.. autoclass:: lakeshore.ssm_source_module.SSMSystemSourceModuleOperationRegister
    :members:

.. autoclass:: lakeshore.ssm_measure_module.SSMSystemMeasureModuleOperationRegister
    :members:

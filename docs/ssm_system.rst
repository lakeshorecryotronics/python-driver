.. _ssm_system:

M81 Synchronous Source Measure System
=====================================

Instrument methods are grouped into three classes: SSMsystem, SourceModule, and MeasureModule

SSMS Instrument methods
-----------------------

.. module:: lakeshore.ssm_system

.. autoclass:: SSMSystem
    :member-order: bysource
    :members:
    :inherited-members:

Source Module methods
---------------------

.. module:: lakeshore.ssm_source_module

.. autoclass:: SourceModule
    :member-order: bysource
    :members:
    :inherited-members:

Measure Module methods
----------------------

.. module:: lakeshore.ssm_measure_module

.. autoclass:: MeasureModule
    :member-order: bysource
    :members:
    :inherited-members:


Instrument registers
--------------------

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

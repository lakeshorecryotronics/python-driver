.. _ssm_system:

M81 Synchronous Source Measure System
=====================================

Instrument methods
------------------

Instrument methods are grouped into three classes: SSMsystem, SourceModule, and MeasureModule

.. module:: lakeshore.ssm_system

.. autoclass:: SSMSystem
    :member-order: bysource
    :members:
    :inherited-members:

.. autoclass:: SourceModule
    :member-order: bysource
    :members:
    :inherited-members:

.. autoclass:: MeasureModule
    :member-order: bysource
    :members:
    :inherited-members:


Instrument registers
--------------------

This page outlines the registers used to interact with various settings and
methods of the M81.

.. autoclass:: SSMSystemQuestionableRegister
    :members:

.. autoclass:: SSMSystemModuleQuestionableRegister
    :members:

.. autoclass:: SSMSystemOperationRegister
    :members:

.. autoclass:: SSMSystemSourceModuleOperationRegister
    :members:

.. autoclass:: SSMSystemMeasureModuleOperationRegister
    :members:

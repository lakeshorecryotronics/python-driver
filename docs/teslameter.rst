.. _teslameter:

F41 & F71 Teslameters
=====================
The Lake Shore single-axis (F41) and multi-axis (F71) Teslameters provide highly accurate field strength measurements.

More information about the instrument can be found `on our website`_ including the manual which has a list of all SCPI commands and queries.

For an example script, check out :ref:`example_scripts`.

.. _on our website: https://www.lakeshore.com/products/Gaussmeters/F71-F41-teslameters/Pages/Overview.aspx

Instrument methods
------------------
.. module:: lakeshore.teslameter

.. autoclass:: Teslameter
    :member-order: bysource
    :members:
    :inherited-members:


Instrument classes
------------------

This page outlines the objects and classes used to interact with registers in the Teslameter driver.

.. autoclass:: TeslameterOperationRegister
    :members:

.. autoclass:: TeslameterQuestionableRegister
    :members:

.. autoclass:: StatusByteRegister
    :noindex:
    :members:

    .. automethod:: __init__

.. autoclass:: StandardEventRegister
    :noindex:
    :members:

    .. automethod:: __init__


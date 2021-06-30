.. _teslameter:

F41 & F71 Teslameters
=====================
The Lake Shore single-axis (F41) and multi-axis (F71) Teslameters provide highly accurate field strength measurements.

More information about the instrument can be found `on our website`_ including the manual which has a list of all SCPI commands and queries.

.. _on our website: https://www.lakeshore.com/products/Gaussmeters/F71-F41-teslameters/Pages/Overview.aspx

Example Scripts
_______________
Below are a few example scripts for the Teslameters that use the Lake Shore Python driver.

Streaming F41/F71 teslameter data to a CSV file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/teslameter_record_data_example.py

Instrument class methods
________________________
.. module:: lakeshore.teslameter

.. autoclass:: Teslameter
    :member-order: bysource
    :members:
    :inherited-members:


Status register classes
_______________________

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


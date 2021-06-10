.. _fast_hall:

M91 Fast Hall Controller
========================
The Lake Shore M91 Fast Hall controller makes high speed Hall measurements for materials characterization.

More information about the instrument can be found `on our website`_ including the manual which has a list of all SCPI commands and queries.

.. _on our website: https://www.lakeshore.com/products/categories/overview/material-characterization-products/measureready-instruments/measureready-m91-fasthall-measurement-controller

Example Scripts
===============
Below are a few example scripts for the M91 Fast Hall Controller that use the Lake Shore Python driver.

Fast Hall Full Sample Analysis
------------------------------
.. literalinclude:: examples/fasthall_full_sample_analysis.py

Fast Hall Record Contact Check Data
-----------------------------------
.. literalinclude:: examples/fasthall_record_contact_check_data_example.py

Classes and methods
===================

Instrument methods
------------------
.. module:: lakeshore.fast_hall_controller

.. autoclass:: FastHall
    :member-order: bysource
    :members:
    :inherited-members:


Instrument classes
------------------

This page outlines the classes and objects used to interact with various settings and
methods of the M91.

.. autoclass:: FastHallOperationRegister
    :members:

.. autoclass:: FastHallQuestionableRegister
    :members:

.. autoclass:: ContactCheckManualParameters
    :members:

    .. automethod:: __init__

.. autoclass:: ContactCheckOptimizedParameters
    :members:

    .. automethod:: __init__

.. autoclass:: FastHallManualParameters
    :members:

    .. automethod:: __init__

.. autoclass:: FastHallLinkParameters
    :members:

    .. automethod:: __init__

.. autoclass:: FourWireParameters
    :members:

    .. automethod:: __init__

.. autoclass:: DCHallParameters
    :members:

    .. automethod:: __init__

.. autoclass:: ResistivityManualParameters
    :members:

    .. automethod:: __init__

.. autoclass:: ResistivityLinkParameters
    :members:

    .. automethod:: __init__

.. autoclass:: StatusByteRegister
    :members:

    .. automethod:: __init__

.. autoclass:: StandardEventRegister
    :members:

    .. automethod:: __init__


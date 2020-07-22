.. _fast_hall:

M91 Fast Hall Controller
========================
The Lake Shore M91 Fast Hall controller makes high speed Hall measurements for materials characterization.

More information about the instrument can be found `on our website`_ including the manual which has a list of all SCPI commands and queries.

For a example scripts, check out :ref:`example_scripts`.

.. _on our website: https://www.lakeshore.com/products/categories/overview/material-characterization-products/measureready-instruments/measureready-m91-fasthall-measurement-controller

Instrument methods
------------------
.. module:: lakeshore.M91

.. autoclass:: FastHall
    :member-order: bysource
    :members:
    :inherited-members:

Instrument classes
__________________
This page outlines the classes and objects used to interact with various settings and
methods of the M91.

.. autoclass:: FastHallOperationRegister
    :members:

    .. automethod:: __init__

.. autoclass:: FastHallQuestionableRegister
    :members:

    .. automethod:: __init__

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

.. autoclass:: ResistivityLinkParameters
    :members:

    .. automethod:: __init__


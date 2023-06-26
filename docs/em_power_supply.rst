.. _em_power_supply:

Model 643 & 648 Electromagnet Power Supplies
============================================
The Lake Shore Model 643 (2.5 kW) and Model 648 (9.1 kW) Electromagnet Power Supplies provide a highly accurate linear, bipolar current source.

More information about the `Model 643`_ and `Model 648`_ can be found `on our website`_ including the manual which has a list of all commands and queries.

.. _Model 643: https://www.lakeshore.com/products/categories/overview/material-characterization-products/electromagnet-power-supplies/model-643-electromagnet-power-supply
.. _Model 648: https://www.lakeshore.com/products/categories/overview/material-characterization-products/electromagnet-power-supplies/model-648-electromagnet-power-supply
.. _on our website: https://www.lakeshore.com/products/categories/material-characterization-products/electromagnet-power-supplies

Example Scripts
_______________
Below are a few example scripts for the Electromagnet Power Supplies that use the Lake Shore Python driver.

Outputting current and measuring voltage on a Model 643
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/643_current_set_example.py

Setting up magnet water and outputting current from a Model 648
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/648_magnet_water.py

Querying the hardware error status register from a Model 648
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: examples/648_status_register.py

Instrument class methods
________________________
.. module:: lakeshore.em_power_supply

.. autoclass:: ElectromagnetPowerSupply
    :member-order: bysource
    :members:
    :inherited-members:

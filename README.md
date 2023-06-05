# Lake Shore Python Driver

[![Build Status](https://lakeshorecryotronics.visualstudio.com/Lake%20Shore%20Dev/_apis/build/status/Python%20Driver?branchName=main)](https://lakeshorecryotronics.visualstudio.com/Lake%20Shore%20Dev/_build/latest?definitionId=138?branchName=main)
[![Documentation Status](https://readthedocs.org/projects/lake-shore-python-driver/badge/?version=latest)](https://lake-shore-python-driver.readthedocs.io/en/latest/?badge=latest)
[![PyPI Version](https://img.shields.io/pypi/v/lakeshore.svg)](https://pypi.org/project/lakeshore/)

The [Lake Shore](https://www.lakeshore.com) python driver allows users to quickly and easily communicate with Lake Shore instruments. It automatically establishes a connection and provides a variety of functions specific to the product that configure settings and acquire measurements. 

## Documentation
[Click here to read the documentation and some example scripts](https://lake-shore-python-driver.readthedocs.io/en/latest/)


## Supported Products
Advanced support
* [F41 and F71 Teslameters](https://www.lakeshore.com/products/Gaussmeters/F71-F41-teslameters/Pages/Overview.aspx)
* [Model 121 Programmable DC Current Source](https://www.lakeshore.com/products/categories/overview/temperature-products/ac-and-dc-current-sources/model-121-programmable-dc-current-source)
* [155 Precision I/V Source](https://www.lakeshore.com/products/measureready/model-155/Pages/Overview.aspx) 
* [M91 FastHall Controller](https://www.lakeshore.com/products/categories/overview/material-characterization-products/measureready-instruments/measureready-m91-fasthall-measurement-controller) 
* [M81 Synchronous Source Measure System](https://www.lakeshore.com/products/categories/overview/material-characterization-products/measureready-m81-synchronous-source-measure-system/measureready-m81-synchronous-source-measure-system)
* [Model 224 Temperature Monitor](https://www.lakeshore.com/products/categories/overview/temperature-products/cryogenic-temperature-monitors/model-224-temperature-monitor)
* [Model 240 Input Modules](https://www.lakeshore.com/products/categories/overview/temperature-products/cryogenic-temperature-modules/240-series-input-modules)
* [Model 335 Cryogenic Temperature Controller](https://www.lakeshore.com/products/categories/overview/temperature-products/cryogenic-temperature-controllers/model-335-cryogenic-temperature-controller)
* [Model 336 Cryogenic Temperature Controller](https://www.lakeshore.com/products/categories/overview/temperature-products/cryogenic-temperature-controllers/model-336-cryogenic-temperature-controller)
* [Model 372 AC Resistance Bridge](https://www.lakeshore.com/products/categories/overview/temperature-products/cryogenic-temperature-controllers/model-372-ac-resistance-bridge-temperature-controller)
* [Model 643 and 648 Electromagnet Power Supplies](https://www.lakeshore.com/products/categories/material-characterization-products/electromagnet-power-supplies)

  Basic support
* [Model 350 Cryogenic Temperature Controller](https://www.lakeshore.com/products/categories/overview/temperature-products/cryogenic-temperature-controllers/model-350-cryogenic-temperature-controller)
* [Model 425 Gaussmeter](https://www.lakeshore.com/products/categories/overview/magnetic-products/gaussmeters-teslameters/model-425-gaussmeter)

## Getting Started
Install the driver using [pip](https://pip.pypa.io/en/stable/quickstart/):

    pip install lakeshore

## A Simple Example
The following code will connect to a 155 Precision Source over USB and print what is returned by an identification query.

    from lakeshore import PrecisionSource

    my_instrument = PrecisionSource()
    print(my_instrument.query('*IDN?'))

## Contribute
We want your feedback!

Please request changes, features, and additional instruments through the GitHub issues page.

Don't hesitate to create pull requests. They make the driver better for everyone! 

## Resources
* [Lake Shore website](https://www.lakeshore.com)
* [GitHub repo](https://github.com/lakeshorecryotronics/python-driver)
* [Change log](https://github.com/lakeshorecryotronics/python-driver/blob/main/CHANGELOG.md)
* [Documentation](https://lake-shore-python-driver.readthedocs.io/en/latest/)

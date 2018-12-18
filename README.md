# Introduction 
The [Lake Shore](https://www.lakeshore.com) python driver allows users to quickly and easily communicate with Lake Shore instruments. It automatically establishes a connection and provides a variety of functions specific to the product that configure settings and acquire measurements. 

# List of Supported Products
* [F41 and F71 Teslameters](https://www.lakeshore.com/products/Gaussmeters/F71-F41-teslameters/Pages/Overview.aspx)
* [155 Precision I/V Source](https://www.lakeshore.com/products/measureready/model-155/Pages/Overview.aspx) 


# Getting Started
Install the driver using [pip](https://pip.pypa.io/en/stable/quickstart/):

    pip install lakeshore

# A simple example
The following code will connect to a 155 Precision Source over USB and print what is returned by an identification query.

    from lakeshore import PrecisionSource

    my_instrument = PrecisionSource()
    print(my_instrument.query('*IDN?'))

# Documentation
Detailed documentation of the driver and more example code is available [here](TBD).

# Contribute
We want your feedback! Please request changes, features, and additional instruments through the GitHub issues page.

If you have developed a code for your application that would be helpful for other users, please create a pull request on GitHub.

# Resources
* Lake Shore website: [https://www.lakeshore.com](https://www.lakeshore.com)
* GitHub: 
* License: 
* Change log: 
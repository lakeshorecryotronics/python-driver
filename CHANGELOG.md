Change Log
==========
Release 1.3.0
-------------
Added:
- Basic support for the Model 425 Gaussmeter
- Basic support for the Model 643 Electromagnet Power Supply
- Basic support for the Model 648 Electromagnet Power Supply
- Basic support for the Model 335 Cryogenic Temperature Controller
- Basic support for the Model 336 Cryogenic Temperature Controller
- Basic support for the Model 350 Cryogenic Temperature Controller
- Basic support for the Model 372 AC Resistance Bridge
- Basic support for the Model 224 Temperature Monitor
- Basic support for the Model 240 Input Modules
- Basic support for the Model 121 Programmable DC Current Source
- Official product name aliases for instrument classes

 
Release 1.2.0
-------------
Added:
 - Support for M91 FastHall Measurement Controller

Release 1.1.0
-------------
Added:
 - Support for configurable TCP ports.
 - Teslameter corrected analog out enumerations.
 - Driver thread safety.

Changed:
- Changed key names in dicts returned by some configuration queries for the Teslameter.
- Default TCP port is now 7777 instead of 8888.

Fixed:
- `output_enabled` in `get_field_control_output_mode` response was previously always true.

Release 1.0.0
-------------
Initial release of the Lake Shore python driver.

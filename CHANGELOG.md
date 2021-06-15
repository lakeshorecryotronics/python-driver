Change Log
==========
Release 1.5.0
-------------
Changed:
- The computer will remain awake while streaming data from the M81

Fixed:
- Incorrect header levels in the docs

Removed:
- Support for python 2

Release 1.4.0
-------------
Added:
- Full support for the Model 224 temperature monitor
- Full support for the Model 240 temperature monitor
- Full support for the Model 335 temperature controller
- Full support for the Model 336 temperature controller
- Full support for the Model 372 temperature controller
- Full support for the M81 synchronous source measure system

Changed:
- Renamed M91.py to fast_hall_controller.py to maintain convention and avoid using the same name as the class
- SCPI error queue cleared by default upon initial connection
- Improved documentation

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

Change Log
==========

Release 1.6.0
-------------
Added:
- M81 data sources enumeration and example
- Support for lock-in IIR filter on M81
- Read subsystem support for M81
- Settings profiles for M81 include summary and notes queries
- Support for M81 monitor out scale query
- M81 calibration information queries
- M81 load all modules and unload module methods
- All instruments support enter and exit methods for context management
- Data streaming on M81 supports source readback settling
- Parameter sweeping on M81
- Frequency range threshold support for M81 measure module
- Configurable FIR cycles in M81 measure modules
- Output limits for M81 source modules
- Bias voltage controls for M81 measure modules
- Disable on compliance for M81 source modules
- M81 module reset commands
- Line frequency detection queries for M81
- Minimum and maximum values support for M81 measure modules
- Digital high pass filter for M81 measure modules
- Resistance measurement methods for M81
- Relative measurement methods for M81 measure modules

Changed:
- Clarified confusing M81 documentation
- Model 335 gets now return list literals where appropriate

Fixed:
- M81 FIR cycles now set as expected
- M81 data source mnemonics corrected
- Correctly handles multi-line responses from MeasureReady instruments
- Replaced methods that referred to current and voltage by i and v with the full word

Release 1.5.3
-------------
Added:
- Settings profiles for the M81 SSM System

Fixed:
- Issue with public docs build causing classes and methods to not appear
- All aliased classes are now properly documented

Release 1.5.2
-------------
Fixed:
- Bugs in the status register base methods

Release 1.5.1
-------------
Fixed:
- Readme now updated with which products are fully supported

Release 1.5.0
-------------
Added:
- Dark mode get and set methods for the M81

Changed:
- The computer will remain awake while streaming data from the M81

Fixed:
- Incorrect header levels in the docs
- A few bugs in the M81 driver

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

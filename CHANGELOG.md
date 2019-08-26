Change Log
==========
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

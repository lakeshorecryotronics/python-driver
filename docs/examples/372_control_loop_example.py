from lakeshore import Model372, Model372HeaterOutputSettings, Model372ControlLoopZoneSettings

# Include baud rate when initializing instrument
my_model_372 = Model372(57600)

# Configure output for zone mode, controlled by control input, with power up enabled filter enabled and a reading
# delay of 10 seconds
# Note; it's assumed that the control input is enabled and configured
heater_settings = Model372HeaterOutputSettings(my_model_372.OutputMode.ZONE, my_model_372.InputChannel.CONTROL, True, True, 10)
my_model_372.configure_heater(1, heater_settings)

# Configure a relay for Warmup Heater Zone
my_model_372.set_relay_for_warmup_heater_control_zone(1)

# Set up control loop with an upper bound of 15K, a gain of 50, an integral value of 5000, a derivative of 2000, and a
# manual output of 50%. Range is set to true, setpoint ramp rate is set to 10 seconds, and relay 1 is configured for
# the zone and relay 2 is not configured
control_loop_settings = Model372ControlLoopZoneSettings(15, 50.0, 5000, 2000, 50, True, 10, True, False)
# Set control loop on output 1 (Warmup Heater) in zone 4
my_model_372.set_control_loop_parameters(1, 4, control_loop_settings)

# Create a setpoint for 5 K
my_model_372.set_setpoint_kelvin(1, 5.0)
# Enable ramping to setpoint for output 1 at a rate of 10 Kelvin/minute
my_model_372.set_setpoint_ramp_parameter(1, True, 10)

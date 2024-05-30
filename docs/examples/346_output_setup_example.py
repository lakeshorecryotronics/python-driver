from lakeshore import Model346

# Connect to the first available Model 346 temperature controller over USB
my_model_346 = Model346()

# Set the control loop values for outputs 1 and 5
my_model_346.set_heater_pid(1, 40, 27, 0)
my_model_346.set_heater_pid(5, 42, 25, 10)

# Configure heater output 1 with a 50 ohm load, 0.75 amp max current, and screen display mode to power
my_model_346.set_heater_setup(1, 50.0, 0.75, my_model_346.HeaterOutputUnits.POWER)

# Configure settings of analog output 5 to have a high and low value of 3.65 and 1.02 (preferred units) respectively
my_model_346.set_analog_output_settings(5, 3.65, 1.02)

# Set closed loop output mode for outputs 1 and 5
my_model_346.set_output_mode(1, my_model_346.OutputMode.PID, "A")
my_model_346.set_output_mode(5, my_model_346.OutputMode.PID, "A")

# Set a control setpoint for outputs 1 and 5 to 1.5 and 2.5 (preferred units) respectively
my_model_346.set_control_setpoint(1, 1.5)
my_model_346.set_control_setpoint(5, 2.5)

# Turn the heater on by setting the heater range
my_model_346.set_heater_range(1, my_model_346.HeaterRange.LOW)
# Output 5 "turned on" when its output mode was set.

# Obtain the output percentage of output 1 and print it to the console
output_one = my_model_346.get_heater_output(1)
print("Output 1: " + str(output_one))

# Obtain the output percentage of output 3 and print it to the console
output_five = my_model_346.get_analog_output_percentage(5)
print("Output 5: " + str(output_five))

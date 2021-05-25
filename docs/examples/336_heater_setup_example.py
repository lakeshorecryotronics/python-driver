from lakeshore import Model336, Model336HeaterResistance, Model336HeaterOutputUnits, Model336InputChannel, \
                      Model336InputSensorUnits, Model336Polarity, Model336HeaterRange, Model336HeaterVoltageRange, \
                      Model336HeaterOutputMode

# Connect to the first available Model 336 temperature controller over USB with a baud rate of 57600
my_model_336 = Model336()

# Set the control loop values for outputs 1 and 3
my_model_336.set_heater_pid(1, 40, 27, 0)
my_model_336.set_heater_pid(3, 35, 20, 0)

# Configure heater output 1 with a 50 ohm load, 0.75 amp max current, and screen display mode to power
my_model_336.set_heater_setup(1, Model336HeaterResistance.HEATER_50_OHM, 0.75, Model336HeaterOutputUnits.POWER)

# Configure analog heater output 3 to monitor sensor channel A, a high and low value of 3.65 and 1.02 kelvin
# respectively as a unipolar output
my_model_336.set_monitor_output_heater(3, Model336InputChannel.CHANNEL_A, Model336InputSensorUnits.KELVIN, 3.65, 1.02,
                                        Model336Polarity.UNIPOLAR)

# Set closed loop output mode for heater 1
my_model_336.set_heater_output_mode(1, Model336HeaterOutputMode.CLOSED_LOOP, Model336InputChannel.CHANNEL_A)

# Set closed loop output mode for heater 3
my_model_336.set_heater_output_mode(3, Model336HeaterOutputMode.CLOSED_LOOP, Model336InputChannel.CHANNEL_B)

# Set a control setpoint for outputs 1 and 3 to 1.5 kelvin
my_model_336.set_control_setpoint(1, 1.5)
my_model_336.set_control_setpoint(3, 2.5)

# Turn the heaters on by setting the heater range
my_model_336.set_heater_range(1, Model336HeaterRange.MEDIUM)
my_model_336.set_heater_range(3, Model336HeaterVoltageRange.VOLTAGE_ON)

# Obtain the output percentage of output 1 and print it to the console
heater_one_output = my_model_336.get_heater_output(1)
print("Output 1: " + str(heater_one_output))

# Obtain the output percentage of output 3 and print it to the console
heater_three_output = my_model_336.get_analog_output_percentage(3)
print("Output 3: " + str(heater_three_output))

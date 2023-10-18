from lakeshore import Model372, Model372InputSetupSettings

# Include baud rate when initializing instrument
my_model_372 = Model372(57600)

# Configure a sensor
# Create Model372InputSetupSettings object with current excitation mode, 31.6 uA excitation current, autoranging on
# (tracking current), current source not shunted, preferred units of Kelvin, and a resistance range of 20.0 kOhms
sensor_settings = Model372InputSetupSettings(my_model_372.SensorExcitationMode.CURRENT,
                                             my_model_372.MeasurementInputCurrentRange.RANGE_31_POINT_6_MICRO_AMPS,
                                             my_model_372.AutoRangeMode.CURRENT, False,
                                             my_model_372.InputSensorUnits.KELVIN,
                                             my_model_372.MeasurementInputResistance.RANGE_20_KIL_OHMS)

# Pass settings into method along with desired input channel
my_model_372.configure_input(1, sensor_settings)

# Get all readings (temperature, resistance, excitation power, quadrature) from sensor
sensor_1_readings = my_model_372.get_all_input_readings(1)

# Record readings to a file
file = open("372_sensor_1_data.csv", "w")
file.write("Header information\n")
# Call readings using the keys of the returned dictionary
file.write("Temperature Reading," + str(sensor_1_readings['kelvin']) + "\n")
file.write("Resistance Reading," + str(sensor_1_readings['resistance']) + "\n")
file.write("Excitation Power," + str(sensor_1_readings['power']) + "\n")
file.write("Imaginary Part of Resistance," + str(sensor_1_readings['quadrature']) + "\n")
file.close()

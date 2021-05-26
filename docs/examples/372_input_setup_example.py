from lakeshore import Model372
from lakeshore import Model372SensorExcitationMode, Model372MeasurementInputCurrentRange, \
    Model372AutoRangeMode, Model372InputSensorUnits, Model372MeasurementInputResistance, Model372InputSetupSettings

# Include baud rate when initializing instrument
my_model_372 = Model372(57600)

# Configure a sensor
# Create Model372InputSetupSettings object with current excitation mode, 31.6 uA excitation current, autoranging on
# (tracking current), current source not shunted, preferred units of Kelvin, and a resistance range of 20.0 kOhms
sensor_settings = Model372InputSetupSettings(Model372SensorExcitationMode.CURRENT,
                                             Model372MeasurementInputCurrentRange.RANGE_31_POINT_6_MICRO_AMPS,
                                             Model372AutoRangeMode.CURRENT, False, Model372InputSensorUnits.KELVIN,
                                             Model372MeasurementInputResistance.RANGE_20_KIL_OHMS)

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

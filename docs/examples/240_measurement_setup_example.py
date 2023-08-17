from lakeshore import Model240, Model240InputParameter
from time import sleep

# Connect to the first available Model 240 over USB
my_model_240 = Model240()

# Define the channel configuration for a sensor with a negative temperature coefficient, autorange disabled
# current reversal disabled, the channel enabled, and set to the 100 kOhm range
rtd_config = Model240InputParameter(my_model_240.SensorTypes.NTC_RTD, False, False, my_model_240.Units.SENSOR, True,
                                    my_model_240.InputRange.RANGE_NTCRTD_100_KIL_OHMS)

# Apply the configuration to all channels
for channel in range(1, 9):
    my_model_240.set_input_parameter(channel, rtd_config)

sleep(1)
print("Reading from channel 5: {} ohms".format(my_model_240.get_sensor_reading(5)))

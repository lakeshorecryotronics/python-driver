from lakeshore import Model335
from lakeshore.model_335 import Model335DisplaySetup, Model335HeaterResistance, \
    Model335HeaterOutputDisplay, Model335HeaterRange, Model335AutoTuneMode, Model335HeaterError
from time import sleep

# Connect to the first available Model 335 temperature controller over USB using a baud rate of 57600
my_model_335 = Model335(57600)

# It is assumed that the instrument is configured properly with a control input sensor curve
# and heater output, capable of closed loop control

# Configure the display mode
my_model_335.set_display_setup(Model335DisplaySetup.TWO_INPUT_A)

# Configure heater output 1 using the HeaterSetup class and set_heater_setup method
my_model_335.set_heater_setup_one(Model335HeaterResistance.HEATER_50_OHM, 1.0, Model335HeaterOutputDisplay.POWER)

# Configure heater output 1 to a setpoint of 310 kelvin (units correspond to the configured output units)
set_point = 325
my_model_335.set_control_setpoint(1, set_point)

# Turn on the heater by setting the range
my_model_335.set_heater_range(1, Model335HeaterRange.HIGH)

# Check to see if there are any heater related errors
heater_error = my_model_335.get_heater_status(1)
if heater_error is not Model335HeaterError.NO_ERROR:
    raise Exception(heater_error.name)

# Allow the heater some time to turn on and start maintaining a setpoint
sleep(10)

# Ensure that the temperature is within 5 degrees kelvin of the setpoint
kelvin_reading = my_model_335.get_kelvin_reading(1)
if (kelvin_reading < (set_point - 5)) or (kelvin_reading > (set_point + 5)):
    raise Exception("Temperature reading is not within 5k of the setpoint")

# Initiate autotune in PI mode, initial conditions will not be met if the system is not
# maintaining a temperature within 5 K of the setpoint
my_model_335.set_autotune(1, Model335AutoTuneMode.P_I)

# Poll the instrument until the autotune process completes
autotune_status = my_model_335.get_tuning_control_status()
while autotune_status["active_tuning_enable"] and not autotune_status["tuning_error"]:
    autotune_status = my_model_335.get_tuning_control_status()
    # Print the status to the console every 5 seconds
    print("Active tuning: " + str(autotune_status["active_tuning_enable"]))
    print("Stage status: " + str(autotune_status["stage_status"]) + "/10")
    sleep(5)

if autotune_status["tuning_error"]:
    raise Exception("An error occurred while running autotune")

from lakeshore import Model643
from time import sleep

# Connect to 643 over USB
my_power_supply = Model643()

# Setup current and ramp rate limits
my_power_supply.set_limits(20.000, 3.000)

# Start outputting current from the power supply
my_power_supply.set_current(10.000)

# Wait for power supply to ramp up to specified output current
sleep(10)

# Record real-time output voltage at power supply terminals
measured_voltage = my_power_supply.get_measured_voltage()

print(f"Measured Voltage: {measured_voltage}")

# Set current output back to 0 Amps
my_power_supply.set_current(0)

from lakeshore import Model648

# Connect to 648 over USB
my_power_supply = Model648()

# Setup current and ramp rate limits
my_power_supply.set_limits(120.000, 40.000)

# Set magnet water to Auto
my_power_supply.set_magnet_water(2)

# Setup ramp rate for current output
my_power_supply.set_ramp_rate(25.000)

# Start outputting current from the power supply
my_power_supply.set_current(95.000)

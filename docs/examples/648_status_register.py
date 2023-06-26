from lakeshore import Model648

# Connect to 648 over USB 
my_power_supply = Model648()

# Query for hardware errors register mask
register_mask = my_power_supply.get_hardware_error_enable_mask()

# Mask all hardware errors (Masked bits do not affect the parent register)
register_mask.from_integer(0)

# Unmask desired error bits
register_mask.output_over_current = True
register_mask.output_over_voltage = True
register_mask.temperature_fault = True

# Set hardware errors mask
my_power_supply.set_hardware_error_enable_mask(register_mask)

# Query for hardware errors (Ignores the bits masked above)
hardware_error = my_power_supply.get_status_byte().hardware_errors_summary
if hardware_error:
    print(my_power_supply.get_hardware_error_condition())
else:
    print("No hardware errors!")




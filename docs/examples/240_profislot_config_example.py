from lakeshore import Model240, Model240Units, Model240ProfiSlot

# Connect to the first available Model 240 over USB
my_model_240 = Model240()

# Print the instrument's current PROFIBUS connection status to the console
print("Profibus connection status: " + my_model_240.get_profibus_connection_status())

# Configure the number of PROFIBUS slots for the instrument to present to the bus as a modular station
# Setting the number of PROFIBUS slots to 2
my_model_240.set_profibus_slot_count(2)

# Create the ProfiSlot class object by specifying which input to associate the
# slot with and what temperature units the data will be presented in
# Setting the input channel as 2 and temperature units to Celsius
my_profibus_slot = Model240ProfiSlot(2, Model240Units.CELSIUS)

# Configure what data to be presented on the given PROFIBUS slot
# Profibus slot 1 will be associated with channel 2
my_model_240.set_profibus_slot_configuration(1, my_profibus_slot)

# Print the PROFIBUS address
# An address of 126 indicates that it is not configured and it can then be set by a PROFIBUS master
print("Profibus adress: " + my_model_240.get_profibus_address())

# Set the desired address as 123
my_model_240.set_profibus_address("123")

# Acquiring settings that were configured above
print(my_model_240.get_profibus_slot_count())
slot_1_config = my_model_240.get_profibus_slot_configuration(1)
print(slot_1_config.slot_channel)
print(slot_1_config.slot_units)

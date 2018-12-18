from lakeshore import Teslameter

# Connect to the first available Teslameter over USB
my_teslameter = Teslameter()

# Configure the instrument to be in DC field mode and give it a moment to settle
my_teslameter.command('SENSE:MODE DC')

# Query the probe serial number
probe_serial_number = my_teslameter.query('PROBE:SNUMBER?')

# Query the probe temperature
probe_temperature = my_teslameter.query('FETCH:TEMPERATURE?')

# Create a file to write data into.
file = open("teslameter_data.csv", "w")

# Write header info including the instrument serial number, probe serial number, and temperature.
file.write('Header Information\n')
file.write('Instrument serial number:,' + my_teslameter.serial_number + '\n')
file.write('Probe serial number:,' + probe_serial_number + '\n')
file.write('Probe temperature:,' + probe_temperature + '\n\n')

# Collect 10 seconds of 10 ms data points and write them to the csv file
my_teslameter.log_buffered_data_to_file(10, 10, file)

# Close the file so that it can be used by the function
file.close()

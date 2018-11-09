from lakeshore.precision_source import PrecisionSource

# The purpose of this script is to sweep frequency, amplitude, and offset of an output signal using
# a Lake Shore AC/DC 155 Precision Source

# Create a new instance of the Lake Shore 155 Precision Source.
# It will connect to the first instrument it finds via serial USB
my_source = PrecisionSource()

# Define a custom list of frequencies to sweep through
frequency_sweep_list = ['1', '10', '100', '250', '500', '750', '1000', '2000', '5000', '10000']

# Sweep frequency in voltage mode. Wait 1 second at each step
my_source.sweep_voltage(1, frequency_values=frequency_sweep_list)


# Creates a list of whole number offset values between -5V and 5V.
offset_sweep_list = range(-5, 6)
# Creates a list of amplitudes between 0 and 5V incrementing by 100mV
amplitude_sweep_list = [value/10 for value in range(0, 51)]
# Creates a list of frequencies starting with 0.1 Hz and increasing by powers of ten up to 10 kHz
frequency_sweep_list = [10**exponent for exponent in range(-1, 5)]

# Use the function defined above to sweep across all combinations of the lists.
# For each combination, wait 10ms before moving to the next one.
my_source.sweep_voltage(0.01,
                        offset_values=offset_sweep_list,
                        amplitude_values=amplitude_sweep_list,
                        frequency_values=frequency_sweep_list)

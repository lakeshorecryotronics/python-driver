from lakeshore import SSMSystem
from time import sleep
from math import sqrt

# Connect to instrument via USB
my_M81 = SSMSystem()

# Instantiate source and measure modules
balanced_current_source = my_M81.get_source_module(1)
voltage_measure = my_M81.get_measure_module(1)

# Set the source frequency to 13.7 Hz
balanced_current_source.set_frequency(13.7)

# Set the source current peak amplitude to 1 mA
balanced_current_source.set_current_amplitude(0.001)

# Set the voltage measure module to reference the source 1 module with a 100 ms time constant
voltage_measure.setup_lock_in_measurement('S1', 0.1)

# Enable the source output
balanced_current_source.enable()

# Wait for 15 time constants before taking a measurement
sleep(1.5)
lock_in_magnitude = voltage_measure.get_lock_in_r()

# Get the amplitude of the current source
peak_current = balanced_current_source.get_current_amplitude()

# Calculate the resistance
resistance = lock_in_magnitude * sqrt(2) / peak_current
print("Resistance: {} ohm".format(resistance))

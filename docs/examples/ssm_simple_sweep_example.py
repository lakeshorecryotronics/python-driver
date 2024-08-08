from lakeshore import SSMSystem
from time import sleep

# Connect to instrument via USB and reset settings
my_ssm = SSMSystem()
my_ssm.reset_measurement_settings()

# Set up a VS-10 in channel S1
s1_vs_10 = my_ssm.get_source_module(1)
s1_vs_10.enable()

# Configure the VS-10 to smoothly ramp to 2 volts at 0.25 volts per second
s1_vs_10.set_voltage_ramp_configuration(2, slew_rate=0.25)
# Initiate the ramp
my_ssm.initiate_sweeps()

print('Ramping to start')
# Poll the instrument waiting for the ramp to finish
while s1_vs_10.get_source_sweep_state():
    sleep(0.1)

print('Running data sweep')
# Automatically do a sweep on S1 with data collected from M1
swept_data = s1_vs_10.do_dc_sweep_step_and_measure(2, 5)

print(swept_data)

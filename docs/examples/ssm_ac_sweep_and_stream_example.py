from lakeshore import SSMSystem
import time , random

sweep_data = {}

start_value = 0.001
stop_value = 3
number_of_points = 20
source_dwell_time = 0.2
round_trip = True
sweep_spacing = 'LINEAR'  # 'LINEAR' or 'LOGARITHMIC'
ac_sweep_shape = 'SINUSOID'  # 'SINUSOID', 'SQUARE', 'TRIANGLE'

my_ssm = SSMSystem()
sweep_data = {}

source1 = my_ssm.get_source_module(1)
source1.enable()
measure1 = my_ssm.get_measure_pod(1)
measure1.setup_lock_in_measurement('S1','0.0002')

stream_elements = [(my_ssm.DataSourceMnemonic.SOURCE_AMPLITUDE,1),
                   (my_ssm.DataSourceMnemonic.MEASURE_R, 1),
                   (my_ssm.DataSourceMnemonic.MEASURE_THETA, 1),
                   (my_ssm.DataSourceMnemonic.MEASURE_X, 1)]

sweep_data = source1.sweep_ac_amplitude(start_amplitude=start_value,
                                          stop_amplitude=stop_value, 
                                          ac_shape=ac_sweep_shape,
                                          source_frequency=2500,
                                          optional_custom_data_sources=stream_elements,
                                          dwell_time=source_dwell_time,
                                          number_of_points=number_of_points,
                                          round_trip=round_trip,
                                          include_relative_time=True,
                                          sweep_spacing=sweep_spacing)

time.sleep(1)

print(sweep_data)

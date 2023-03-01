from lakeshore import SSMSystem

# Connect to instrument via USB
my_ssm = SSMSystem()

# Set up a BCS-10 in channel S1 in SC shape with a manual range of 100 mA
s1_bcs = my_ssm.get_source_module(1)

s1_bcs.set_shape('DC')
s1_bcs.configure_current_range(False, max_level=.1)

# Configure the sweep settings to sweep 0 mA to 100 mA with a dwell time of 1 ms
sweep_configuration = SSMSystem.SourceSweepSettings(sweep_type=my_ssm.SourceSweepType.CURRENT_AMPLITUDE,
                                                    start=0.0,
                                                    stop=0.1,
                                                    points=1000,
                                                    dwell=.001)
s1_bcs.set_sweep_configuration(sweep_configuration)

# stream 1,000 samples of synchronized data at 1,000 samples per second and simultaneously start the sweep
s1_bcs.enable()
stream_data = my_ssm.get_data(1000, 1000,
                              [my_ssm.DataSourceMnemonic.SOURCE_AMPLITUDE, 1],
                              [my_ssm.DataSourceMnemonic.MEASURE_DC, 1])

print(stream_data)

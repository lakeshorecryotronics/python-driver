from lakeshore import SSMSystem, SSMSystemDataSourceMnemonic

# Connect to instrument via USB
my_M81 = SSMSystem()

# stream 5,000 samples of synchronized data at 1,000 samples per second
streamed_data = my_M81.get_data(1000, 5000,
                                (SSMSystemDataSourceMnemonic.RELATIVE_TIME, 1),
                                (SSMSystemDataSourceMnemonic.SOURCE_OFFSET, 1),
                                (SSMSystemDataSourceMnemonic.MEASURE_X, 1),
                                (SSMSystemDataSourceMnemonic.MEASURE_Y, 1),
                                (SSMSystemDataSourceMnemonic.MEASURE_DC, 2))

# format the data and print to the console
for point in streamed_data:
    print(f'Time in seconds: {point[0]}')
    print(f'Source 1 offset: {point[1]}')
    print(f'Measure 1 in-phase indication: {point[2]}')
    print(f'Measure 1 out-of-phase indication: {point[3]}')
    print(f'Measure 2 DC indication: {point[4]}\n')

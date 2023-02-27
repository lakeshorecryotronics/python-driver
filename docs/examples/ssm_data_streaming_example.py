from lakeshore import SSMSystem
from lakeshore import SSMSystemEnums

# Connect to instrument via USB
my_M81 = SSMSystem()

# stream 5,000 samples of synchronized data at 1,000 samples per second
streamed_data = my_M81.get_data(1000, 5000,
                                (SSMSystemEnums.DataSourceMnemonic.RELATIVE_TIME, 1),
                                (SSMSystemEnums.DataSourceMnemonic.SOURCE_OFFSET, 1),
                                (SSMSystemEnums.DataSourceMnemonic.MEASURE_X, 1),
                                (SSMSystemEnums.DataSourceMnemonic.MEASURE_Y, 1),
                                (SSMSystemEnums.DataSourceMnemonic.MEASURE_DC, 2))

# format the data and print to the console
for point in streamed_data:
    print(f'Time in seconds: {point[0]}')
    print(f'Source 1 offset: {point[1]}')
    print(f'Measure 1 in-phase indication: {point[2]}')
    print(f'Measure 1 out-of-phase indication: {point[3]}')
    print(f'Measure 2 DC indication: {point[4]}\n')

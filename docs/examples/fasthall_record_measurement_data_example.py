from lakeshore import FastHall, ContactCheckManualParameters

# Connect to the first available FastHall over USB
my_fast_hall = FastHall()

# Create a contact check parameters object with desired settings to run a manual Contact Check measurement
ccheck_settings = ContactCheckManualParameters(excitation_type='CURRENT',
                                               excitation_start_value=-10e-6,
                                               excitation_end_value=10e-6,
                                               compliance_limit=1.5,
                                               number_of_points=20)
# Create a file to write data into
file = open("fasthall_data.csv", "w")

# Write header info including the type of test and specific measurements being taken
file.write('Contact Check of Van der Pauw Sample with Varying Current Excitation Ranges\n')
file.write('Contact Pair 1-2\n')
file.write(' , Offset, Slope, R Squared, R Squared Passed, In Compliance, Voltage Overload, Current Overload\n')

# Create a list of current excitation ranges
excitation_ranges = [10e-3, 10e-4, 10e-5, 10e-6]

# Run a separate Contact Check measurement and collect results for each range in the list of excitation ranges
for range_value in excitation_ranges:

    # Set the value of the excitation range
    ccheck_settings.excitation_range = range_value

    # Write the specific excitation range that is being used
    file.write('Excitation Range: ' + str(range_value) + 'A\n')

    # Run a complete contact check measurement using the settings with the updated excitation range
    results = my_fast_hall.run_complete_contact_check_manual(ccheck_settings, sample_type="VDP")

    # Collect the measurement results that correlate to the first contact pair (Contact Pair 1-2)
    contact_pair_results = results.get('ContactPairIVResults')
    pair_one_results = contact_pair_results[0]

    # Obtain contact pair result values, then convert them into a list and then a string
    logged_keys = ['Offset', 'Slope', 'RSquared', 'RSquaredPass', 'InCompliance', 'VoltageOverload', 'CurrentOverload']
    logged_values = [pair_one_results[key] for key in logged_keys]
    logged_string = ','.join(str(value) for value in logged_values)

    # Write the result values to the file
    file.write(',' + logged_string + '\n')

# Close the file so that it can be used by the function
file.close()

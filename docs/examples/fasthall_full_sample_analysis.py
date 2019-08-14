from lakeshore import FastHall
from lakeshore import ContactCheckOptimizedParameters, ResistivityLinkParameters, FastHallLinkParameters

# Connect to the first available FastHall over USB
my_fast_hall = FastHall()

# Create an optimized contact check settings object that limits the max current to 1 mA
ccheck_settings = ContactCheckOptimizedParameters(max_current=1e-3)

# Define the DC magnetic field strength of the measurement
magnetic_field_strength = 0.1

# Create a resistivity and FastHall measurement linked settings objects
resistivity_settings = ResistivityLinkParameters()
fasthall_settings = FastHallLinkParameters(magnetic_field_strength)

# Run the optimized contact check to automatically determine the best parameters for the sample
ccheck_results = my_fast_hall.run_complete_contact_check_optimized(ccheck_settings)

# Run a resistivity measurement linking the parameters determined by the contact check
resistivity_results = my_fast_hall.run_complete_resistivity_link(resistivity_settings)

# Prompt the user to insert the sample into the defined field
input("Insert sample into " + str(magnetic_field_strength) + " Tesla field")

# Run the FastHall measurement linking information from the resistivity and contact check measurements
fasthall_results = my_fast_hall.run_complete_fasthall_link(fasthall_settings)

# Dump the data into a text file
results_file = open("sample_analysis.txt", "w")
results_file.write("Contact check results:\n" + str(ccheck_results))
results_file.write("\nResistivity results:\n" + str(resistivity_results))
results_file.write("\nFastHall results:\n" + str(fasthall_results))

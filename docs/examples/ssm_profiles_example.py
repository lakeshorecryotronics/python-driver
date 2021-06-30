from lakeshore import SSMSystem

# Connect to instrument via USB
my_M81 = SSMSystem()

# Print a list of saved settings profiles
print(my_M81.settings_profiles.get_list())

# Check that a specific profile can be applied with the present modules
profile_name = "Transistor IV sweep"
if my_M81.settings_profiles.get_valid_for_restore(profile_name):
    my_M81.settings_profiles.restore(profile_name)
else:
    print("The connected modules don't match the profile. Please check the profile and try again.")

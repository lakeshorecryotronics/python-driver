from lakeshore import Model121

# Connect to Model 121 over USB
current_source = Model121()

# Set current source to 150 nA and start
current_source.set_current(150e-9)

# Query and print the current source level
print(current_source.get_current())

import matplotlib.pyplot as plt
from lakeshore import Model224
from lakeshore.model_224 import Model224CurveHeader, Model224CurveFormat, Model224CurveTemperatureCoefficients, \
    Model224SoftCalSensorTypes

# Connect to a temperature instrument (the Model 224 in this case) over USB
myinstrument = Model224()

# Configure a curve by first setting its header parameters. First, set the name and serial number of the curve.
# Then, select the units used to set map the sensor units to temperature units. Set a temperature limit, and
# then specify whether the coefficients are positive or negative.
curve_header_25 = Model224CurveHeader("My_Curve", "ABC123", Model224CurveFormat.VOLTS_PER_KELVIN, 300.0,
                                      Model224CurveTemperatureCoefficients.POSITIVE)
myinstrument.set_curve_header(25, curve_header_25)

# Edit individual data points of the curve. In this case, a sensor value of 1.23 is set to equal a Kelvin value of
# 276.0
myinstrument.set_curve_data_point(25, 1, 1.23, 276.0)

# You can create a softcal curve by inputting 1-3 calibration sensor/temperature points. The instrument generates
# a new curve using your entered data points and the selected standard curve
myinstrument.generate_and_apply_soft_cal_curve(Model224SoftCalSensorTypes.DT_400, 30, "SN123", (276, 10),
                                               (300, 5), (310, 2))

# Use the get_curve method to get all the data points for a curve as a list. This can then be used to create a plot
# of the calibration curve.
data_points_list = myinstrument.get_curve(30)
x_list = [item[0] for item in data_points_list]
y_list = [item[1] for item in data_points_list]
plt.plot(x_list, y_list)

# Finally, a curve can be deleted if you would like to reset the data points for that curve. Only user curves
# can be deleted.
myinstrument.delete_curve(25)


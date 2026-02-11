from lakeshore import Model346, Model346InputSensorSettings

# Initialize the Model346 temperature controller
my_model_346 = Model346()

# Retrieve connected option cards as a dictionary of slot identifiers and OptionCard objects
option_cards = my_model_346.get_installed_option_cards()

# Print the details of each option card
for slot, card in option_cards.items():
    print(f"Slot {slot}: {card}")

# Define NTC RTD sensor settings
ntc_rtd_settings = Model346InputSensorSettings(
    sensor_type=my_model_346.InputSensorType.NTC_RTD,
    autorange_enable=True,
    compensation=True,
    units=my_model_346.InputSensorUnits.KELVIN,
    input_range=my_model_346.NTCRTDRange.ONE_THOUSAND_OHM
)

# Define Thermocouple settings for type E
thermocouple_settings = Model346InputSensorSettings(
    sensor_type=my_model_346.InputSensorType.THERMOCOUPLE,
    autorange_enable=False, # Thermocouples have a fixed range of 50mV
    compensation=True,
    units=my_model_346.InputSensorUnits.KELVIN,
    input_range=my_model_346.ThermocoupleRange.FIFTY_MILLIVOLTS
)

# Loop through option card slots and configure channels for SCANNER and THERMOCOUPLE cards
for slot, option_card in option_cards.items():

    # Configure all scanner input sensor channels as NTC RTDs
    if option_card.card_type == my_model_346.OptionCardType.SCANNER:
        for channel in option_card.channels:  # Loop through channels of the SCANNER card
            my_model_346.set_input_sensor(input_channel=channel, sensor_params=ntc_rtd_settings)

        # Get the scanner input sensor settings and print them in a readable format
        for channel in option_card.channels:
            sensor_settings = my_model_346.get_input_sensor(input_channel=channel)
            print(
                f"Channel {channel} on slot {slot} has sensor settings: "
                f"SensorType={sensor_settings.sensor_type.name}, "
                f"AutoRange={sensor_settings.autorange_enable}, "
                f"Compensation={sensor_settings.compensation}, "
                f"Units={sensor_settings.units.name}, "
                f"InputRange={sensor_settings.input_range.name}"
            )

        # Read and print the current temperature reading from each scanner channel for channel in option_card.channels:
            temperature_reading = my_model_346.get_kelvin_reading(input_channel=channel)
            print(f"Current temperature reading from channel {channel} on slot {slot}: {temperature_reading} K")

    # Thermocouple setup for channels on a Thermocouple card
    if option_card.card_type == my_model_346.OptionCardType.THERMOCOUPLE:
        for channel in option_card.channels:

            # Set the sensor parameters for the thermocouple
            my_model_346.set_input_sensor(input_channel=channel, sensor_params=thermocouple_settings)

            my_model_346.set_input_curve(input_channel=channel, curve_number=my_model_346.StandardCurveType.THERMOCOUPLE_TYPE_E)

            # Get the curve settings and print them
            curve_settings = my_model_346.get_input_curve(input_channel=channel)
            print(f"Channel {channel} on slot {slot} has curve settings: {curve_settings}")

            # Get the thermocouple sensor settings and print them
            sensor_settings = my_model_346.get_input_sensor(input_channel=channel)
            print(
                f"Channel {channel} on slot {slot} has sensor settings: "
                f"SensorType={sensor_settings.sensor_type.name}, "
                f"AutoRange={sensor_settings.autorange_enable}, "
                f"Compensation={sensor_settings.compensation}, "
                f"Units={sensor_settings.units.name}, "
                f"InputRange={sensor_settings.input_range.name}"
            )

            # Read and print the current temperature reading from the thermocouple channel
            temperature_reading = my_model_346.get_kelvin_reading(input_channel=channel)
            print(f"Current temperature reading from channel {channel} on slot {slot}: {temperature_reading} K")


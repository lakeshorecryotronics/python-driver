"""Implements functionality unique to the Model 643 and 648 electromagnet power supplies."""

import serial
from .generic_instrument import GenericInstrument, RegisterBase, _parse_response, InstrumentException


class ElectromagnetPowerSupply(GenericInstrument):
    """Class object representing a Lake Shore Model 643 or 648 electromagnet power supply."""
    vid_pid = [(0x1FB9, 0x0601), (0x1FB9, 0x0602)]  # 643, 648

    def __init__(self,
                 serial_number=None,
                 com_port=None,
                 baud_rate=57600,
                 data_bits=7,
                 stop_bits=1,
                 parity=serial.PARITY_ODD,
                 flow_control=False,
                 handshaking=False,
                 timeout=2.0,
                 ip_address=None,
                 tcp_port=7777,
                 **kwargs):

        # Call the parent init, then fill in values specific to the instrument
        GenericInstrument.__init__(self, serial_number, com_port, baud_rate, data_bits, stop_bits, parity, flow_control,
                                   handshaking, timeout, ip_address, tcp_port, **kwargs)

    class EMPowerSupplyServiceRequestEnableRegister(RegisterBase):
        """Class object representing the service request enable register LSB to MSB."""
        bit_names = [
            "",
            "operational_errors_summary",
            "hardware_errors_summary",
            "",
            "message_available",
            "event_summary",
            "",
            "operation_summary"
        ]

        def __init__(self,
                     operational_errors_summary,
                     hardware_errors_summary,
                     message_available,
                     event_summary,
                     operation_summary
                     ):
            self.operational_errors_summary = operational_errors_summary
            self.hardware_errors_summary = hardware_errors_summary
            self.message_available = message_available
            self.event_summary = event_summary
            self.operation_summary = operation_summary

    class EMPowerSupplyStatusByteRegister(RegisterBase):
        """Class object representing the status byte register LSB to MSB."""
        bit_names = [
            "",
            "operational_errors_summary",
            "hardware_errors_summary",
            "",
            "message_available",
            "event_summary",
            "service_request",
            "operation_summary"
        ]

        def __init__(self,
                     operational_errors_summary,
                     hardware_errors_summary,
                     message_available,
                     event_summary,
                     service_request,
                     operation_summary
                     ):
            self.operational_errors_summary = operational_errors_summary
            self.hardware_errors_summary = hardware_errors_summary
            self.message_available = message_available
            self.event_summary = event_summary
            self.service_request = service_request
            self.operation_summary = operation_summary

    class EMPowerSupplyStandardEventStatusRegister(RegisterBase):
        """Class object representing the standard event status register LSB to MSB."""
        bit_names = [
            "operation_complete",
            "",
            "query_error",
            "",
            "execution_error",
            "command_error",
            "",
            "power_on"
        ]

        def __init__(self,
                     operation_complete,
                     query_error,
                     execution_error,
                     command_error,
                     power_on
                     ):
            self.operation_complete = operation_complete
            self.query_error = query_error
            self.execution_error = execution_error
            self.command_error = command_error
            self.power_on = power_on

    class EMPowerSupplyOperationEventRegister(RegisterBase):
        """Class object representing the operation event register LSB to MSB."""
        bit_names = [
            "compliance",
            "ramp_done",
            "power_limit",
            "",
            "",
            "",
            "",
            ""
        ]

        def __init__(self,
                     compliance,
                     ramp_done,
                     power_limit
                     ):
            self.compliance = compliance
            self.ramp_done = ramp_done
            self.power_limit = power_limit

    class EMPowerSupplyHardwareErrorsRegister(RegisterBase):
        """Class object representing the hardware errors register LSB to MSB."""
        bit_names = [
            "output_control_failure",
            "dac_processor_not_responding",
            "output_over_current",
            "output_over_voltage",
            "temperature_fault",
            "output_stage_protect",
            "",
            ""
        ]

        def __init__(self,
                     output_control_failure,
                     dac_processor_not_responding,
                     output_over_current,
                     output_over_voltage,
                     temperature_fault,
                     output_stage_protect
                     ):
            self.output_control_failure = output_control_failure
            self.dac_processor_not_responding = dac_processor_not_responding
            self.output_over_current = output_over_current
            self.output_over_voltage = output_over_voltage
            self.temperature_fault = temperature_fault
            self.output_stage_protect = output_stage_protect

    class EMPowerSupplyOperationalErrorsRegister(RegisterBase):
        """Class object representing the operational errors register LSB to MSB."""
        bit_names = [
            "calibration_error",
            "external_current_program_error",
            "temperature_high",
            "low_line_voltage",
            "high_line_voltage",
            "magnet_flow_switch_fault",
            "power_supply_flow_switch_fault",
            "remote_enable_fault"
        ]

        def __init__(self,
                     calibration_error,
                     external_current_program_error,
                     temperature_high,
                     low_line_voltage,
                     high_line_voltage,
                     magnet_flow_switch_fault,
                     power_supply_flow_switch_fault,
                     remote_enable_fault
                     ):
            self.calibration_error = calibration_error
            self.external_current_program_error = external_current_program_error
            self.temperature_high = temperature_high
            self.low_line_voltage = low_line_voltage
            self.high_line_voltage = high_line_voltage
            self.magnet_flow_switch_fault = magnet_flow_switch_fault
            self.power_supply_flow_switch_fault = power_supply_flow_switch_fault
            self.remote_enable_fault = remote_enable_fault

    def command(self, command_string, check_errors=True):
        """Send a command to the instrument.

        Args:
            command_string (str): A serial command
            check_errors (bool): Specifies if command errors should be checked. Optional parameter. Defaults to True.
        """

        if check_errors:
            # Performs a query to check the errors.
            self.query(command_string)
        else:
            # Call generic command
            super().command(command_string)

    def query(self, query_string, check_errors=True):
        """Send a query to the instrument and return the response

        Args:
            query_string (str): A serial query ending in a question mark.

            check_errors (bool): Specifies if command errors should be checked. Optional parameter. Defaults to True.

        Returns:
            str: The instrument query response as a string.
        """

        if check_errors:
            # Append command error query (*R)
            query_string += "; *ESR?"

        # Generic query
        response = super().query(query_string)

        if check_errors:
            # Remove command error response from full response
            response_list = _parse_response(response)
            error_response = response_list.pop()
            register = self.EMPowerSupplyStandardEventStatusRegister.from_integer(int(error_response))
            if register.command_error:
                raise InstrumentException("Command Error: The instrument could not interpret the command due to a "
                                          "syntax error, an unrecognized header, unrecognized terminator, or an "
                                          "unsupported command.")
            if register.execution_error:
                raise InstrumentException("Execution Error: The instrument was instructed to do something not within "
                                          "its capabilities.")
            if register.query_error:
                raise InstrumentException("Query Error: The output queue is full.")
            response = ';'.join(response_list)

        return response

    def set_limits(self, max_current, max_ramp_rate):
        """Sets the upper setting limits for output current, and output current ramp rate.

            This is a software limit that will limit the setting of the values. Only limits internal setting of the
            current.

        Args:
            max_current (float): The maximum output current setting allowed. The Model 643 bounds are 0.0000 - 70.1000
                A. The Model 648 bounds are 0.0000 - 135.1000 A.

            max_ramp_rate (float): The maximum output current ramp rate setting allowed (0.0001 - 50.000 A/s).
        """
        self.command(f"LIMIT {max_current}, {max_ramp_rate}")

    def get_limits(self):
        """Returns the upper setting limits for output current, and output current ramp rate.

            This is a software limit that limits the setting of the values. Only limits the internal
            setting of the current.

        Returns:
            list[float]: List of [output_current, output_current_ramp_rate].
        """
        return [float(element) for element in self.query("LIMIT?").split(',')]

    def set_ramp_rate(self, ramp_rate):
        """Sets the output current ramp rate.

            This value will be used in both the positive and negative directions. Setting value is limited by set_limit.

        Args:
            ramp_rate (float): The rate at which the current will ramp when a new output current setting is entered
                (0.0001 - 50.000 A/s).
        """
        self.command(f"RATE {ramp_rate}")

    def get_ramp_rate(self):
        """Returns the output current ramp rate.

            This value is used in both the positive and negative directions.

        Returns:
            float: The rate at which the current will ramp when a new output current setting is entered.
        """
        return float(self.query("RATE?"))

    def set_ramp_segment(self, segment, current, ramp_rate):
        """Sets the current and ramp rate of one of the ramp segments.

        Args:
            segment (int): Specifies the ramp segment to be modified (1 - 5).
            current (float): Specifies the upper output current setting that will use this segment.
            ramp_rate (float): Specifies the rate at which the current will ramp. (0.0001 - 50.000 A/s).

        """
        self.command(f"RSEGS {segment}, {current}, {ramp_rate}")

    def get_ramp_segment(self, segment):
        """Returns the current and ramp rate of a specific ramp segment.

        Args:
            segment (int): Specifies the ramp segment to be modified (1 - 5).

        Returns:
            list[float]: List of current and ramp_rate settings. [current, ramp_rate].
        """
        return [float(x) for x in self.query(f"RSEGS? {segment}").split(',')]

    def set_ramp_segments_enable(self, state):
        """Specifies if ramp segments are to be used.

            Ramp segments are used to change the output current ramp rate based on the output current.

        Args:
            state (bool): The state of the ramp segments enable. 0=Disabled and 1=Enabled.
        """
        self.command(f"RSEG {int(state)}")

    def get_ramp_segments_enable(self):
        """Returns if ramp segments are to be used.

            Ramp segments are used to change the output current ramp rate based on the output current.

        Returns:
            bool: Whether ramp segments are enabled. 0=Disabled and 1=Enabled.
        """
        return bool(int(self.query("RSEG?")))

    def set_current(self, current):
        """Sets the output current setting.

            The setting value is limited by set_limit.

        Args:
            current (float): The output current value that the output will ramp to at the present ramp rate. The Model
                643 bounds are 0.0000 - +/-70.1000 A. The Model 648 bounds are 0.0000 - +/-135.1000 A.
        """
        self.command(f"SETI {current}")

    def get_current(self):
        """Returns the output current setting.

        Returns:
            float: The output current value that the output will ramp to at the present ramp rate.
        """
        return float(self.query("SETI?"))

    def get_measured_current(self):
        """Returns actual measured output current.

        Returns:
            float: Measured output current.
        """
        return float(self.query("RDGI?"))

    def get_measured_voltage(self):
        """Returns actual output voltage measured at the power supply terminals.

        Returns:
            float: Measured output voltage.
        """
        return float(self.query("RDGV?"))

    def stop_output_current_ramp(self):
        """Stops the output current ramp.

            Stops within 2 s of sending command. TO restart the ramp, use the set_current method to set a new output
            current set-point.
        """
        self.command("STOP")

    def set_internal_water(self, mode):
        """Configures the internal water mode.

        Args:
            mode (int): Internal water mode (0, 1, 2, or 3). 0 = Manual-Off, 1 = Manual-On, 2 = Auto, 3 = Disabled.
        """
        self.command(f"INTWTR {mode}")

    def get_internal_water(self) :
        """Returns the internal water mode.

        Returns:
            int: Internal water mode. 0 = Manual-Off, 1 = Manual-On, 2 = Auto, 3 = Disabled.

        """
        return int(self.query("INTWTR?"))

    def set_magnet_water(self, mode):
        """Configures the magnet water mode.

        Args:
            mode (int): Magnet water mode. (0, 1, 2, or 3). 0 = Manual-Off, 1 = Manual-On, 2 = Auto, 3 = Disabled.
        """
        self.command(f"MAGWTR {mode}")

    def get_magnet_water(self) :
        """Returns the magnet water mode.

        Returns:
            int: Magnet water mode. 0 = Manual-Off, 1 = Manual-On, 2 = Auto, 3 = Disabled.
        """
        return int(self.query("MAGWTR?"))

    def set_display_brightness(self, brightness_level):
        """Specifies display brightness.

        Args:
            brightness_level (int): The display brightness. 0=25%, 1=50%, 2=75%, 3=100%.
        """
        self.command(f"DISP {brightness_level}")

    def get_display_brightness(self) :
        """Returns display brightness.

        Returns:
            int: The display brightness. 0=25%, 1=50%, 2=75%, 3=100%.
        """
        return int(self.query("DISP?"))

    def set_front_panel_lock(self, lock_state, code):
        """Sets the lock status of the front panel keypad.

        Args:
            lock_state (int): The lock state to be set (0, 1, or 2). 0=unlock, 1=lock, and 2=lock limits.
            code (int): Keypad lock code required to make changes to the lock state of the front panel.
        """
        self.command(f"LOCK {lock_state},{code}")

    def get_front_panel_status(self):
        """Returns what lock state the front panel keypad is in.

        Returns:
            int: The state of the front panel keypad lock (0, 1, or 2). 0=unlock, 1=lock, 2=lock limits.
        """
        return int(self.query("LOCK?").split(',')[0])

    def get_front_panel_lock_code(self) :
        """Returns the lock code for the front panel.

        Returns:
            int: Front panel lock code.
        """
        return int(self.query("LOCK?").split(',')[1])

    def set_programming_mode(self, mode):
        """Sets the current programming mode of the instrument.

        Args:
            mode (int): Programming mode (0, 1, or 2). 0=Internal, 1=External, 2=Sum.
        """
        self.command(f"XPGM {mode}")

    def get_programming_mode(self):
        """Returns the current programming mode of the instrument.

        Returns:
            int: Programming mode. 0=Internal, 1=External, 2=Sum.
        """
        return int(self.query("XPGM?"))

    def set_ieee_488(self, terminator, eoi_enable, address):
        """Configures the IEEE-488 interface.

        Args:
            terminator(int): the terminator. 0=<CR><LF>, 1=<LF><CR>, 2=<LF>, 3=no terminator (must have EOI enabled).
            eoi_enable(int): Sets EOI (End of Interrupt) mode. 0=Enabled, 1=Disabled.
            address (int): Specifies IEEE address. 1 - 30(0 and 31 are reserved).
        """
        self.command(f"IEEE {terminator},{eoi_enable},{address}")

    def get_iee_488(self):
        """Returns IEEE-488 interface configuration.

        Returns:
            list[int]: [terminator, eoi_enable, address]
                terminator(int): the terminator. 0=<CR><LF>, 1=<LF><CR>, 2=<LF>, 3=no terminator (must
                have EOI enabled).
                eoi_enable(int): Sets EOI (End of Interrupt) mode. 0=Enabled, 1=Disabled.
                address (int): Specifies IEEE address. 1 - 30(0 and 31 are reserved).
        """
        return [int(x) for x in self.query("IEEE?").split(',')]

    def set_ieee_interface_mode(self, mode):
        """Sets the interface mode of the instrument.

        Args:
            mode (int): Interface mode. 0, 1 or 2. 0=local, 1=remote, and 2=remote with local lockout.
        """
        self.command(f"MODE {mode}")

    def get_ieee_interface_mode(self):
        """Returns the interface mode of the instrument.

        Returns:
            int: Interface mode of the instrument. 0, 1 or 2. 0=local, 1=remote, and 2=remote with local lockout.
        """
        return int(self.query("MODE?"))

    def set_factory_defaults(self):
        """Sets all configuration values to factory defaults and resets the instrument.

            The instrument must be at zero amps for this command to work.
        """
        self.command("DFLT 99")

    def reset_instrument(self):
        """Sets the controller parameters to power-up settings.

            Use the set_factory_defaults command to set factory-defaults.
        """
        self.command("*RST")

    def clear_interface(self):
        """Clears the event registers in all register groups. Also clears the error queue.

            Clears the bits in the Status Byte Register, Standard Event Status Register, and Operation event Register,
            and terminates al pending operations. Clears the interface, but not the instrument. The related instrument
            command is reset_instrument.
        """
        self.command("*CLS")

    def get_self_test(self):
        """Returns result of instrument self test completed at power up.

        Returns:
            bool: True means errors found, and False means no errors found.
        """
        return bool(int(self.query("*TST?")))

    def set_service_request_enable_mask(self, register_mask):
        """Configures the Service Request Enable Register.

            The Service Request Enable Register determines which summary bits of the Status
            Byte may set bit 6 (RQS/MSS) of the Status Byte to generate a Service Request.

        Args:
            register_mask (ElectromagnetPowerSupply.EMPowerSupplyServiceRequestEnableRegister): Register configuration object.
        """
        self.command(f"*SRE {register_mask.to_integer()}")

    def get_service_request_enable_mask(self):
        """Returns Service Request Enable Register configuration.

            The Service Request Enable Register determines which summary bits of the Status
            Byte may set bit 6 (RQS/MSS) of the Status Byte to generate a Service Request.

        Returns:
            ElectromagnetPowerSupply.EMPowerSupplyServiceRequestEnableRegister: Register configuration object.
        """
        bit_weighting = int(self.query("*SRE?"))
        return self.EMPowerSupplyServiceRequestEnableRegister.from_integer(bit_weighting)

    def get_status_byte(self):
        """Returns state of the Status Byte Register.

            The Status Byte register, typically referred to as the Status Byte, is a non-latching,
            read-only register that contains all the summary bits from the register sets.

        Returns:
            ElectromagnetPowerSupply.EMPowerSupplyStatusByteRegister: Register state object.
        """
        bit_weighting = int(self.query("*STB?"))
        return self.EMPowerSupplyStatusByteRegister.from_integer(bit_weighting)

    def set_standard_event_status_enable_mask(self, register_mask):
        """Configures Standard Event Status Enable Register group.

            The Standard Event Status Enable Register determines which bits in the Standard
            Event Status Register will set the summary bit in the Status Byte (bit 5).

        Args:
            register_mask (ElectromagnetPowerSupply.EMPowerSupplyStandardEventStatusRegister): Register configuration
                object.
        """
        self.command(f"*ESE {register_mask.to_integer()}")

    def get_standard_event_status_enable_mask(self):
        """Returns Standard Event Status Enable Register configuration.

            The Standard Event Status Enable Register determines which bits in the Standard
            Event Status Register will set the summary bit in the Status Byte (bit 5).

        Returns:
            ElectromagnetPowerSupply.EMPowerSupplyStandardEventStatusRegister: Register configuration object.
        """
        bit_weighting = int(self.query("*ESE?"))
        return self.EMPowerSupplyStandardEventStatusRegister.from_integer(bit_weighting)

    def get_standard_event_status_event(self):
        """Returns state of the Standard Event Status Register.

            Bits in this register correspond to various system events and latch when the event
            occurs. When an event bit is set, subsequent events corresponding to that bit are
            ignored. Set bits remain latched until the register is reset by this query or clear_interface.

        Returns:
            ElectromagnetPowerSupply.EMPowerSupplyStandardEventStatusRegister: Register state object.
        """
        bit_weighting = int(self.query("*ESR?"))
        return self.EMPowerSupplyStandardEventStatusRegister.from_integer(bit_weighting)

    def set_operation_event_enable_mask(self, register_mask):
        """Configures the Operational Event Enable Register.

            Each bit has a bit weighting and represents the enable/disable mask of the corresponding operational status
            bit in the Operational Status Register. This determines which status bits can set the corresponding summary
            bit in the Status Byte Register.

        Args:
            ElectromagnetPowerSupply.EMPowerSupplyOperationEventRegister: Register configuration object.
        """
        self.command(f"OPSTE {register_mask.to_integer()}")

    def get_operation_event_enable_mask(self):
        """Returns Operational Event Enable Register configuration.

            Each bit has a bit weighting and represents the enable/disable mask of the corresponding operational status
            bit in the Operational Status Register. This determines which status bits can set the corresponding summary
            bit in the Status Byte Register.

        Returns:
            ElectromagnetPowerSupply.EMPowerSupplyOperationEventRegister: Register configuration object.
        """
        bit_weighting = int(self.query("OPSTE?"))
        return self.EMPowerSupplyOperationEventRegister.from_integer(bit_weighting)

    def get_operation_event_condition(self):
        """Returns the real-time state of the operation event bits.

            The condition register constantly monitors the instrument status. The data bits are real-time and are not
            latched or buffered. The register is read-only.

        Returns:
            ElectromagnetPowerSupply.EMPowerSupplyOperationEventRegister: Object with each of the register bits' status.
        """
        weighted_operation_events = int(self.query("OPSTR?"))
        return self.EMPowerSupplyOperationEventRegister.from_integer(weighted_operation_events)

    def get_operation_event_event(self):
        """Returns the latched state of the operation event bits.

            Bits in the event register correspond to various system events and latch when the event occurs. When
            an event bit is set, subsequent events corresponding to that bit are ignored.

        Returns:
            ElectromagnetPowerSupply.EMPowerSupplyOperationEventRegister: Object with each of the register bits' status.
        """
        weighted_operation_events = int(self.query("OPST?"))
        return self.EMPowerSupplyOperationEventRegister.from_integer(weighted_operation_events)

    def set_hardware_error_enable_mask(self, register_mask):
        """Sets which hardware error bits will set the summary bit in the Status Byte Register.

            Each bit has a bit weighting and represents the enable/disable mask of the corresponding error bits in the
            Error Status Register. This determines which status bits can set the corresponding summary bits in the
            Status Byte Register.

        Args:
            register_mask (ElectromagnetPowerSupply.EMPowerSupplyHardwareErrorsRegister): Register mask configuration
                object.
        """
        operational_mask = self.query("ERSTE?").split(',')[1]
        self.command(f"ERSTE {register_mask.to_integer()},{operational_mask}")

    def get_hardware_error_enable_mask(self):
        """Returns which hardware error bits will set the summary bit in the Status Byte Register.

            Each bit has a bit weighting and represents the enable/disable mask of the corresponding error bits in the
            Error Status Register. This determines which status bits can set the corresponding summary bits in the
            Status Byte Register.

        Returns:
            ElectromagnetPowerSupply.EMPowerSupplyHardwareErrorsRegister: Register mask configuration object.
        """
        hardware_mask = int(self.query("ERSTE?").split(',')[0])
        return self.EMPowerSupplyHardwareErrorsRegister.from_integer(hardware_mask)

    def get_hardware_error_condition(self):
        """Returns the real-time state of the hardware error bits.

            The condition register constantly monitors the instrument status. The data bits are real-time and are not
            latched or buffered. The register is read-only.

        Returns:
            ElectromagnetPowerSupply.EMPowerSupplyHardwareErrorsRegister: Object with each of the register bits' status.
        """
        weighted_hardware_errors = int(self.query("ERST?").split(',')[0])
        return self.EMPowerSupplyHardwareErrorsRegister.from_integer(weighted_hardware_errors)

    def get_hardware_error_event(self):
        """Returns the latched state of the hardware error bits.

            Bits in the event register correspond to various system events and latch when the event occurs. When
            an event bit is set, subsequent events corresponding to that bit are ignored.

        Returns:
            ElectromagnetPowerSupply.EMPowerSupplyHardwareErrorsRegister: Object with each of the register bits' status.
        """
        weighted_hardware_errors = int(self.query("ERSTR?").split(',')[0])
        return self.EMPowerSupplyHardwareErrorsRegister.from_integer(weighted_hardware_errors)

    def set_operational_error_enable_mask(self, register_mask):
        """Sets which operational error bits will set the summary bit in the Status Byte Register.

            Each bit has a bit weighting and represents the enable/disable mask of the corresponding error bits in the
            Error Status Register. This determines which status bits can set the corresponding summary bits in the
            Status Byte Register.

        Args:
            register_mask (ElectromagnetPowerSupply.EMPowerSupplyHardwareErrorsRegister): Register mask configuration
                object.
        """
        hardware_mask = self.query("ERSTE?").split(',')[0]
        self.command(f"ERSTE {register_mask.to_integer()},{hardware_mask}")

    def get_operational_error_enable_mask(self):
        """Returns which operational error bits will set the summary bit in the Status Byte Register.

            Each bit has a bit weighting and represents the enable/disable mask of the corresponding error bits in the
            Error Status Register. This determines which status bits can set the corresponding summary bits in the
            Status Byte Register.

        Returns:
            ElectromagnetPowerSupply.EMPowerSupplyHardwareErrorsRegister: Register mask configuration object.
        """
        operational_mask = int(self.query("ERSTE?").split(',')[1])
        return self.EMPowerSupplyOperationalErrorsRegister.from_integer(operational_mask)

    def get_operational_error_condition(self):
        """Returns the real-time state of the operational error bits.

            The condition register constantly monitors the instrument status. The data bits are real-time and are not
            latched or buffered. The register is read-only.

        Returns:
            ElectromagnetPowerSupply.EMPowerSupplyOperationalErrorsRegister: Object with each of the register bits' status.
        """
        weighted_operational_errors = int(self.query("ERST?").split(',')[1])
        return self.EMPowerSupplyOperationalErrorsRegister.from_integer(weighted_operational_errors)

    def get_operational_error_event(self):
        """Returns the latched state of the operational error bits.

            Bits in the event register correspond to various system events and latch when the event occurs. When
            an event bit is set, subsequent events corresponding to that bit are ignored.

        Returns:
            ElectromagnetPowerSupply.EMPowerSupplyOperationalErrorsRegister: Object with each of the register bits' status.
        """
        weighted_operational_bits = int(self.query("ERSTR?").split(',')[1])
        return self.EMPowerSupplyOperationalErrorsRegister.from_integer(weighted_operational_bits)


# Create an aliases using the product names
Model643 = ElectromagnetPowerSupply
Model648 = ElectromagnetPowerSupply

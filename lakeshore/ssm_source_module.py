"""Implements functionality unique to the M81 Source Modules."""

from lakeshore.xip_instrument import RegisterBase
from lakeshore.ssm_base_module import SSMSystemModuleQuestionableRegister, BaseModule


class SSMSystemSourceModuleOperationRegister(RegisterBase):
    """Class object representing the operation status register of a source module"""

    bit_names = [
        "v_limit",
        "i_limit"
    ]

    def __init__(
            self,
            v_limit,
            i_limit):
        self.v_limit = v_limit
        self.i_limit = i_limit


class SourceModule(BaseModule):
    """Class for interaction with a specific source channel of the M81 instrument"""

    def get_multiple(self, *data_sources):
        r"""Gets a list of values corresponding to the input data sources for this module.

            Args:
                data_sources str: Variable length list of DATASOURCE_MNEMONIC.

            Returns:
                Tuple of values corresponding to the given data sources for this module
        """

        elements = [(data_source, self.module_number) for data_source in data_sources]
        return self.device.get_multiple(*elements)

    def get_name(self):
        """Returns the user-settable name of the module"""

        return self.device.query('SOURce{}:NAME?'.format(self.module_number)).strip('\"')

    def set_name(self, new_name):
        """Set the name of the module"""

        self.device.command('SOURce{}:NAME "{}"'.format(self.module_number, new_name))

    def get_model(self):
        """Returns the model of the module (i.e. BCS-10)"""

        return self.device.query('SOURce{}:MODel?'.format(self.module_number)).strip('\"')

    def get_serial(self):
        """Returns the serial number of the module (i.e. LSA1234)"""

        return self.device.query('SOURce{}:SERial?'.format(self.module_number)).strip('\"')

    def get_hw_version(self):
        """Returns the hardware version of the module"""

        return int(self.device.query('SOURce{}:HWVersion?'.format(self.module_number)))

    def get_self_cal_status(self):
        """Returns the status of the last self calibration of the module"""

        return self.device.query('SOURce{}:SCALibration:STATus?'.format(self.module_number))

    def run_self_cal(self):
        """Run a self calibration for the module"""

        self.device.command('SOURce{}:SCALibration:RUN'.format(self.module_number))

    def reset_self_cal(self):
        """Restore factory self calibration for the module"""

        self.device.command('SOURce{}:SCALibration:RESet'.format(self.module_number))

    def get_enable_state(self):
        """Returns the output state of the module"""

        return bool(int(self.device.query('SOURce{}:STATe?'.format(self.module_number))))

    def set_enable_state(self, state):
        """Set the enable state of the module

            Args:
                state (bool):
                    The new output state
        """

        self.device.command('SOURce{}:STATe {}'.format(self.module_number, str(int(state))))

    def enable(self):
        """Sets the enable state of the module to True"""

        self.set_enable_state(True)

    def disable(self):
        """Sets the enable state of the module to False"""

        self.set_enable_state(False)

    def get_excitation_mode(self):
        """Returns the excitation mode of the module. 'CURRENT' or 'VOLTAGE'."""

        return self.device.query('SOURce{}:FUNCtion:MODE?'.format(self.module_number))

    def set_excitation_mode(self, excitation_mode):
        """Sets the excitation mode of the module

            Args:
                excitation_mode (str):
                    The new excitation mode ('CURRENT' or 'VOLTAGE')
        """

        self.device.command('SOURce{}:FUNCtion:MODE {}'.format(self.module_number, excitation_mode))

    def go_to_current_mode(self):
        """Sets the excitation mode of the module to 'CURRENT'"""

        self.set_excitation_mode('CURRent')

    def go_to_voltage_mode(self):
        """Sets the excitation mode of the module to 'VOLTAGE'"""

        self.set_excitation_mode('VOLTage')

    def get_shape(self):
        """Returns the signal shape of the module. 'DC' or 'SINUSOID'."""

        return self.device.query('SOURce{}:FUNCtion:SHAPe?'.format(self.module_number))

    def set_shape(self, shape):
        """Sets the signal shape of the module

            Args:
                shape (str):
                    The new signal shape ('DC', 'SINUSOID', 'TRIANGLE', 'SQUARE')
        """

        self.device.command('SOURce{}:FUNCtion:SHAPe {}'.format(self.module_number, shape))

    def get_frequency(self):
        """Returns the excitation frequency of the module"""

        return float(self.device.query('SOURce{}:FREQuency?'.format(self.module_number)))

    def set_frequency(self, frequency):
        """Sets the excitation frequency of the module

            Args:
                frequency (float):
                    The new excitation frequency
        """
        self.device.command('SOURce{}:FREQuency {}'.format(self.module_number, str(frequency)))

    def get_sync_state(self):
        """Returns whether the source channel synchronization feature is engaged

            If true, this channel will ignore its own frequency, and instead track the frequency of the synchronization source.
            If false, this channel will generate its own frequency.
        """

        return bool(int(self.device.query('SOURce{}:SYNChronize:STATe?'.format(self.module_number))))

    def get_sync_source(self):
        """Returns the channel used for frequency synchronization"""

        return self.device.query('SOURce{}:SYNChronize:SOURce?'.format(self.module_number))

    def get_sync_phase_shift(self):
        """Returns the phase shift applied between the synchronization source and this channel"""

        return float(self.device.query('SOURce{}:SYNChronize:PHASe?'.format(self.module_number)))

    def configure_sync(self, source, phase_shift, enable_sync=True):
        """Configure the source channel synchronization feature

            Args:
                source (str):
                    The channel used for synchronization ('S1', 'S2', 'S3', or 'RIN').
                    This channel will follow the frequency set for the specifed channel.

                phase_shift (float):
                    The phase shift applied between the synchronization source and this channel in degrees.

                enable_sync (bool):
                    If true, this channel will ignore its own frequency, and instead track the frequency of the synchronization source.
                    If false, this channel will generate its own frequency.
        """
        self.device.command('SOURce{}:SYNChronize:SOURce {}'.format(self.module_number, source))
        self.device.command('SOURce{}:SYNChronize:PHASe {}'.format(self.module_number, str(phase_shift)))
        self.device.command('SOURce{}:SYNChronize:STATe {}'.format(self.module_number, str(int(enable_sync))))

    def get_duty(self):
        """Returns the duty cycle of the module"""

        return float(self.device.query('SOURce{}:DCYCle?'.format(self.module_number)))

    def set_duty(self, duty):
        """Sets the duty cycle of the module

            Args:
                duty (float):
                    The new duty cycle
        """

        self.device.command('SOURce{}:DCYCle {}'.format(self.module_number, str(duty)))

    def get_coupling(self):
        """Returns the coupling type of the module. 'AC' or 'DC'."""

        return self.device.query('SOURce{}:COUPling?'.format(self.module_number))

    def set_coupling(self, coupling):
        """Sets the coupling of the module

            Args:
                coupling (str):
                    The new coupling type ('AC', or 'DC')
        """
        self.device.command('SOURce{}:COUPling {}'.format(self.module_number, coupling))

    def use_ac_coupling(self):
        """Sets the coupling type of the module to 'AC'"""

        self.set_coupling('AC')

    def use_dc_coupling(self):
        """Sets the coupling type of the module to 'DC'"""

        self.set_coupling('DC')

    def get_guard_state(self):
        """Returns the guard state of the module"""

        return bool(int(self.device.query('SOURce{}:GUARd?'.format(self.module_number))))

    def set_guard_state(self, guard_state):
        """Sets the guard state of the module

            Args:
                guard_state (bool):
                    The new guard state (True to enable guards, False to disable guards)
        """

        self.device.command('SOURce{}:GUARd {}'.format(self.module_number, str(int(guard_state))))

    def enable_guards(self):
        """Sets the guard state of the module to True"""

        self.set_guard_state(True)

    def disable_guards(self):
        """Sets the guard state of the module to False"""

        self.set_guard_state(False)

    def get_cmr_source(self):
        """Returns the Common Mode Reduction (CMR) source. 'INTernal', or 'EXTernal'."""

        return self.device.query('SOURce{}:CMR:SOURce?'.format(self.module_number))

    def set_cmr_source(self, cmr_source):
        """Sets the Common Mode Reduction (CMR) source.

            Args:
                cmr_source (str):
                    The new CMR source ('INTernal', or 'EXTernal')
        """

        self.device.command('SOURce{}:CMR:SOURce {}'.format(self.module_number, cmr_source))

    def get_cmr_state(self):
        """Returns the Common Mode Reduction (CMR) state of the module"""

        return bool(int(self.device.query('SOURce{}:CMR:STATe?'.format(self.module_number))))

    def set_cmr_state(self, cmr_state):
        """Sets the Common Mode Reduction (CMR) state of the module

            Args:
                cmr_state (bool):
                    The new CMR state (True to enable CMR, False to disable CMR)
        """

        self.device.command('SOURce{}:CMR:STATe {}'.format(self.module_number, str(int(cmr_state))))

    def enable_cmr(self):
        """Sets the CMR state of the module to True"""

        self.set_cmr_state(True)

    def disable_cmr(self):
        """Sets the CMR state of the module to False"""

        self.set_cmr_state(False)

    def configure_cmr(self, cmr_source, cmr_state=True):
        """Configure Common Mode Reduction (CMR)

            Args:
                cmr_source (str):
                    The new CMR source ('INTernal', or 'EXTernal')

                cmr_state (bool):
                    The new CMR state (True to enable CMR, False to disable CMR)
        """

        self.set_cmr_source(cmr_source)
        self.set_cmr_state(cmr_state)

    def get_i_range(self):
        """Returns the present current range of the module in Amps"""

        return float(self.device.query('SOURce{}:CURRent:RANGe?'.format(self.module_number)))

    def get_i_ac_range(self):
        """Returns the present AC current range of the module in Amps"""

        return float(self.device.query('SOURce{}:CURRent:RANGe:AC?'.format(self.module_number)))

    def get_i_dc_range(self):
        """Returns the present DC current range of the module in Amps"""

        return float(self.device.query('SOURce{}:CURRent:RANGe:DC?'.format(self.module_number)))

    def get_i_autorange_status(self):
        """Returns whether automatic selection of the current range is enabled for this module"""

        return bool(int(self.device.query('SOURce{}:CURRent:RANGe:AUTO?'.format(self.module_number))))

    def configure_i_range(self, autorange, max_level=None, max_ac_level=None, max_dc_level=None):
        """Sets up current ranging for this module

            Args:
                autorange (bool):
                    True to enable automatic range selection. False for manual ranging.

                max_level (float):
                    The largest current that needs to be sourced.

                max_ac_level (float):
                    The largest AC current that needs to be sourced. Separate AC and DC ranges are only available on some modules.

                max_dc_level (float):
                    The largest DC current that needs to be sourced. Separate AC and DC ranges are only available on some modules.
        """

        if autorange:
            if max_level is not None or max_ac_level is not None or max_dc_level is not None:
                raise ValueError('If autorange is selected, a manual range cannot be specified.')

            self.device.command('SOURce{}:CURRent:RANGe:AUTO 1'.format(self.module_number))
        else:
            if max_level is not None:
                if max_ac_level is not None or max_dc_level is not None:
                    raise ValueError('Either a single range, or separate AC and DC ranges can be supplied, not both.')

                self.device.command('SOURce{}:CURRent:RANGe {}'.format(self.module_number, str(max_level)))
            else:
                if max_ac_level is not None:
                    self.device.command('SOURce{}:CURRent:RANGe:AC {}'.format(self.module_number, str(max_ac_level)))
                if max_dc_level is not None:
                    self.device.command('SOURce{}:CURRent:RANGe:DC {}'.format(self.module_number, str(max_dc_level)))

    def get_i_amplitude(self):
        """Returns the current amplitude for the module in Amps"""

        return float(self.device.query('SOURce{}:CURRent:LEVel:AMPLitude?'.format(self.module_number)))

    def set_i_amplitude(self, amplitude):
        """Sets the current amplitude for the module

            Args:
                amplitude (float):
                    The new current amplitude in Amps
        """
        self.device.command('SOURce{}:CURRent:LEVel:AMPLitude {}'.format(self.module_number, str(amplitude)))

    def get_i_offset(self):
        """Returns the current offset for the module in Amps"""

        return float(self.device.query('SOURce{}:CURRent:LEVel:OFFSet?'.format(self.module_number)))

    def set_i_offset(self, offset):
        """Sets the current offset for the module

            Args:
                offset (float):
                    The new current offset in Amps
        """

        self.device.command('SOURce{}:CURRent:LEVel:OFFSet {}'.format(self.module_number, str(offset)))

    def apply_dc_current(self, level, enable_output=True):
        """Apply DC current

            Args:
                level (float):
                    DC current level in Amps

                enable_output (bool):
                    Set the enable state of the module to True
        """

        self.set_excitation_mode('CURRent')
        self.set_shape('DC')
        self.set_i_amplitude(level)

        if enable_output:
            self.enable()

    def apply_ac_current(self, frequency, amplitude, offset=0.0, enable_output=True):
        """Apply AC current

            Args:
                frequency (float):
                    Excitation frequency in Hz

                amplitude (float):
                    Current amplitude in Amps

                offset (float):
                    Current offset in Amps

                enable_output (bool):
                    Set the enable state of the module to True
        """

        self.set_excitation_mode('CURRent')
        self.set_frequency(frequency)
        self.set_shape('SINusoid')
        self.set_i_amplitude(amplitude)
        self.set_i_offset(offset)

        if enable_output:
            self.enable()

    def get_i_limit(self):
        """Returns the current limit enforced by the module in Amps"""

        return float(self.device.query('SOURce{}:CURRent:PROTection?'.format(self.module_number)))

    def set_i_limit(self, i_limit):
        """Sets the current limit enforced by the module

            Args:
                i_limit (float):
                    The new limit to apply in Amps
        """
        self.device.command('SOURce{}:CURRent:PROTection {}'.format(self.module_number, str(i_limit)))

    def get_i_limit_status(self):
        """Returns whether the current limit circuitry is presently engaged and limiting the current sourced by the module"""

        return bool(int(self.device.query('SOURce{}:CURRent:PROTection:TRIPped?'.format(self.module_number))))

    def get_voltage_range(self):
        """Returns the present voltage range of the module in Volts"""

        return float(self.device.query('SOURce{}:VOLTage:RANGe?'.format(self.module_number)))

    def get_voltage_ac_range(self):
        """Returns the present AC voltage range of the module in Volts"""

        return float(self.device.query('SOURce{}:VOLTage:RANGe:AC?'.format(self.module_number)))

    def get_voltage_dc_range(self):
        """Returns the present DC voltage range of the module in Volts"""

        return float(self.device.query('SOURce{}:VOLTage:RANGe:DC?'.format(self.module_number)))

    def get_voltage_autorange_status(self):
        """Returns whether automatic selection of the voltage range is enabled for this module"""

        return bool(int(self.device.query('SOURce{}:VOLTage:RANGe:AUTO?'.format(self.module_number))))

    def configure_voltage_range(self, autorange, max_level=None, max_ac_level=None, max_dc_level=None):
        """Sets up voltage ranging for this module

            Args:
                autorange (bool):
                    True to enable automatic range selection. False for manual ranging.

                max_level (float):
                    The largest voltage that needs to be sourced.

                max_ac_level (float):
                    The largest AC voltage that needs to be sourced. Separate AC and DC ranges are only available on some modules.

                max_dc_level (float):
                    The largest DC voltage that needs to be sourced. Separate AC and DC ranges are only available on some modules.
        """

        if autorange:
            if max_level is not None or max_ac_level is not None or max_dc_level is not None:
                raise ValueError('If autorange is selected, a manual range cannot be specified.')

            self.device.command('SOURce{}:VOLTage:RANGe:AUTO 1'.format(self.module_number))
        else:
            if max_level is not None:
                if max_ac_level is not None or max_dc_level is not None:
                    raise ValueError('Either a single range, or separate AC and DC ranges can be supplied, not both.')

                self.device.command('SOURce{}:VOLTage:RANGe {}'.format(self.module_number, str(max_level)))
            else:
                if max_ac_level is not None:
                    self.device.command('SOURce{}:VOLTage:RANGe:AC {}'.format(self.module_number, str(max_ac_level)))
                if max_dc_level is not None:
                    self.device.command('SOURce{}:VOLTage:RANGe:DC {}'.format(self.module_number, str(max_dc_level)))

    def get_voltage_amplitude(self):
        """Returns the voltage amplitude for the module in Volts"""

        return float(self.device.query('SOURce{}:VOLTage:LEVel:AMPLitude?'.format(self.module_number)))

    def set_voltage_amplitude(self, amplitude):
        """Sets the voltage amplitude for the module

            Args:
                amplitude (float):
                    The new voltage amplitude in Volts
        """

        self.device.command('SOURce{}:VOLTage:LEVel:AMPLitude {}'.format(self.module_number, str(amplitude)))

    def get_voltage_offset(self):
        """Returns the voltage offset for the module in Volts"""

        return float(self.device.query('SOURce{}:VOLTage:LEVel:OFFSet?'.format(self.module_number)))

    def set_voltage_offset(self, offset):
        """Sets the voltage offset for the module

            Args:
                offset (float):
                    The new voltage offset in Volts
        """

        self.device.command('SOURce{}:VOLTage:LEVel:OFFSet {}'.format(self.module_number, str(offset)))

    def apply_dc_voltage(self, level, enable_output=True):
        """Apply DC voltage

            Args:
                level (float):
                    DC voltage level in Volts

                enable_output (bool):
                    Set the enable state of the module to True
        """

        self.set_excitation_mode('VOLTage')
        self.set_shape('DC')
        self.set_i_amplitude(level)

        if enable_output:
            self.enable()

    def apply_ac_voltage(self, frequency, amplitude, offset=0.0, enable_output=True):
        """Apply AC voltage

            Args:
                frequency (float):
                    Excitation frequency in Hz

                amplitude (float):
                    Voltage amplitude in Volts

                offset (float):
                    Voltage offset in Volts

                enable_output (bool):
                    Set the enable state of the module to True
        """

        self.set_excitation_mode('VOLTage')
        self.set_frequency(frequency)
        self.set_shape('SINusoid')
        self.set_i_amplitude(amplitude)
        self.set_i_offset(offset)

        if enable_output:
            self.enable()

    def get_voltage_limit(self):
        """Returns the voltage limit enforced by the module in Volts"""

        return float(self.device.query('SOURce{}:VOLTage:PROTection?'.format(self.module_number)))

    def set_voltage_limit(self, v_limit):
        """Sets the voltage limit enforced by the module

            Args:
                v_limit (float):
                    The new limit to apply in Volts
        """

        self.device.command('SOURce{}:VOLTage:PROTection {}'.format(self.module_number, str(v_limit)))

    def get_voltage_limit_status(self):
        """Returns whether the voltage limit circuitry is presently engaged and limiting the voltage at the output of the module"""

        return bool(int(self.device.query('SOURce{}:VOLTage:PROTection:TRIPped?'.format(self.module_number))))

    def get_present_questionable_status(self):
        """Returns the names of the questionable status register bits and their values"""

        response = self.device.query('STATus:QUEStionable:SOURce{}:CONDition?'.format(self.module_number), check_errors=False)
        status_register = SSMSystemModuleQuestionableRegister.from_integer(response)

        return status_register

    def get_questionable_events(self):
        """Returns the names of questionable event status register bits that are currently high.
        The event register is latching and values are reset when queried."""

        response = self.device.query('STATus:QUEStionable:SOURce{}:EVENt?'.format(self.module_number), check_errors=False)
        status_register = SSMSystemModuleQuestionableRegister.from_integer(response)

        return status_register

    def get_questionable_event_enable_mask(self):
        """Returns the names of the questionable event enable register bits and their values.
        These values determine which questionable bits propagate to the questionable event register."""

        response = self.device.query('STATus:QUEStionable:SOURce{}:ENABle?'.format(self.module_number), check_errors=False)
        status_register = SSMSystemModuleQuestionableRegister.from_integer(response)

        return status_register

    def set_questionable_event_enable_mask(self, register_mask):
        """Configures the values of the questionable event enable register bits.
        These values determine which questionable bits propagate to the questionable event register.

            Args:
                register_mask ([Instrument]QuestionableRegister):
                    An instrument specific QuestionableRegister class object with all bits configured true or false.
        """

        integer_representation = register_mask.to_integer()
        self.device.command('STATus:QUEStionable:SOURce{}:ENABle {}'.format(self.module_number, integer_representation), check_errors=False)

    def get_present_operation_status(self):
        """Returns the names of the operation status register bits and their values"""

        response = self.device.query('STATus:OPERation:SOURce{}:CONDition?'.format(self.module_number), check_errors=False)
        status_register = SSMSystemSourceModuleOperationRegister.from_integer(response)

        return status_register

    def get_operation_events(self):
        """Returns the names of operation event status register bits that are currently high.
        The event register is latching and values are reset when queried."""

        response = self.device.query('STATus:OPERation:SOURce{}:EVENt?'.format(self.module_number), check_errors=False)
        status_register = SSMSystemSourceModuleOperationRegister.from_integer(response)

        return status_register

    def get_operation_event_enable_mask(self):
        """Returns the names of the operation event enable register bits and their values.
        These values determine which operation bits propagate to the operation event register."""

        response = self.device.query('STATus:OPERation:SOURce{}:ENABle?'.format(self.module_number), check_errors=False)
        status_register = SSMSystemSourceModuleOperationRegister.from_integer(response)

        return status_register

    def set_operation_event_enable_mask(self, register_mask):
        """Configures the values of the operation event enable register bits.
        These values determine which operation bits propagate to the operation event register.

            Args:
                register_mask ([Instrument]OperationRegister):
                    An instrument specific OperationRegister class object with all bits configured true or false.
        """

        integer_representation = register_mask.to_integer()
        self.device.command('STATus:OPERation:SOURce{}:ENABle {}'.format(self.module_number, integer_representation), check_errors=False)

    def get_identify_state(self):
        """Returns the identification state for the given pod."""
        response = bool(int(self.device.query('SOURce{}:IDENtify?'.format(self.module_number), check_errors=False)))
        return response

    def set_identify_state(self, state):
        """Returns the identification state for the given pod.

            Args:
                state (bool):
                    The desired state for the LED, 1 for identify, 0 for normal state
        """
        self.device.command('SOURce{}:IDENtify {}'.format(self.module_number, int(state)), check_errors=False)

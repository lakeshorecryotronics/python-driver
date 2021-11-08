"""Implements functionality unique to the M81 Measure Modules."""

from lakeshore.xip_instrument import RegisterBase
from lakeshore.ssm_base_module import SSMSystemModuleQuestionableRegister, BaseModule


class SSMSystemMeasureModuleOperationRegister(RegisterBase):
    """Class object representing the operation status register of a measure module"""

    bit_names = [
        "overload",
        "settling",
        "unlocked"
    ]

    def __init__(
            self,
            overload,
            settling,
            unlocked):
        self.overload = overload
        self.settling = settling
        self.unlocked = unlocked


class MeasureModule(BaseModule):
    """Class for interaction with a specific measure channel of the M81 instrument"""

    def get_name(self):
        """Returns the user-settable name of the module"""

        return self.device.query(f'SENSe{self.module_number}:NAME?').strip('\"')

    def set_name(self, new_name):
        """Set the name of the module"""

        self.device.command(f'SENSe{self.module_number}:NAME "{new_name}"')

    def get_model(self):
        """Returns the model of the module (i.e. VM-10)"""

        return self.device.query(f'SENSe{self.module_number}:MODel?').strip('\"')

    def get_serial(self):
        """Returns the serial number of the module (i.e. LSA1234)"""

        return self.device.query(f'SENSe{self.module_number}:SERial?').strip('\"')

    def get_hw_version(self):
        """Returns the hardware version of the module"""

        return int(self.device.query(f'SENSe{self.module_number}:HWVersion?'))

    def get_self_cal_status(self):
        """Returns the status of the last self calibration of the module"""

        return self.device.query(f'SENSe{self.module_number}:SCALibration:STATus?')

    def run_self_cal(self):
        """Run a self calibration for the module"""

        self.device.command(f'SENSe{self.module_number}:SCALibration:RUN')

    def reset_self_cal(self):
        """Restore factory self calibration for the module"""

        self.device.command(f'SENSe{self.module_number}:SCALibration:RESet')

    def get_averaging_time(self):
        """Returns the averaging time of the module in Power Line Cycles. Not relevant in lock-in mode."""

        return float(self.device.query(f'SENSe{self.module_number}:NPLCycles?'))

    def set_averaging_time(self, nplc):
        """Sets the averaging time of the module. Not relevant in lock-in mode.

            Args:
                nplc (float):
                    The new number of power line cycles to average
        """

        self.device.command(f'SENSe{self.module_number}:NPLCycles {float(nplc)}')

    def get_mode(self):
        """Returns the measurement mode of the module. 'DC', 'AC', or 'LIA'."""

        return self.device.query(f'SENSe{self.module_number}:MODE?')

    def set_mode(self, mode):
        """Sets the measurement mode of the module

            Args:
                mode (str):
                    The new measurement mode ('DC', 'AC', or 'LIA')
        """

        self.device.command(f'SENSe{self.module_number}:MODE {mode}')

    def get_coupling(self):
        """Return input coupling of the module. 'AC' or 'DC'."""

        return self.device.query(f'SENSe{self.module_number}:COUPling?')

    def set_coupling(self, coupling):
        """Sets the input coupling of the module

            Args:
                coupling (str):
                    The new input coupling ('AC' or 'DC')
        """

        self.device.command(f'SENSe{self.module_number}:COUPling {coupling}')

    def use_ac_coupling(self):
        """Sets the input coupling of the module to 'AC'"""

        self.set_coupling('AC')

    def use_dc_coupling(self):
        """Sets the input coupling of the module to 'DC'"""

        self.set_coupling('DC')

    def get_input_configuration(self):
        """Returns the input configuration of the module. 'AB', 'A', or 'GROUND'."""
        return self.device.query(f'SENSe{self.module_number}:CONFiguration?')

    def set_input_configuration(self, input_configuration):
        """Sets the input configuration of the module

            Args:
                input_configuration (str):
                    The new input configuration ('AB', 'A', or 'GROUND')
        """

        self.device.command(f'SENSe{self.module_number}:CONFiguration {input_configuration}')

    def get_bias_voltage(self):
        """Return the bias voltage applied on the amplifier input in Volts"""

        return float(self.device.query(f'SENSe{self.module_number}:BIAS:VOLTage:DC?'))

    def set_bias_voltage(self, bias_voltage):
        """Sets the bias voltage applied on the amplifier input

            Args:
                bias_voltage (float):
                    The new bias voltage in Volts
        """

        self.device.command(f'SENSe{self.module_number}:BIAS:VOLTage:DC {str(bias_voltage)}')

    def get_filter_state(self):
        """Returns whether the hardware filter is engaged"""

        return bool(int(self.device.query(f'SENSe{self.module_number}:FILTer:STATe?')))

    def get_lowpass_corner_frequency(self):
        """Returns the low pass filter cuttoff frequency. 'NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', 'F3000', or 'F10000'."""

        return self.device.query(f'SENSe{self.module_number}:FILTer:LPASs:FREQuency?')

    def get_lowpass_rolloff(self):
        """Returns the low pass filter roll-off. 'R6' or 'R12'."""

        return self.device.query(f'SENSe{self.module_number}:FILTer:LPASs:ATTenuation?')

    def get_highpass_corner_frequency(self):
        """Returns the high pass filter cuttoff frequency. 'NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', or 'F3000'."""

        return self.device.query(f'SENSe{self.module_number}:FILTer:HPASs:FREQuency?')

    def get_highpass_rolloff(self):
        """Returns the high pass filter roll-off. 'R6' or 'R12'."""

        return self.device.query(f'SENSe{self.module_number}:FILTer:HPASs:ATTenuation?')

    def get_gain_allocation_strategy(self):
        """Returns the gain allocation strategy used for the hardware filter. 'NOISE', or 'RESERVE'."""

        return self.device.query(f'SENSe{self.module_number}:FILTer:OPTimization?')

    def set_gain_allocation_strategy(self, optimization_type):
        """Sets the gain allocation strategy used for the hardware filter

            Args:
                optimization_type (str):
                    The new optimization type ('NOISE', or 'RESERVE')
        """

        self.device.command(f'SENSe{self.module_number}:FILTer:OPTimization {optimization_type}')

    def configure_input_lowpass_filter(self, corner_frequency, rolloff='R12'):
        """Configure the input low pass filter

            Args:
                corner_frequency (str):
                    The low pass corner frequency ('NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', 'F3000', or 'F10000'). F10 = 10 Hz, etc.

                rolloff (str):
                    The low pass roll-off ('R6' or 'R12'). R6 = 6 dB/Octave, R12 = 12 dB/Octave.
        """

        self.device.command(f'SENSe{self.module_number}:FILTer:LPASs:FREQuency {corner_frequency}')
        self.device.command(f'SENSe{self.module_number}:FILTer:LPASs:ATTenuation {rolloff}')
        self.device.command(f'SENSe{self.module_number}:FILTer:STATe 1')

    def configure_input_highpass_filter(self, corner_frequency, rolloff='R12'):
        """Configure the input high pass filter

            Args:
                corner_frequency (str):
                    The high pass corner frequency ('NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', or 'F3000'). F10 = 10 Hz, etc.

                rolloff (str):
                    The high pass roll-off ('R6' or 'R12'). R6 = 6 dB/Octave, R12 = 12 dB/Octave.
        """

        self.device.command(f'SENSe{self.module_number}:FILTer:HPASs:FREQuency {corner_frequency}')
        self.device.command(f'SENSe{self.module_number}:FILTer:HPASs:ATTenuation {rolloff}')
        self.device.command(f'SENSe{self.module_number}:FILTer:STATe 1')

    def disable_input_filters(self):
        """Disables the hardware filters"""

        self.device.command(f'SENSe{self.module_number}:FILTer:STATe 0')

    def get_i_range(self):
        """Returns the current range in Amps"""

        return float(self.device.query(f'SENSe{self.module_number}:CURRent:RANGe?'))

    def get_i_autorange_status(self):
        """Returns whether autoranging is enabled for the module"""

        return bool(int(self.device.query(f'SENSe{self.module_number}:CURRent:RANGe:AUTO?')))

    def configure_i_range(self, autorange, max_level=None):
        """Configure current ranging for the module

            Args:
                autorange (bool):
                    True to enable real time range decisions by the module. False for manual ranging.

                max_level (float):
                    The largest current that needs to be measured by the module in Amps.
        """

        if autorange:
            if max_level is not None:
                raise ValueError('If autorange is selected, a manual range cannot be specified.')

            self.device.command(f'SENSe{self.module_number}:CURRent:RANGe:AUTO 1')
        else:
            if max_level is not None:
                self.device.command(f'SENSe{self.module_number}:CURRent:RANGe {str(max_level)}')

    def get_voltage_range(self):
        """Returns the voltage range in Volts"""

        return float(self.device.query(f'SENSe{self.module_number}:VOLTage:RANGe?'))

    def get_voltage_autorange_status(self):
        """Returns whether autoranging is enabled for the module"""

        return bool(int(self.device.query(f'SENSe{self.module_number}:VOLTage:RANGe:AUTO?')))

    def configure_voltage_range(self, autorange, max_level):
        """Configure voltage ranging for the module

            Args:
                autorange (bool):
                    True to enable real time range decisions by the module. False for manual ranging.

                max_level (float):
                    The largest voltage that needs to be measured by the module in Volts.
        """

        if autorange:
            if max_level is not None:
                raise ValueError('If autorange is selected, a manual range cannot be specified.')

            self.device.command(f'SENSe{self.module_number}:VOLTage:RANGe:AUTO 1')
        else:
            if max_level is not None:
                self.device.command(f'SENSe{self.module_number}:VOLTage:RANGe {str(max_level)}')

    def get_reference_source(self):
        """Returns the lock-in reference source. 'S1', 'S2', 'S3', 'RIN'."""

        return self.device.query(f'SENSe{self.module_number}:LIA:RSOurce?')

    def set_reference_source(self, reference_source):
        """Sets the lock-in reference source

            Args:
                reference_source (str):
                    The new reference source ('S1', 'S2', 'S3', 'RIN')
        """

        self.device.command(f'SENSe{self.module_number}:LIA:RSOurce {reference_source}')

    def get_reference_harmonic(self):
        """Returns the lock-in reference harmonic"""

        return int(self.device.query(f'SENSe{self.module_number}:LIA:DHARmonic?'))

    def set_reference_harmonic(self, harmonic):
        """Sets the lock-in reference harmonic

            Args:
                harmonic (int):
                    The new reference harmonic. 1 is the fundamental frequency, 2 is twice the fundamental frequency, etc.
        """

        self.device.command(f'SENSe{self.module_number}:LIA:DHARmonic {str(harmonic)}')

    def get_reference_phase_shift(self):
        """Returns the lock-in reference phase shift in degrees"""

        return float(self.device.query(f'SENSe{self.module_number}:LIA:DPHase?'))

    def set_reference_phase_shift(self, phase_shift):
        """Sets the lock-in reference phase shift

            Args:
                phase_shift (float):
                    The new reference phase shift in degrees
        """
        self.device.command(f'SENSe{self.module_number}:LIA:DPHase {str(phase_shift)}')

    def auto_phase(self):
        """Executes a one time adjustment of the reference phase shift such that the present phase measurement is zero."""

        self.device.command(f'SENSe{self.module_number}:LIA:DPHase:AUTO')

    def get_lock_in_time_constant(self):
        """Returns the lock-in time constant in seconds"""

        return float(self.device.query(f'SENSe{self.module_number}:LIA:TIMEconstant?'))

    def set_lock_in_time_constant(self, time_constant):
        """Sets the lock-in time constant

            Args:
                time_constant (float):
                    The new time constant in seconds
        """
        self.device.command(f'SENSe{self.module_number}:LIA:TIMEconstant {str(time_constant)}')

    def get_lock_in_settle_time(self, settle_percent=0.01):
        """Returns the lock-in settle time in seconds

            Args:
                settle_percent (float)
                    The desired percent signal has settled to in percent
                    A value of `0.1` is interpreted as 0.1 %
        """
        return float(self.device.query(f'SENSe{self.module_number}:LIA:STIMe? {str(settle_percent)}'))

    def get_lock_in_equivalent_noise_bandwidth(self):
        """Returns the equivalent noise bandwidth (ENBW) in Hz"""
        return float(self.device.query(f'SENSe{self.module_number}:LIA:ENBW?'))

    def get_lock_in_rolloff(self):
        """Returns the lock-in PSD output filter roll-off for the present module. 'R6', 'R12', 'R18' or 'R24'."""

        return self.device.query(f'SENSe{self.module_number}:LIA:ROLLoff?')

    def set_lock_in_rolloff(self, rolloff):
        """Sets the lock-in PSD output filter roll-off

            Args:
                rolloff (str):
                    The new PSD output filter roll-off ('R6', 'R12', 'R18' or 'R24')
        """

        self.device.command(f'SENSe{self.module_number}:LIA:ROLLoff {rolloff}')

    def get_lock_in_fir_state(self):
        """Returns the state of the lock-in PSD output FIR filter"""

        return bool(int(self.device.query(f'SENSe{self.module_number}:LIA:FIR:STATe?')))

    def set_lock_in_fir_state(self, state):
        """Sets the state of the lock-in PSD output FIR filter

            Args:
                state (bool):
                    The new state of the PSD output FIR filter
        """

        self.device.command(f'SENSe{self.module_number}:LIA:FIR:STATe {str(int(state))}')

    def enable_lock_in_fir(self):
        """Sets the state of the lock-in PSD output FIR filter to True."""

        self.set_lock_in_fir_state(True)

    def disable_lock_in_fir(self):
        """Sets the state of the lock-in PSD output FIR filter to False."""

        self.set_lock_in_fir_state(False)

    def get_lock_in_fir_cycles(self):
        """Returns the number of FIR cycles"""

        return int(self.device.query(f'SENSe{self.module_number}:LIA:FIR:CYCLes?'))

    def set_lock_in_fir_cycles(self, cycles):
        """Sets the number of FIR cycles

            Args:
                cycles (int):
                    The desired number of FIR cycles, between 1 and 100
        """

        self.device.commands(f'SENSe{self.module_number}:LIA:FIR:CYCLes {str(int(cycles))}')

    def setup_dc_measurement(self, nplc=1):
        """Setup the module for DC measurement

            Args:
                nplc (float):
                    The new number of power line cycles to average
        """

        self.set_mode('DC')
        self.set_averaging_time(nplc)

    def setup_ac_measurement(self, nplc=1):
        """Setup the module for DC measurement

            Args:
                nplc (float):
                    The new number of power line cycles to average
        """

        self.set_mode('AC')
        self.set_averaging_time(nplc)

    def setup_lock_in_measurement(self,
                                  reference_source,
                                  time_constant,
                                  rolloff='R24',
                                  reference_phase_shift=0.0,
                                  reference_harmonic=1,
                                  use_fir=True):
        """Setup the module for lock-in measurement

            Args:
                reference_source (str):
                    Lock-in reference source ('S1', 'S2', 'S3', 'RIN')

                time_constant (float):
                    Time constant in seconds

                rolloff (str):
                    Lock-in PSD output filter roll-off ('R6', 'R12', 'R18' or 'R12')

                reference_phase_shift (float):
                    Lock-in reference phase shift in degrees

                reference_harmonic (int):
                    Lock-in reference harmonic. 1 is the fundamental frequency, 2 is twice the fundamental frequency, etc.

                use_fir (bool):
                    Enable or disable the PSD output FIR filter
        """

        self.set_mode('LIA')
        self.set_reference_source(reference_source)
        self.set_lock_in_time_constant(time_constant)
        self.set_lock_in_rolloff(rolloff)
        self.set_reference_phase_shift(reference_phase_shift)
        self.set_reference_harmonic(reference_harmonic)
        self.set_lock_in_fir_state(use_fir)

    def get_multiple(self, *data_sources):
        """Gets a list of values corresponding to the input data sources for this module.

            Args:
                data_sources (str): Variable length list of DATASOURCE_MNEMONIC.

            Returns:
                Tuple of values corresponding to the given data sources for this module
        """

        elements = [(data_source, self.module_number) for data_source in data_sources]
        return self.device.get_multiple(*elements)

    def get_dc(self):
        """Returns the DC measurement in module units"""

        return float(self.device.query(f'READ:SENSe{self.module_number}:DC?'))

    def get_rms(self):
        """Returns the RMS measurement in module units"""

        return float(self.device.query(f'READ:SENSe{self.module_number}:RMS?'))

    def get_peak_to_peak(self):
        """Returns the peak to peak measurement in module units"""

        return float(self.device.query(f'READ:SENSe{self.module_number}:PTPeak?'))

    def get_positive_peak(self):
        """Returns the positive peak measurement in module units"""

        return float(self.device.query(f'READ:SENSe{self.module_number}:PPEak?'))

    def get_negative_peak(self):
        """Returns the negative peak measurement in module units"""

        return float(self.device.query(f'READ:SENSe{self.module_number}:NPEak?'))

    def get_lock_in_x(self):
        """Returns the present X measurement from the lock-in"""

        return float(self.device.query(f'FETCh:SENSe{self.module_number}:LIA:X?'))

    def get_lock_in_y(self):
        """Returns the present Y measurement from the lock-in"""

        return float(self.device.query(f'FETCh:SENSe{self.module_number}:LIA:Y?'))

    def get_lock_in_r(self):
        """Returns the present magnitude measurement from the lock-in"""

        return float(self.device.query(f'FETCh:SENSe{self.module_number}:LIA:R?'))

    def get_lock_in_theta(self):
        """Returns the present angle measurement from the lock-in"""

        return float(self.device.query(f'FETCh:SENSe{self.module_number}:LIA:THETa?'))

    def get_lock_in_frequency(self):
        """Returns the present detected frequency from the Phase Locked Loop (PLL)"""

        return float(self.device.query(f'FETCh:SENSe{self.module_number}:LIA:FREQuency?'))

    def get_pll_lock_status(self):
        """Returns the present lock status of the PLL. True if locked, False if unlocked."""

        return bool(int(self.device.query(f'FETCh:SENSe{self.module_number}:LIA:LOCK?')))

    def get_present_questionable_status(self):
        """Returns the names of the questionable status register bits and their values"""

        response = self.device.query(f'STATus:QUEStionable:SENSe{self.module_number}:CONDition?', check_errors=False)
        status_register = SSMSystemModuleQuestionableRegister.from_integer(response)

        return status_register

    def get_questionable_events(self):
        """Returns the names of questionable event status register bits that are currently high.
        The event register is latching and values are reset when queried."""

        response = self.device.query(f'STATus:QUEStionable:SENSe{self.module_number}:EVENt?', check_errors=False)
        status_register = SSMSystemModuleQuestionableRegister.from_integer(response)

        return status_register

    def get_questionable_event_enable_mask(self):
        """Returns the names of the questionable event enable register bits and their values.
        These values determine which questionable bits propagate to the questionable event register."""

        response = self.device.query(f'STATus:QUEStionable:SENSe{self.module_number}:ENABle?', check_errors=False)
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
        self.device.command(f'STATus:QUEStionable:SENSe{self.module_number}:ENABle {integer_representation}', check_errors=False)

    def get_present_operation_status(self):
        """Returns the names of the operation status register bits and their values"""

        response = self.device.query(f'STATus:OPERation:SENSe{self.module_number}:CONDition?', check_errors=False)
        status_register = SSMSystemMeasureModuleOperationRegister.from_integer(response)

        return status_register

    def get_operation_events(self):
        """Returns the names of operation event status register bits that are currently high.
        The event register is latching and values are reset when queried."""

        response = self.device.query(f'STATus:OPERation:SENSe{self.module_number}:EVENt?', check_errors=False)
        status_register = SSMSystemMeasureModuleOperationRegister.from_integer(response)

        return status_register

    def get_operation_event_enable_mask(self):
        """Returns the names of the operation event enable register bits and their values.
        These values determine which operation bits propagate to the operation event register."""

        response = self.device.query(f'STATus:OPERation:SENSe{self.module_number}:ENABle?', check_errors=False)
        status_register = SSMSystemMeasureModuleOperationRegister.from_integer(response)

        return status_register

    def set_operation_event_enable_mask(self, register_mask):
        """Configures the values of the operaiton event enable register bits.
        These values determine which operaiton bits propagate to the operaiton event register.

            Args:
                register_mask ([Instrument]OperationRegister):
                    An instrument specific OperationRegister class object with all bits configured true or false.
        """

        integer_representation = register_mask.to_integer()
        self.device.command(f'STATus:OPERation:SENSe{self.module_number}:ENABle {integer_representation}', check_errors=False)

    def get_identify_state(self):
        """Returns the identification state for the given pod."""
        response = bool(int(self.device.query(f'SENSe{self.module_number}:IDENtify?', check_errors=False)))
        return response

    def set_identify_state(self, state):
        """Returns the identification state for the given pod.

            Args:
                state (bool):
                    The desired state for the LED, 1 for identify, 0 for normal state
        """
        self.device.command(f'SENSe{self.module_number}:IDENtify {int(state)}', check_errors=False)

    def get_dark_mode_state(self):
        """Returns the dark mode state for the given pod"""
        response = self.device.query(f'SENSe{self.module_number}:DMODe?', cherk_errors=False)
        return response

    def set_dark_mode_state(self, state):
        """Configures the dark mode state for the given pod.

            Args:
                state (bool):
                    The desired operation for the LED, 1 for normal mode, 0 for dark mode
        """
        self.device.command(f'SENSe{self.module_number}:DMODe {state}', check_errors=False)

    def get_frequency_range_threshold(self):
        """Returns the frequency range threshold for the module. Frequency range threshold normalized to the -3 db
           point. For example, a value of 0.1 means 10 % of the -3 db point.
        """

        return float(self.device.query(f'SENSe{self.module_number}:FRTHreshold?'))

    def set_frequency_range_threshold(self, threshold):
        """Sets the frequency range threshold for the specified module.
        When the modules range is set to Auto, a range such that the frequency of the signal does not exceed the given
        percentage of the bandwidth of the range will be chosen.

        Args:
            threshold (float):
                Frequency range threshold normalized to the -3 db point with a valid range of 0.0 to 1.0.
                For example, a value of 0.1 means 10 % of the -3 db point.
        """

        self.device.command(f'SENSe{self.module_number}:FRTHreshold {float(threshold)}')
        
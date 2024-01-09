"""Implements functionality unique to the M81 Measure Modules."""

from datetime import datetime
from warnings import warn
from lakeshore.xip_instrument import RegisterBase
from lakeshore.ssm_base_module import SSMSystemModuleQuestionableRegister, BaseModule
from lakeshore.ssm_system_enums import SSMSystemEnums


class SSMSystemMeasureModuleOperationRegister(RegisterBase):
    """Class object representing the operation status register of a measure module."""

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


# pylint: disable=R0904
class MeasureModule(BaseModule):
    """Class for interaction with a specific measure channel of the M81 instrument."""

    def get_name(self):
        """Returns the user-settable name of the module."""

        return self.device.query(f'SENSe{self.module_number}:NAME?').strip('\"')

    def set_name(self, new_name):
        """Set the name of the module."""

        self.device.command(f'SENSe{self.module_number}:NAME "{new_name}"')

    def get_notes(self):
        """Returns the user-settable notes of the module."""

        return self.device.query(f'SENSe{self.module_number}:NOTes?').strip('\"')

    def set_notes(self, new_note):
        """Set the notes of the module."""

        self.device.command(f'SENSe{self.module_number}:NOTes "{new_note}"')

    def get_model(self):
        """Returns the model of the module (i.e. VM-10)."""

        return self.device.query(f'SENSe{self.module_number}:MODel?').strip('\"')

    def get_serial(self):
        """Returns the serial number of the module (i.e. LSA1234)."""

        return self.device.query(f'SENSe{self.module_number}:SERial?').strip('\"')

    def get_hw_version(self):
        """Returns the hardware version of the module."""

        return int(self.device.query(f'SENSe{self.module_number}:HWVersion?'))

    def get_self_cal_status(self):
        """Returns the status of the last self calibration of the module."""

        return self.device.query(f'SENSe{self.module_number}:SCALibration:STATus?')

    def run_self_cal(self):
        """Run a self calibration for the module."""

        self.device.command(f'SENSe{self.module_number}:SCALibration:RUN')

    def reset_self_cal(self):
        """Restore factory self calibration for the module."""

        self.device.command(f'SENSe{self.module_number}:SCALibration:RESet')

    def get_averaging_time(self):
        """Returns the averaging time of the module in Power Line Cycles. Not relevant in lock-in mode."""

        return float(self.device.query(f'SENSe{self.module_number}:NPLCycles?'))

    def set_averaging_time(self, nplc):
        """Sets the averaging time of the module. Not relevant in lock-in mode.

            Args:
                nplc (float):
                    The new number of power line cycles to average.
        """

        self.device.command(f'SENSe{self.module_number}:NPLCycles {float(nplc)}')

    def get_mode(self):
        """Returns the measurement mode of the module. 'DC', 'AC', or 'LIA'."""

        return self.device.query(f'SENSe{self.module_number}:MODE?')

    def set_mode(self, mode):
        """Sets the measurement mode of the module.

            Args:
                mode (str):
                    The new measurement mode ('DC', 'AC', or 'LIA').
        """

        self.device.command(f'SENSe{self.module_number}:MODE {mode}')

    def get_coupling(self):
        """Return input coupling of the module. 'AC' or 'DC'."""

        return self.device.query(f'SENSe{self.module_number}:COUPling?')

    def set_coupling(self, coupling):
        """Sets the input coupling of the module.

            Args:
                coupling (str):
                    The new input coupling ('AC' or 'DC').
        """

        self.device.command(f'SENSe{self.module_number}:COUPling {coupling}')

    def use_ac_coupling(self):
        """Sets the input coupling of the module to 'AC'."""

        self.set_coupling('AC')

    def use_dc_coupling(self):
        """Sets the input coupling of the module to 'DC'."""

        self.set_coupling('DC')

    def get_input_configuration(self):
        """Returns the input configuration of the module. 'AB', 'A', or 'GROUND'."""
        return self.device.query(f'SENSe{self.module_number}:CONFiguration?')

    def set_input_configuration(self, input_configuration):
        """Sets the input configuration of the module.

            Args:
                input_configuration (str):
                    The new input configuration ('AB', 'A', or 'GROUND').
        """

        self.device.command(f'SENSe{self.module_number}:CONFiguration {input_configuration}')

    def enable_bias_voltage(self):
        """Enables the bias voltage applied to the amplifier."""

        self.device.command(f'SENSe{self.module_number}:BIAS:STATe 1')

    def disable_bias_voltage(self):
        """Disables the bias voltage applied to the amplifier."""

        self.device.command(f'SENSe{self.module_number}:BIAS:STATe 0')

    def get_bias_voltage_enabled(self):
        """Return whether the bias voltage is enabled."""

        return bool(int(self.device.query(f'SENSe{self.module_number}:BIAS:STATe?')))

    def get_bias_voltage(self):
        """Return the bias voltage applied on the amplifier input in Volts."""

        return float(self.device.query(f'SENSe{self.module_number}:BIAS:VOLTage:DC?'))

    def set_bias_voltage(self, bias_voltage):
        """Sets the bias voltage applied on the amplifier input.

            Args:
                bias_voltage (float):
                    The new bias voltage in Volts.
        """

        self.device.command(f'SENSe{self.module_number}:BIAS:VOLTage:DC {str(bias_voltage)}')

    def get_filter_state(self):
        """Returns whether the hardware filter is engaged."""

        return bool(int(self.device.query(f'SENSe{self.module_number}:FILTer:STATe?')))

    def get_lowpass_corner_frequency(self):
        """Returns the low pass filter cutoff frequency.

            'NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', 'F3000', or 'F10000'.
        """

        return self.device.query(f'SENSe{self.module_number}:FILTer:LPASs:FREQuency?')

    def get_lowpass_rolloff(self):
        """Returns the low pass filter roll-off.

            'R6' or 'R12'.
        """

        return self.device.query(f'SENSe{self.module_number}:FILTer:LPASs:ATTenuation?')

    def get_highpass_corner_frequency(self):
        """Returns the high pass filter cutoff frequency.

            'NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', or 'F3000'.
        """

        return self.device.query(f'SENSe{self.module_number}:FILTer:HPASs:FREQuency?')

    def get_highpass_rolloff(self):
        """Returns the high pass filter roll-off.

            'R6' or 'R12'.
        """

        return self.device.query(f'SENSe{self.module_number}:FILTer:HPASs:ATTenuation?')

    def get_gain_allocation_strategy(self):
        """Returns the gain allocation strategy used for the hardware filter.

            'NOISE', or 'RESERVE'.
        """

        return self.device.query(f'SENSe{self.module_number}:FILTer:OPTimization?')

    def set_gain_allocation_strategy(self, optimization_type):
        """Sets the gain allocation strategy used for the hardware filter.

            Args:
                optimization_type (str):
                    The new optimization type ('NOISE', or 'RESERVE').
        """

        self.device.command(f'SENSe{self.module_number}:FILTer:OPTimization {optimization_type}')

    def configure_input_lowpass_filter(self, corner_frequency, rolloff='R12'):
        """Configure the input low pass filter.

            Args:
                corner_frequency (str):
                    The low pass corner frequency.
                    ('NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', 'F3000', or 'F10000'). F10 = 10 Hz, etc.
                rolloff (str):
                    The low pass roll-off.
                    ('R6' or 'R12'). R6 = 6 dB/Octave, R12 = 12 dB/Octave.
        """

        self.device.command(f'SENSe{self.module_number}:FILTer:LPASs:FREQuency {corner_frequency}')
        self.device.command(f'SENSe{self.module_number}:FILTer:LPASs:ATTenuation {rolloff}')
        self.device.command(f'SENSe{self.module_number}:FILTer:STATe 1')

    def configure_input_highpass_filter(self, corner_frequency, rolloff='R12'):
        """Configure the input high pass filter.

            Args:
                corner_frequency (str):
                    The high pass corner frequency.
                    ('NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', or 'F3000'). F10 = 10 Hz, etc.
                rolloff (str):
                    The high pass roll-off ('R6' or 'R12'). R6 = 6 dB/Octave, R12 = 12 dB/Octave.
        """

        self.device.command(f'SENSe{self.module_number}:FILTer:HPASs:FREQuency {corner_frequency}')
        self.device.command(f'SENSe{self.module_number}:FILTer:HPASs:ATTenuation {rolloff}')
        self.device.command(f'SENSe{self.module_number}:FILTer:STATe 1')

    def disable_input_filters(self):
        """Disables the hardware filters."""

        self.device.command(f'SENSe{self.module_number}:FILTer:STATe 0')

    def get_current_range(self):
        """Returns the current range in Amps."""

        return float(self.device.query(f'SENSe{self.module_number}:CURRent:RANGe?'))

    def get_i_range(self):
        """
        Returns the current range in Amps

        .. deprecated:: 1.5.4
           Use get_current_range instead
        """

        warn('The get_i_range method is deprecated. Use get_current_range instead.', DeprecationWarning)
        return self.get_current_range()

    def get_current_autorange_status(self):
        """Returns whether auto-ranging is enabled for the module."""

        return bool(int(self.device.query(f'SENSe{self.module_number}:CURRent:RANGe:AUTO?')))

    def get_i_autorange_status(self):
        """
        Returns whether autoranging is enabled for the module

        .. deprecated:: 1.5.4
           Use get_current_autorange_status instead
        """

        warn('The get_i_autorange_status method is deprecated. Use get_current_autorange_status instead.', DeprecationWarning)
        return self.get_current_autorange_status()

    def configure_current_range(self, autorange, max_level=None):
        """Configure current ranging for the module.

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
            else:
                self.device.command(f'SENSe{self.module_number}:CURRent:RANGe:AUTO 0')

    def configure_i_range(self, autorange, max_level=None):
        """
        Configure current ranging for the module

        .. deprecated:: 1.5.4
           Use configure_current_range instead

            Args:
                autorange (bool):
                    True to enable real time range decisions by the module. False for manual ranging.
                max_level (float):
                    The largest current that needs to be measured by the module in Amps.
        """

        warn('The configure_i_range method is deprecated. Use configure_current_range instead.', DeprecationWarning)
        self.configure_current_range(autorange, max_level)

    def get_voltage_range(self):
        """Returns the voltage range in Volts."""

        return float(self.device.query(f'SENSe{self.module_number}:VOLTage:RANGe?'))

    def get_voltage_autorange_status(self):
        """Returns whether auto-ranging is enabled for the module."""

        return bool(int(self.device.query(f'SENSe{self.module_number}:VOLTage:RANGe:AUTO?')))

    def configure_voltage_range(self, autorange, max_level=None):
        """Configure voltage ranging for the module.

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
            else:
                self.device.command(f'SENSe{self.module_number}:VOLTage:RANGe:AUTO 0')

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
        """Returns the lock-in reference harmonic."""

        return int(self.device.query(f'SENSe{self.module_number}:LIA:DHARmonic?'))

    def set_reference_harmonic(self, harmonic):
        """Sets the lock-in reference harmonic.

            Args:
                harmonic (int):
                    The new reference harmonic.
                    1 is the fundamental frequency, 2 is twice the fundamental frequency, etc.
        """

        self.device.command(f'SENSe{self.module_number}:LIA:DHARmonic {str(harmonic)}')

    def get_reference_phase_shift(self):
        """Returns the lock-in reference phase shift in degrees."""

        return float(self.device.query(f'SENSe{self.module_number}:LIA:DPHase?'))

    def set_reference_phase_shift(self, phase_shift):
        """Sets the lock-in reference phase shift.

            Args:
                phase_shift (float):
                    The new reference phase shift in degrees.
        """
        self.device.command(f'SENSe{self.module_number}:LIA:DPHase {str(phase_shift)}')

    def auto_phase(self):
        """Executes a one time adjustment of the reference phase shift so that the present phase measurement is zero."""

        self.device.command(f'SENSe{self.module_number}:LIA:DPHase:AUTO')

    def get_lock_in_time_constant(self):
        """Returns the lock-in time constant in seconds."""

        return float(self.device.query(f'SENSe{self.module_number}:LIA:TIMEconstant?'))

    def set_lock_in_time_constant(self, time_constant):
        """Sets the lock-in time constant.

            Args:
                time_constant (float):
                    The new time constant in seconds.
        """
        self.device.command(f'SENSe{self.module_number}:LIA:TIMEconstant {str(time_constant)}')

    def get_lock_in_settle_time(self, settle_percent=0.01):
        """Returns the lock-in settle time in seconds.

            Args:
                settle_percent (float):
                    The desired percent signal has settled to in percent.
                    A value of `0.1` is interpreted as 0.1 %.
        """
        return float(self.device.query(f'SENSe{self.module_number}:LIA:STIMe? {str(settle_percent)}'))

    def get_lock_in_equivalent_noise_bandwidth(self):
        """Returns the equivalent noise bandwidth (ENBW) in Hz."""
        return float(self.device.query(f'SENSe{self.module_number}:LIA:ENBW?'))

    def get_lock_in_rolloff(self):
        """Returns the lock-in PSD output filter roll-off for the present module. 'R6', 'R12', 'R18' or 'R24'."""

        return self.device.query(f'SENSe{self.module_number}:LIA:ROLLoff?')

    def set_lock_in_rolloff(self, rolloff):
        """Sets the lock-in PSD output filter roll-off.

            Args:
                rolloff (str):
                    The new PSD output filter roll-off ('R6', 'R12', 'R18' or 'R24').
        """

        self.device.command(f'SENSe{self.module_number}:LIA:ROLLoff {rolloff}')

    def get_lock_in_iir_state(self):
        """Returns the state of the lock-in PSD output IIR filter."""

        return bool(int(self.device.query(f'SENSe{self.module_number}:LIA:IIR:STATe?')))

    def set_lock_in_iir_state(self, state):
        """Sets the state of the lock-in PSD output IIR filter.

            Args:
                state (bool):
                    The new state of the PSD output IIR filter.
        """

        self.device.command(f'SENSe{self.module_number}:LIA:IIR:STATe {str(int(state))}')

    def enable_lock_in_iir(self):
        """Sets the state of the lock-in PSD output IIR filter to True."""

        self.set_lock_in_iir_state(True)

    def disable_lock_in_iir(self):
        """Sets the state of the lock-in PSD output IIR filter to False."""

        self.set_lock_in_iir_state(False)

    def get_lock_in_fir_state(self):
        """Returns the state of the lock-in PSD output FIR filter."""

        return bool(int(self.device.query(f'SENSe{self.module_number}:LIA:FIR:STATe?')))

    def set_lock_in_fir_state(self, state):
        """Sets the state of the lock-in PSD output FIR filter.

            Args:
                state (bool):
                    The new state of the PSD output FIR filter.
        """

        self.device.command(f'SENSe{self.module_number}:LIA:FIR:STATe {str(int(state))}')

    def enable_lock_in_fir(self):
        """Sets the state of the lock-in PSD output FIR filter to True."""

        self.set_lock_in_fir_state(True)

    def disable_lock_in_fir(self):
        """Sets the state of the lock-in PSD output FIR filter to False."""

        self.set_lock_in_fir_state(False)

    def get_lock_in_fir_cycles(self):
        """Returns the number of FIR cycles."""

        return int(self.device.query(f'SENSe{self.module_number}:LIA:FIR:CYCLes?'))

    def set_lock_in_fir_cycles(self, cycles):
        """Sets the number of FIR cycles.

            Args:
                cycles (int):
                    The desired number of FIR cycles, between 1 and 100.
        """

        self.device.command(f'SENSe{self.module_number}:LIA:FIR:CYCLes {str(int(cycles))}')

    def setup_dc_measurement(self, nplc=1):
        """Set up the module for DC measurement.

            Args:
                nplc (float):
                    The new number of power line cycles to average.
        """

        self.set_mode('DC')
        self.set_averaging_time(nplc)

    def setup_ac_measurement(self, nplc=1):
        """Set up the module for DC measurement.

            Args:
                nplc (float):
                    The new number of power line cycles to average.
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
        """Set up the module for lock-in measurement.

            Args:
                reference_source (str):
                    Lock-in reference source ('S1', 'S2', 'S3', 'RIN').
                time_constant (float):
                    Time constant in seconds.
                rolloff (str):
                    Lock-in PSD output filter roll-off ('R6', 'R12', 'R18' or 'R12').
                reference_phase_shift (float):
                    Lock-in reference phase shift in degrees.
                reference_harmonic (int):
                    Lock-in reference harmonic. 1 is the fundamental frequency, 2 is twice the fundamental frequency,
                    etc.
                use_fir (bool):
                    Enable or disable the PSD output FIR filter.
        """

        self.set_mode('LIA')
        self.set_reference_source(reference_source)
        self.set_lock_in_time_constant(time_constant)
        self.set_lock_in_rolloff(rolloff)
        self.set_reference_phase_shift(reference_phase_shift)
        self.set_reference_harmonic(reference_harmonic)
        self.set_lock_in_fir_state(use_fir)

    def zero_relative_baseline(self):
        """Sets the present measurement as the baseline value for calculating relative readings."""

        self.device.command(f'SENSe{self.module_number}:RELative:ZERO')

    def set_relative_baseline(self, baseline):
        """Sets the relative baseline."""

        self.device.command(f'SENSe{self.module_number}:RELative:BASEline {str(baseline)}')

    def get_relative_baseline(self):
        """Returns the relative baseline."""

        return float(self.device.query(f'SENSe{self.module_number}:RELative:BASEline?'))

    def get_multiple(self, *data_sources):
        """This function is deprecated. Use fetch_multiple() instead."""

        return self.fetch_multiple(*data_sources)

    def get_dc(self):
        """Returns the DC measurement in module units."""

        return float(self.device.query(f'READ:SENSe{self.module_number}:DC?'))

    def get_dc_relative(self):
        """Returns the relative DC measurement in module units."""

        return float(self.device.query(f'READ:SENSe{self.module_number}:DC:RELative?'))

    def get_dc_minimum(self):
        """Returns the minimum DC indication in module units."""

        return float(self.device.query(f'STATistic:MINimum:SENSe{self.module_number}:DC?'))

    def get_dc_maximum(self):
        """Returns the maximum DC indication in module units."""

        return float(self.device.query(f'STATistic:MAXimum:SENSe{self.module_number}:DC?'))

    def get_rms(self):
        """Returns the RMS measurement in module units."""

        return float(self.device.query(f'READ:SENSe{self.module_number}:RMS?'))

    def get_rms_relative(self):
        """Returns the relative RMS measurement in module units."""

        return float(self.device.query(f'READ:SENSe{self.module_number}:RMS:RELative?'))

    def get_rms_minimum(self):
        """Returns the minimum RMS indication in module units."""

        return float(self.device.query(f'STATistic:MINimum:SENSe{self.module_number}:RMS?'))

    def get_rms_maximum(self):
        """Returns the maximum RMS indication in module units."""

        return float(self.device.query(f'STATistic:MAXimum:SENSe{self.module_number}:RMS?'))

    def get_peak_to_peak(self):
        """Returns the peak to peak measurement in module units."""

        return float(self.device.query(f'READ:SENSe{self.module_number}:PTPeak?'))

    def get_peak_to_peak_minimum(self):
        """Returns the minimum peak to peak indication in module units."""

        return float(self.device.query(f'STATistic:MINimum:SENSe{self.module_number}:PTPeak?'))

    def get_peak_to_peak_maximum(self):
        """Returns the maximum peak to peak indication in module units."""

        return float(self.device.query(f'STATistic:MAXimum:SENSe{self.module_number}:PTPeak?'))

    def get_positive_peak(self):
        """Returns the positive peak measurement in module units."""

        return float(self.device.query(f'READ:SENSe{self.module_number}:PPEak?'))

    def get_positive_peak_minimum(self):
        """Returns the minimum positive peak indication in module units."""

        return float(self.device.query(f'STATistic:MINimum:SENSe{self.module_number}:PPEak?'))

    def get_positive_peak_maximum(self):
        """Returns the maximum positive peak indication in module units."""

        return float(self.device.query(f'STATistic:MAXimum:SENSe{self.module_number}:PPEak?'))

    def get_negative_peak(self):
        """Returns the negative peak measurement in module units."""

        return float(self.device.query(f'READ:SENSe{self.module_number}:NPEak?'))

    def get_negative_peak_minimum(self):
        """Returns the minimum negative peak indication in module units."""

        return float(self.device.query(f'STATistic:MINimum:SENSe{self.module_number}:NPEak?'))

    def get_negative_peak_maximum(self):
        """Returns the maximum negative peak indication in module units."""

        return float(self.device.query(f'STATistic:MAXimum:SENSe{self.module_number}:NPEak?'))

    def get_lock_in_x(self):
        """Returns the present X measurement from the lock-in."""

        return float(self.device.query(f'FETCh:SENSe{self.module_number}:LIA:X?'))

    def get_lock_in_x_minimum(self):
        """Returns the minimum X indication from the lock in."""

        return float(self.device.query(f'STATistic:MINimum:SENSe{self.module_number}:LIA:X?'))

    def get_lock_in_x_maximum(self):
        """Returns the maximum X indication from the lock in."""

        return float(self.device.query(f'STATistic:MAXimum:SENSe{self.module_number}:LIA:X?'))

    def get_lock_in_y(self):
        """Returns the present Y measurement from the lock-in."""

        return float(self.device.query(f'FETCh:SENSe{self.module_number}:LIA:Y?'))

    def get_lock_in_y_minimum(self):
        """Returns the minimum Y indication from the lock in."""

        return float(self.device.query(f'STATistic:MINimum:SENSe{self.module_number}:LIA:Y?'))

    def get_lock_in_y_maximum(self):
        """Returns the maximum Y indication from the lock in."""

        return float(self.device.query(f'STATistic:MAXimum:SENSe{self.module_number}:LIA:Y?'))

    def get_lock_in_r(self):
        """Returns the present magnitude measurement from the lock-in."""

        return float(self.device.query(f'FETCh:SENSe{self.module_number}:LIA:R?'))

    def get_lock_in_r_minimum(self):
        """Returns the minimum magnitude indication from the lock in."""

        return float(self.device.query(f'STATistic:MINimum:SENSe{self.module_number}:LIA:R?'))

    def get_lock_in_r_maximum(self):
        """Returns the maximum magnitude indication from the lock in."""

        return float(self.device.query(f'STATistic:MAXimum:SENSe{self.module_number}:LIA:R?'))

    def get_lock_in_theta(self):
        """Returns the present angle measurement from the lock-in."""

        return float(self.device.query(f'FETCh:SENSe{self.module_number}:LIA:THETa?'))

    def get_lock_in_theta_minimum(self):
        """Returns the minimum angle indication from the lock in."""

        return float(self.device.query(f'STATistic:MINimum:SENSe{self.module_number}:LIA:THETa?'))

    def get_lock_in_theta_maximum(self):
        """Returns the maximum angle indication from the lock in."""

        return float(self.device.query(f'STATistic:MAXimum:SENSe{self.module_number}:LIA:THETa?'))

    def get_lock_in_frequency(self):
        """Returns the present detected frequency from the Phase Locked Loop (PLL)."""

        return float(self.device.query(f'FETCh:SENSe{self.module_number}:LIA:FREQuency?'))

    def get_pll_lock_status(self):
        """Returns the present lock status of the PLL. True if locked, False if unlocked."""

        return bool(int(self.device.query(f'FETCh:SENSe{self.module_number}:LIA:LOCK?')))

    def get_present_questionable_status(self):
        """Returns the names of the questionable status register bits and their values."""

        response = self.device.query(f'STATus:QUEStionable:SENSe{self.module_number}:CONDition?', check_errors=False)
        status_register = SSMSystemModuleQuestionableRegister.from_integer(response)

        return status_register

    def get_questionable_events(self):
        """Returns the names of questionable event status register bits that are currently high.

            The event register is latching and values are reset when queried.
        """

        response = self.device.query(f'STATus:QUEStionable:SENSe{self.module_number}:EVENt?', check_errors=False)
        status_register = SSMSystemModuleQuestionableRegister.from_integer(response)

        return status_register

    def get_questionable_event_enable_mask(self):
        """Returns the names of the questionable event enable register bits and their values.

            These values determine which questionable bits propagate to the questionable event register.
        """

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
        """Returns the names of the operation status register bits and their values."""

        response = self.device.query(f'STATus:OPERation:SENSe{self.module_number}:CONDition?', check_errors=False)
        status_register = SSMSystemMeasureModuleOperationRegister.from_integer(response)

        return status_register

    def get_overload_status(self):
        """Returns whether the module is presently in overload or not"""

        response = self.device.query(f'STATus:OPERation:SENSe{self.module_number}:CONDition?', check_errors=False)
        status_register = SSMSystemMeasureModuleOperationRegister.from_integer(response)

        return status_register.overload

    def get_settling_status(self):
        """Returns whether the module is presently settling or not"""

        response = self.device.query(f'STATus:OPERation:SENSe{self.module_number}:CONDition?', check_errors=False)
        status_register = SSMSystemMeasureModuleOperationRegister.from_integer(response)

        return status_register.settling

    def get_unlocked_status(self):
        """Returns whether the module is presently unlocked or not"""

        response = self.device.query(f'STATus:OPERation:SENSe{self.module_number}:CONDition?', check_errors=False)
        status_register = SSMSystemMeasureModuleOperationRegister.from_integer(response)

        return status_register.unlocked

    def get_operation_events(self):
        """Returns the names of operation event status register bits that are currently high.

            The event register is latching and values are reset when queried.
        """

        response = self.device.query(f'STATus:OPERation:SENSe{self.module_number}:EVENt?', check_errors=False)
        status_register = SSMSystemMeasureModuleOperationRegister.from_integer(response)

        return status_register

    def get_operation_event_enable_mask(self):
        """Returns the names of the operation event enable register bits and their values.

            These values determine which operation bits propagate to the operation event register.
        """

        response = self.device.query(f'STATus:OPERation:SENSe{self.module_number}:ENABle?', check_errors=False)
        status_register = SSMSystemMeasureModuleOperationRegister.from_integer(response)

        return status_register

    def set_operation_event_enable_mask(self, register_mask):
        """Configures the values of the operation event enable register bits.

            These values determine which operation bits propagate to the operation event register.

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
        """Sets the identification state for the given pod.

            Args:
                state (bool):
                    The desired state for the LED, 1 for identify, 0 for normal state.
        """

        self.device.command(f'SENSe{self.module_number}:IDENtify {int(state)}', check_errors=False)

    def get_dark_mode_state(self):
        """Returns the dark mode state for the given pod."""

        response = self.device.query(f'SENSe{self.module_number}:DMODe?', cherk_errors=False)
        return response

    def set_dark_mode_state(self, state):
        """Configures the dark mode state for the given pod.

            Args:
                state (bool):
                    The desired operation for the LED, 1 for normal mode, 0 for dark mode.
        """

        self.device.command(f'SENSe{self.module_number}:DMODe {state}', check_errors=False)

    def get_frequency_range_threshold(self):
        """Returns the frequency range threshold for the module.

            Frequency range threshold normalized to the -3 db point. For example, a value of 0.1 means 10 % of the
            -3 db point.
        """

        return float(self.device.query(f'SENSe{self.module_number}:FRTHreshold?'))

    def set_frequency_range_threshold(self, threshold):
        """Sets the frequency range threshold for the specified module.

            When the modules range is set to Auto, a range such that the frequency of the signal does not exceed the
            given percentage of the bandwidth of the range will be chosen.

        Args:
            threshold (float):
                Frequency range threshold normalized to the -3 db point with a valid range of 0.0 to 1.0.
                For example, a value of 0.1 means 10 % of the -3 db point.
        """

        self.device.command(f'SENSe{self.module_number}:FRTHreshold {float(threshold)}')

    def get_digital_high_pass_filter_state(self):
        """Returns the state of the digital high pass filter for lock-in mode."""
        return bool(int(self.device.query(f'SENSe{self.module_number}:DIGital:FILTer:HPASs:STATe?')))

    def set_digital_high_pass_filter_state(self, state):
        """Sets the state of the digital high pass filter for lock-in mode.

            Args:
                state (bool):
                    The desired state fot he digital lock-in high pass filter. 1 for enabled, 0 for disabled.
        """
        self.device.command(f'SENSe{self.module_number}:DIGital:FILTer:HPASs:STATE {int(state)}')

    def get_resistance(self):
        """Returns the present resistance measurement in Ohms. A valid source must be configured.

        Returns:
            float: Present resistance measurement in Ohms.
        """

        return float(self.device.query(f'CALCulate:SENSe{self.module_number}:RESistance?'))

    def set_resistance_source(self, source_module):
        """Configures the resistance feature to use a specified source module to calculate resistance.

        Args:
            source_module (SourceModule): The channel used for calculating resistance.
        """

        if isinstance(source_module, SSMSystemEnums.ReferenceModule):
            source = source_module.name
        else:
            source = source_module

        self.device.command(f'CALCulate:SENSe{self.module_number}:RESistance:SOURce {source}')

    def get_resistance_source(self):
        """Returns the present source module being used to calculate resistance.

                Returns:
                    SourceModule: The channel used for calculating resistance.
                """
        return SSMSystemEnums.ReferenceModule(self.device.query(f'CALCulate:SENSe{self.module_number}:RESistance:SOURce?'))

    def set_resistance_excitation_type(self, excitation_type):
        """Sets the present resistance excitation type of the specified module.

            For "DC", the measure mode is DC and source shape is DC.
            For "AC", the measure mode is Lock-in and source shape is Sine.

        Args:
            excitation_type (ResistanceExcitationType): The desired resistance excitation type.
        """

        if isinstance(excitation_type, SSMSystemEnums.ResistanceExcitationType):
            excitation = excitation_type.name
        else:
            excitation = excitation_type

        self.device.command(f"CALCulate:SENSe{self.module_number}:RESistance:ETYPe {excitation}")

    def get_resistance_excitation_type(self):
        """Returns the present resistance excitation type of the specified module.

            This represents the combination of the specified measure module mode and the selected source module shape.
            For "DC", the measure mode is DC and source shape is DC.
            For "AC", the measure mode is Lock-in and source shape is Sine.

        Returns:
            ResistanceExcitationType: The resistance excitation type.
        """

        return SSMSystemEnums.ResistanceExcitationType(self.device.query(
            f"CALCulate:SENSe{self.module_number}:RESistance:ETYPe?"))

    def set_resistance_mode(self, resistance_mode):
        """Sets the resistance optimization mode of the specified module.

        Args:
            resistance_mode (ResistanceMode): The desired resistance optimization mode.
        """
        if isinstance(resistance_mode, SSMSystemEnums.ResistanceExcitationType):
            mode = resistance_mode.name
        else:
            mode = resistance_mode

        self.device.command(f"CALCulate:SENSe{self.module_number}:RESistance:MODE {mode}")

    def get_resistance_mode(self):
        """Returns the preset resistance optimization mode of the specified module.

        Returns:
            ResistanceMode: The present resistance optimization mode. "NOISe" or "POWer".
        """

        return SSMSystemEnums.ResistanceMode(self.device.query(f"CALCulate:SENSe{self.module_number}:RESistance:MODE?"))

    def set_resistance_range(self, resistance_range):
        """Sets the resistance range of the specified module.

        Args:
            resistance_range (float): The desired resistance range in Ohms.
        """

        self.device.command(f"CALCulate:SENSe{self.module_number}:RESistance:RANGe {resistance_range}")

    def get_resistance_range(self):
        """Returns the present resistance range of the specified module.
        
        Returns:
            float: The resistance range in Ohms.
        """

        return float(self.device.query(f"CALCulate:SENSe{self.module_number}:RESistance:RANGe?"))

    def set_resistance_optimization_state(self, optimization_state):
        """Sets the state of resistance optimization on the specified module

        Args:
            optimization_state (bool): The desired state of resistance optimization. True if optimizing for resistance,
                else False.
        """

        self.device.command(f"CALCulate:SENSe{self.module_number}:RESistance:OPTimize {int(optimization_state)}")

    def get_resistance_optimization_state(self):
        """Returns the present state of optimization on the specified module.

            When optimization is enabled, the instrument will set other settings based on the selected resistance
            range and mode settings.

        Returns:
            bool: The state of resistance optimization. True if optimizing for resistance, else False.
        """

        return bool(self.device.query(f"CALCulate:SENSe{self.module_number}:RESistance:OPTimize?"))

    def set_resistance_observation_time_state(self, state):
        """Sets the state of the observation time on the specified module.

        Args:
            state (bool): The state of resistance observation time.
        """
        self.device.command(f"CALCulate:SENSe{self.module_number}:RESistance:OTIME:STATe {int(state)}")

    def get_resistance_observation_time_state(self):
        """Gets the present state of the observation time on the specified module.

        Returns:
            bool: The state of resistance observation time.
        """

        return bool(int(self.device.query(f"CALCulate:SENSe{self.module_number}:RESistance:OTIMe:STATe?")))

    def set_resistance_observation_time_requested(self, requested_time):
        """Sets the requested observation time on the specified module.

        Args:
            requested_time (float): The requested observation time.
        """

        self.device.command(f"CALCulate:SENSe{self.module_number}:RESistance:OTIMe:REQuested {requested_time}")

    def get_resistance_observation_time_requested(self):
        """Gets the present requested observation time on the specified module.

        Returns:
            float: The requested observation time.
        """

        return float(self.device.query(f"CALCulate:SENSe{self.module_number}:RESistance:OTIMe:REQuested?"))

    def get_resistance_observation_time_actual(self):
        """Gets the present actual observation time for the resistance calculation.

            This is a best-fit calculation based on the requested observation time and reference frequency.

        Returns:
            float: The actual observation time.
        """

        return float(self.device.query(f"CALCulate:SENSe{self.module_number}:RESistance:OTIMe:ACTual?"))

    def get_resistance_observation_time_enbw(self):
        """Gets the present equivalent noise bandwidth (ENBW) for the actual resistance observation time.

        Returns:
            float: The calculated equivalent noise bandwidth.
        """

        return float(self.device.query(f"CALCulate:SENSe{self.module_number}:RESistance:OTIMe:ENBandwidth?"))

    def reset_settings(self):
        """Resets the settings for the specified module to their power on defaults."""

        self.device.command(f'SENSe{self.module_number}:PRESet')

    def unload(self):
        """Unloads the specified module."""

        self.device.command(f'SENSe{self.module_number}:UNLoad')

    def get_load_state(self):
        """Returns the loaded state for the specified module."""

        response = bool(int(self.device.query(f'SENSe{self.module_number}:LOAD?')))
        return response

    def fetch_multiple(self, *data_sources):
        """Returns a list of the latest values corresponding to the input data sources for this module quickly

            Args:
                data_sources (SSMSystemDataSourceMnemonic or str):
                    Variable length list of data sources.

            Returns:
                Tuple of values corresponding to the given data sources for this module.
        """

        elements = [(data_source, self.module_number) for data_source in data_sources]
        return self.device.fetch_multiple(*elements)

    def read_multiple(self, *data_sources):
        """Returns new values after measurement based on present input data source.

            Initiates measurement of new values corresponding to the input data sources for this module and returns them
            after the measurement is complete.

            Args:
                data_sources (SSMSystemReadDataSourceMnemonic or str):
                    Variable length list of data sources.

            Returns:
                Tuple of values corresponding to the given data sources for this module.
        """

        elements = [(data_source, self.module_number) for data_source in data_sources]
        return self.device.read_multiple(*elements)

    def get_self_cal_datetime(self):
        """Returns the self calibration date and time for the specified module."""

        response = self.device.query(f'SENSe{self.module_number}:SCALibration:DATE?').split(',')
        return datetime(int(response[0]), int(response[1]), int(response[2]), int(response[3]),int(response[4]), int(response[5]))

    def get_self_cal_temperature(self):
        """Returns the self calibration temperature for the specified module."""

        return float(self.device.query(f'SENSe{self.module_number}:SCALibration:TEMP?'))

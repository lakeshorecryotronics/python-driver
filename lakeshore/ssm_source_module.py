"""Implements functionality unique to the M81 Source Modules."""

import math
from datetime import datetime
from warnings import warn

from lakeshore.xip_instrument import RegisterBase
from lakeshore.ssm_base_module import SSMSystemModuleQuestionableRegister, BaseModule
from lakeshore.ssm_system_enums import SSMSystemEnums
from lakeshore.requires_firmware_version import requires_firmware_version


class SSMSystemSourceModuleOperationRegister(RegisterBase):
    """Class object representing the operation status register of a source module."""

    bit_names = [
        "v_limit",
        "i_limit",
        "sweeping"
    ]

    def __init__(
            self,
            v_limit,
            i_limit,
            sweeping):
        self.v_limit = v_limit
        self.i_limit = i_limit
        self.sweeping = sweeping


# pylint: disable=R0904
class SourceModule(BaseModule):
    """Class for interaction with a specific source channel of the M81 instrument."""

    def get_multiple(self, *data_sources):
        r"""This function is deprecated. Use fetch_multiple() instead."""

        return self.fetch_multiple(*data_sources)

    def fetch_multiple(self, *data_sources):
        r"""Gets a list of the latest values corresponding to the input data sources for this module.

        Args:
            data_sources (SSMSystemDataSourceMnemonic or str):
                Variable length list of data sources.

        Returns:
            Tuple of values corresponding to the given data sources for this module.
        """

        elements = [(data_source, self.module_number) for data_source in data_sources]
        return self.device.fetch_multiple(*elements)

    def get_name(self):
        """Returns the user-settable name of the module."""

        return self.device.query(f'SOURce{self.module_number}:NAME?').strip('\"')

    def set_name(self, new_name):
        """Set the name of the module."""

        self.device.command(f'SOURce{self.module_number}:NAME "{new_name}"')

    def get_notes(self):
        """Returns the user-settable notes of the module."""

        return self.device.query(f'SOURce{self.module_number}:NOTes?').strip('\"')

    def set_notes(self, new_note):
        """Set the notes of the module."""

        self.device.command(f'SOURce{self.module_number}:NOTes "{new_note}"')

    def get_model(self):
        """Returns the model of the module (i.e. BCS-10)."""

        return self.device.query(f'SOURce{self.module_number}:MODel?').strip('\"')

    def get_serial(self):
        """Returns the serial number of the module (i.e. LSA1234)."""

        return self.device.query(f'SOURce{self.module_number}:SERial?').strip('\"')

    def get_hw_version(self):
        """Returns the hardware version of the module."""

        return int(self.device.query(f'SOURce{self.module_number}:HWVersion?'))

    def get_self_cal_status(self):
        """Returns the status of the last self calibration of the module."""

        return self.device.query(f'SOURce{self.module_number}:SCALibration:STATus?')

    def run_self_cal(self):
        """Run a self calibration for the module."""

        self.device.command(f'SOURce{self.module_number}:SCALibration:RUN')

    def reset_self_cal(self):
        """Restore factory self calibration for the module."""

        self.device.command(f'SOURce{self.module_number}:SCALibration:RESet')

    def get_enable_state(self):
        """Returns the output state of the module."""

        return bool(int(self.device.query(f'SOURce{self.module_number}:STATe?')))

    def set_enable_state(self, state):
        """Sets the enable state of the module.

            Args:
                state (bool):
                    The new output state.
        """

        self.device.command(f'SOURce{self.module_number}:STATe {str(int(state))}')

    def enable(self):
        """Sets the enable state of the module to True."""

        self.set_enable_state(True)

    def disable(self):
        """Sets the enable state of the module to False."""

        self.set_enable_state(False)

    def get_source_function(self):
        """Returns the excitation function of the module. 'CURRENT' or 'VOLTAGE'."""

        return self.device.ExcitationType(self.device.query(f'SOURce{self.module_number}:FUNCtion:MODE?'))

    def set_source_function(self, excitation_mode):
        """Sets the excitation function of the module.

            Args:
                excitation_mode (SSMSystem.ExcitationType):
                    The new excitation mode ('CURRENT' or 'VOLTAGE').
        """

        if isinstance(excitation_mode, self.device.ExcitationType):
            mode = excitation_mode.name
        else:
            mode = excitation_mode

        self.device.command(f'SOURce{self.module_number}:FUNCtion:MODE {mode}')

    def go_to_current_mode(self):
        """Sets the excitation mode of the module to 'CURRENT'."""

        self.set_source_function(self.device.ExcitationType.CURRENT)

    def go_to_voltage_mode(self):
        """Sets the excitation mode of the module to 'VOLTAGE'."""

        self.set_source_function(self.device.ExcitationType.VOLTAGE)

    def get_shape(self):
        """Returns the signal shape of the module. 'DC' or 'SINUSOID'."""

        return self.device.query(f'SOURce{self.module_number}:FUNCtion:SHAPe?')

    def set_shape(self, shape):
        """Sets the signal shape of the module.

            Args:
                shape (str):
                    The new signal shape ('DC', 'SINUSOID', 'TRIANGLE', 'SQUARE').
        """

        self.device.command(f'SOURce{self.module_number}:FUNCtion:SHAPe {shape}')

    def get_frequency(self):
        """Returns the excitation frequency of the module."""

        return float(self.device.query(f'SOURce{self.module_number}:FREQuency?'))

    def set_frequency(self, frequency):
        """Sets the excitation frequency of the module.

            Args:
                frequency (float):
                    The new excitation frequency.
        """
        self.device.command(f'SOURce{self.module_number}:FREQuency {str(frequency)}')

    def get_sync_state(self):
        """Returns whether the source channel synchronization feature is engaged

            If true, this channel will ignore its own frequency, and instead track the frequency of the synchronization
            source.
            If false, this channel will generate its own frequency.
        """

        return bool(int(self.device.query(f'SOURce{self.module_number}:SYNChronize:STATe?')))

    def get_sync_source(self):
        """Returns the channel used for frequency synchronization."""

        return self.device.query(f'SOURce{self.module_number}:SYNChronize:SOURce?')

    def get_sync_phase_shift(self):
        """Returns the phase shift applied between the synchronization source and this channel."""

        return float(self.device.query(f'SOURce{self.module_number}:SYNChronize:PHASe?'))

    def configure_sync(self, source, phase_shift, enable_sync=True):
        """Configure the source channel synchronization feature.

            Args:
                source (str):
                    The channel used for synchronization ('S1', 'S2', 'S3', or 'RIN').
                    This module will follow the frequency set for the specified channel if sync is enabled.
                phase_shift (float):
                    The phase shift applied between the synchronization source and this channel in degrees.
                enable_sync (bool):
                    If true, this channel will ignore its own frequency, and instead track the frequency of the
                    synchronization source.
                    If false, this channel will generate its own frequency.
        """
        self.device.command(f'SOURce{self.module_number}:SYNChronize:SOURce {source}')
        self.device.command(f'SOURce{self.module_number}:SYNChronize:PHASe {str(phase_shift)}')
        self.device.command(f'SOURce{self.module_number}:SYNChronize:STATe {str(int(enable_sync))}')

    def get_duty(self):
        """Returns the duty cycle of the module."""

        return float(self.device.query(f'SOURce{self.module_number}:DCYCle?'))

    def set_duty(self, duty):
        """Sets the duty cycle of the module.

            Args:
                duty (float):
                    The new duty cycle.
        """

        self.device.command(f'SOURce{self.module_number}:DCYCle {str(duty)}')

    def get_coupling(self):
        """Returns the coupling type of the module. 'AC' or 'DC'."""

        return self.device.query(f'SOURce{self.module_number}:COUPling?')

    def set_coupling(self, coupling):
        """Sets the coupling of the module.

            Args:
                coupling (str):
                    The new coupling type ('AC', or 'DC').
        """
        self.device.command(f'SOURce{self.module_number}:COUPling {coupling}')

    def use_ac_coupling(self):
        """Sets the coupling type of the module to 'AC'."""

        self.set_coupling('AC')

    def use_dc_coupling(self):
        """Sets the coupling type of the module to 'DC'."""

        self.set_coupling('DC')

    def set_automatic_coupling(self, enable: bool):
        """Enable or disable automatic coupling for the module.

        Args:
            enable (bool): True to enable automatic coupling, False to disable.
        """
        self.device.command(f'SOURce{self.module_number}:COUPling:AUTO {int(enable)}')

    def get_automatic_coupling(self) -> bool:
        """Query the automatic coupling state of the module.

        Returns:
            bool: True if automatic coupling is enabled, False otherwise.
        """
        return bool(int(self.device.query(f'SOURce{self.module_number}:COUPling:AUTO?')))

    def get_guard_state(self):
        """Returns the guard state of the module."""

        return bool(int(self.device.query(f'SOURce{self.module_number}:GUARd?')))

    def set_guard_state(self, guard_state):
        """Sets the guard state of the module.

            Args:
                guard_state (bool):
                    The new guard state (True to enable guards, False to disable guards).
        """

        self.device.command(f'SOURce{self.module_number}:GUARd {str(int(guard_state))}')

    def enable_guards(self):
        """Sets the guard state of the module to True."""

        self.set_guard_state(True)

    def disable_guards(self):
        """Sets the guard state of the module to False."""

        self.set_guard_state(False)

    def get_cmf_source(self):
        """Returns the Common Mode Feedback (CMF) source. 'INTernal', or 'EXTernal'."""

        return self.device.query(f'SOURce{self.module_number}:CMF:SOURce?')

    def set_cmr_source(self, cmr_source):
        """
        This function is deprecated. Use set_cmf_source() instead.

        .. deprecated:: 1.9.0
            Use set_cmf_source instead.
        """

        warn("The set_cmr_source method is deprecated, use set_cmf_source instead", DeprecationWarning)

        self.set_cmf_source(cmr_source)

    def get_cmr_source(self):
        """
        This function is deprecated. Use get_cmf_source() instead.

        .. deprecated:: 1.9.0
            Use get_cmf_source instead.
        """

        warn("The get_cmr_source method is deprecated, use get_cmf_source instead", DeprecationWarning)

        return self.get_cmf_source()

    def set_cmf_source(self, cmf_source):
        """Sets the Common Mode Feedback (CMF) source.

            Args:
                cmf_source (str):
                    The new CMF source ('INTernal', or 'EXTernal').
        """

        self.device.command(f'SOURce{self.module_number}:CMF:SOURce {cmf_source}')

    def get_cmf_state(self):
        """Returns the Common Mode Feedback (CMF) state of the module."""

        return bool(int(self.device.query(f'SOURce{self.module_number}:CMF:STATe?')))

    def get_cmr_state(self):
        """
        This function is deprecated. Use get_cmf_state() instead.

        .. deprecated:: 1.9.0
            Use get_cmf_state instead.
        """

        warn("The get_cmr_state method is deprecated, use get_cmf_state instead", DeprecationWarning)

        return self.get_cmf_state()

    def set_cmf_state(self, cmf_state):
        """Sets the Common Mode Feedback (CMF) state of the module.

            Args:
                cmf_state (bool):
                    The new CMF state (True to enable CMF, False to disable CMF).
        """

        self.device.command(f'SOURce{self.module_number}:CMF:STATe {str(int(cmf_state))}')

    def set_cmr_state(self, cmr_state):
        """
        This function is deprecated. Use set_cmf_state() instead.

        .. deprecated:: 1.9.0
            Use set_cmf_state instead.
        """

        warn("The set_cmr_state method is deprecated, use set_cmf_state instead", DeprecationWarning)

        self.set_cmf_state(cmr_state)

    def enable_cmf(self):
        """Sets the CMF state of the module to True."""

        self.set_cmf_state(True)

    def enable_cmr(self):
        """
        This function is deprecated. Use enable_cmf() instead.

        .. deprecated:: 1.9.0
            Use enable_cmf instead.
        """

        warn("The enable_cmr method is deprecated, use enable_cmf instead", DeprecationWarning)

        self.set_cmr_state(True)

    def disable_cmf(self):
        """Sets the CMF state of the module to False."""

        self.set_cmf_state(False)

    def disable_cmr(self):
        """
        This function is deprecated. Use disable_cmf() instead.

        .. deprecated:: 1.9.0
            Use disable_cmf instead.
        """

        warn("The disable_cmr method is deprecated, use disable_cmf instead", DeprecationWarning)

        self.set_cmr_state(False)

    def configure_cmf(self, cmf_source, cmf_state=True):
        """Configure Common Mode Feedback (CMF).

            Args:
                cmf_source (str):
                    The new CMF source ('INTernal', or 'EXTernal').
                cmf_state (bool):
                    The new CMF state (True to enable CMF, False to disable CMF).
        """

        self.set_cmf_source(cmf_source)
        self.set_cmf_state(cmf_state)

    def configure_cmr(self, cmr_source, cmr_state=True):
        """
        This function is deprecated. Use configure_cmf() instead.

        .. deprecated:: 1.9.0
            Use configure_cmf instead.
        """

        warn("The configure_cmr method is deprecated, use configure_cmf instead", DeprecationWarning)

        self.set_cmr_source(cmr_source)
        self.set_cmr_state(cmr_state)

    def get_current_range(self):
        """Returns the present current range of the module in Amps."""

        return float(self.device.query(f'SOURce{self.module_number}:CURRent:RANGe?'))

    def get_i_range(self):
        """
        Returns the present current range of the module in Amps
        
        .. deprecated:: 1.5.4
           Use get_current_range instead.
        """

        warn("The get_i_range method is deprecated, use get_current_range instead", DeprecationWarning)
        return self.get_current_range()

    def get_current_ac_range(self):
        """Returns the present AC current range of the module in Amps."""

        return float(self.device.query(f'SOURce{self.module_number}:CURRent:RANGe:AC?'))

    def get_i_ac_range(self):
        """
        Returns the present AC current range of the module in Amps
        
        .. deprecated:: 1.5.4
           Use get_current_ac_range instead.
        """

        warn("The get_i_ac_range method is deprecated, use get_current_ac_range instead", DeprecationWarning)
        return self.get_current_ac_range()

    def get_current_dc_range(self):
        """Returns the present DC current range of the module in Amps."""

        return float(self.device.query(f'SOURce{self.module_number}:CURRent:RANGe:DC?'))

    def get_i_dc_range(self):
        """
        Returns the present DC current range of the module in Amps
        
        .. deprecated:: 1.5.4
           Use get_current_dc_range instead.
        """

        warn("The get_i_dc_range method is deprecated, use get_current_dc_range instead", DeprecationWarning)
        return self.get_current_dc_range()

    def get_current_autorange_status(self):
        """Returns whether automatic selection of the current range is enabled for this module."""

        return bool(int(self.device.query(f'SOURce{self.module_number}:CURRent:RANGe:AUTO?')))

    def get_i_autorange_status(self):
        """
        Returns whether automatic selection of the current range is enabled for this module
        
        .. deprecated:: 1.5.4
           Use get_current_autorange_status instead.
        """

        warn("The get_i_autorange_status method is deprecated, use get_current_autorange_status instead", DeprecationWarning)
        return self.get_current_autorange_status()

    def configure_current_range(self, autorange, max_level=None, max_ac_level=None, max_dc_level=None):
        """Sets up current ranging for this module.

            Args:
                autorange (bool):
                    True to enable automatic range selection. False for manual ranging.
                max_level (float):
                    The largest current that needs to be sourced.
                max_ac_level (float):
                    The largest AC current that needs to be sourced. Separate AC and DC ranges are only available on
                    some modules.
                max_dc_level (float):
                    The largest DC current that needs to be sourced. Separate AC and DC ranges are only available on
                    some modules.
        """

        if autorange:
            if max_level is not None or max_ac_level is not None or max_dc_level is not None:
                raise ValueError('If autorange is selected, a manual range cannot be specified.')

            self.device.command(f'SOURce{self.module_number}:CURRent:RANGe:AUTO 1')
        else:
            if max_level is not None:
                if max_ac_level is not None or max_dc_level is not None:
                    raise ValueError('Either a single range, or separate AC and DC ranges can be supplied, not both.')

                self.device.command(f'SOURce{self.module_number}:CURRent:RANGe {str(max_level)}')
            else:
                if max_ac_level is not None:
                    self.device.command(f'SOURce{self.module_number}:CURRent:RANGe:AC {str(max_ac_level)}')
                if max_dc_level is not None:
                    self.device.command(f'SOURce{self.module_number}:CURRent:RANGe:DC {str(max_dc_level)}')

    def configure_i_range(self, autorange, max_level=None, max_ac_level=None, max_dc_level=None):
        """
        Sets up current ranging for this module

            Args:
                autorange (bool):
                    True to enable automatic range selection. False for manual ranging.
                max_level (float):
                    The largest current that needs to be sourced.
                max_ac_level (float):
                    The largest AC current that needs to be sourced. Separate AC and DC ranges are only available on some modules.
                max_dc_level (float):
                    The largest DC current that needs to be sourced. Separate AC and DC ranges are only available on some modules.
        
        .. deprecated:: 1.5.4
           Use configure_current_range instead.
        """

        warn("The configure_i_range method is deprecated, use configure_current_range instead", DeprecationWarning)
        self.configure_current_range(autorange, max_level, max_ac_level, max_dc_level)

    def get_current_amplitude(self):
        """Returns the current amplitude for the module in Amps."""

        return float(self.device.query(f'SOURce{self.module_number}:CURRent:LEVel:AMPLitude?'))

    def get_i_amplitude(self):
        """
        Returns the current amplitude for the module in Amps
        
        .. deprecated:: 1.5.4
           Use get_current_amplitude instead.
        """

        warn("The get_i_amplitude method is deprecated, use get_current_amplitude instead", DeprecationWarning)
        return self.get_current_amplitude()

    def set_current_amplitude(self, amplitude):
        """Sets the current amplitude for the module.

            Args:
                amplitude (float):
                    The new current amplitude in Amps.
        """
        self.device.command(f'SOURce{self.module_number}:CURRent:LEVel:AMPLitude {str(amplitude)}')

    def set_i_amplitude(self, amplitude):
        """
        Sets the current amplitude for the module

            Args:
                amplitude (float):
                    The new current amplitude in Amps
        
        .. deprecated:: 1.5.4
           Use set_current_amplitude instead.
        """

        warn("The set_i_amplitude method is deprecated, use set_current_amplitude instead", DeprecationWarning)
        self.set_current_amplitude(amplitude)

    def get_current_offset(self):
        """Returns the current offset for the module in Amps."""

        return float(self.device.query(f'SOURce{self.module_number}:CURRent:LEVel:OFFSet?'))

    def get_i_offset(self):
        """
        Returns the current offset for the module in Amps
        
        .. deprecated:: 1.5.4
           Use get_current_offset instead.
        """

        warn("The get_i_offset method is deprecated, use get_current_offset instead", DeprecationWarning)
        return self.get_current_offset()

    def set_current_offset(self, offset):
        """Sets the current offset for the module.

            Args:
                offset (float):
                    The new current offset in Amps.
        """

        self.device.command(f'SOURce{self.module_number}:CURRent:LEVel:OFFSet {str(offset)}')

    def set_i_offset(self, offset):
        """
        Sets the current offset for the module

            Args:
                offset (float):
                    The new current offset in Amps
        
        .. deprecated:: 1.5.4
           Use set_current_offset instead.
        """

        warn("The set_i_offset method is deprecated, use set_current_offset instead", DeprecationWarning)
        self.set_current_offset(offset)

    def apply_dc_current(self, level, output_enable=True):
        """Apply DC current.

            Args:
                level (float):
                    DC current level in Amps.
                output_enable (bool):
                    Turns the module output on if true; off if false.
        """

        if not output_enable:
            self.disable()

        self.set_source_function('CURRent')
        self.set_shape('DC')
        self.set_current_amplitude(level)

        if output_enable:
            self.enable()

    def apply_ac_current(self, frequency, amplitude, offset=0.0, output_enable=True):
        """Apply AC current.

            Args:
                frequency (float):
                    Excitation frequency in Hz.
                amplitude (float):
                    Current amplitude in Amps.
                offset (float):
                    Current offset in Amps.
                output_enable (bool):
                    Turns the module output on if true; off if false.
        """

        if not output_enable:
            self.disable()

        self.set_source_function('CURRent')
        self.set_frequency(frequency)
        self.set_shape('SINusoid')
        self.set_current_amplitude(amplitude)
        self.set_current_offset(offset)

        if output_enable:
            self.enable()

    def get_current_limit(self):
        """Returns the current limit enforced by the module in Amps."""

        return float(self.device.query(f'SOURce{self.module_number}:CURRent:PROTection?'))

    def get_i_limit(self):
        """
        Returns the current limit enforced by the module in Amps
        
        .. deprecated:: 1.5.4
           Use get_current_limit instead.
        """

        warn("The get_i_limit method is deprecated, use get_current_limit instead", DeprecationWarning)
        return self.get_current_limit()

    def set_current_limit(self, current_limit):
        """Sets the current limit enforced by the module.

            Args:
                current_limit (float):
                    The new limit to apply in Amps.
        """
        self.device.command(f'SOURce{self.module_number}:CURRent:PROTection {str(current_limit)}')

    def set_i_limit(self, i_limit):
        """
        Sets the current limit enforced by the module

            Args:
                i_limit (float):
                    The new limit to apply in Amps
        
        .. deprecated:: 1.5.4
           Use set_current_limit instead.
        """

        warn("The set_i_limit method is deprecated, use set_current_limit instead", DeprecationWarning)
        self.set_current_limit(i_limit)

    def get_current_limit_status(self):
        """Returns whether the current limit circuitry is presently engaged.

            This limits the current sourced by the module.
        """

        return bool(int(self.device.query(f'SOURce{self.module_number}:CURRent:PROTection:TRIPped?')))

    def get_i_limit_status(self):
        """
        Returns whether the current limit circuitry is presently engaged and limiting the current sourced by the module
        
        .. deprecated:: 1.5.4
           Use get_current_limit_status instead.
        """

        warn("The get_i_limit_status method is deprecated, use get_current_limit_status instead", DeprecationWarning)
        return self.get_current_limit_status()

    def get_voltage_range(self):
        """Returns the present voltage range of the module in Volts."""

        return float(self.device.query(f'SOURce{self.module_number}:VOLTage:RANGe?'))

    def get_voltage_ac_range(self):
        """Returns the present AC voltage range of the module in Volts."""

        return float(self.device.query(f'SOURce{self.module_number}:VOLTage:RANGe:AC?'))

    def get_voltage_dc_range(self):
        """Returns the present DC voltage range of the module in Volts."""

        return float(self.device.query(f'SOURce{self.module_number}:VOLTage:RANGe:DC?'))

    def get_voltage_autorange_status(self):
        """Returns whether automatic selection of the voltage range is enabled for this module."""

        return bool(int(self.device.query(f'SOURce{self.module_number}:VOLTage:RANGe:AUTO?')))

    def configure_voltage_range(self, autorange, max_level=None, max_ac_level=None, max_dc_level=None):
        """Sets up voltage ranging for this module.

            Args:
                autorange (bool):
                    True to enable automatic range selection. False for manual ranging.
                max_level (float):
                    The largest voltage that needs to be sourced.
                max_ac_level (float):
                    The largest AC voltage that needs to be sourced. Separate AC and DC ranges are only available on
                    some modules.
                max_dc_level (float):
                    The largest DC voltage that needs to be sourced. Separate AC and DC ranges are only available on
                    some modules.
        """

        if autorange:
            if max_level is not None or max_ac_level is not None or max_dc_level is not None:
                raise ValueError('If autorange is selected, a manual range cannot be specified.')

            self.device.command(f'SOURce{self.module_number}:VOLTage:RANGe:AUTO 1')
        else:
            if max_level is not None:
                if max_ac_level is not None or max_dc_level is not None:
                    raise ValueError('Either a single range, or separate AC and DC ranges can be supplied, not both.')

                self.device.command(f'SOURce{self.module_number}:VOLTage:RANGe {str(max_level)}')
            else:
                if max_ac_level is not None:
                    self.device.command(f'SOURce{self.module_number}:VOLTage:RANGe:AC {str(max_ac_level)}')
                if max_dc_level is not None:
                    self.device.command(f'SOURce{self.module_number}:VOLTage:RANGe:DC {str(max_dc_level)}')

    def get_voltage_amplitude(self):
        """Returns the voltage amplitude for the module in Volts."""

        return float(self.device.query(f'SOURce{self.module_number}:VOLTage:LEVel:AMPLitude?'))

    def set_voltage_amplitude(self, amplitude):
        """Sets the voltage amplitude for the module.

            Args:
                amplitude (float):
                    The new voltage amplitude in Volts.
        """

        self.device.command(f'SOURce{self.module_number}:VOLTage:LEVel:AMPLitude {str(amplitude)}')

    def get_voltage_offset(self):
        """Returns the voltage offset for the module in Volts."""

        return float(self.device.query(f'SOURce{self.module_number}:VOLTage:LEVel:OFFSet?'))

    def set_voltage_offset(self, offset):
        """Sets the voltage offset for the module.

            Args:
                offset (float):
                    The new voltage offset in Volts.
        """

        self.device.command(f'SOURce{self.module_number}:VOLTage:LEVel:OFFSet {str(offset)}')

    def apply_dc_voltage(self, level, output_enable=True):
        """Apply DC voltage.

            Args:
                level (float):
                    DC voltage level in Volts.
                output_enable (bool):
                    Turns the module output on if true; off if false.
        """

        if not output_enable:
            self.disable()

        self.set_source_function('VOLTage')
        self.set_shape('DC')
        self.set_voltage_amplitude(level)

        if output_enable:
            self.enable()

    def apply_ac_voltage(self, frequency, amplitude, offset=0.0, output_enable=True):
        """Apply AC voltage.

            Args:
                frequency (float):
                    Excitation frequency in Hz.
                amplitude (float):
                    Voltage amplitude in Volts.
                offset (float):
                    Voltage offset in Volts.
                output_enable (bool):
                    Turns the module output on if true; off if false.
        """

        if not output_enable:
            self.disable()

        self.set_source_function(self.device.ExcitationType.VOLTAGE)
        self.set_frequency(frequency)
        self.set_shape('SINusoid')
        self.set_voltage_amplitude(amplitude)
        self.set_voltage_offset(offset)

        if output_enable:
            self.enable()

    def get_voltage_limit(self):
        """Returns the voltage limit enforced by the module in Volts."""

        return float(self.device.query(f'SOURce{self.module_number}:VOLTage:PROTection?'))

    def set_voltage_limit(self, voltage_limit):
        """Sets the voltage limit enforced by the module.

            Args:
                voltage_limit (float):
                    The new limit to apply in Volts.
        """

        self.device.command(f'SOURce{self.module_number}:VOLTage:PROTection {str(voltage_limit)}')

    def get_voltage_limit_status(self):
        """Returns whether the voltage limit circuitry is presently engaged.

            This limits the voltage at the output of the module.
         """

        return bool(int(self.device.query(f'SOURce{self.module_number}:VOLTage:PROTection:TRIPped?')))

    def get_present_questionable_status(self):
        """Returns the names of the questionable status register bits and their values."""

        response = self.device.query(f'STATus:QUEStionable:SOURce{self.module_number}:CONDition?', check_errors=False)
        status_register = SSMSystemModuleQuestionableRegister.from_integer(response)

        return status_register

    def get_questionable_events(self):
        """Returns the names of questionable event status register bits that are currently high.

            The event register is latching and values are reset when queried.
        """

        response = self.device.query(f'STATus:QUEStionable:SOURce{self.module_number}:EVENt?', check_errors=False)
        status_register = SSMSystemModuleQuestionableRegister.from_integer(response)

        return status_register

    def get_questionable_event_enable_mask(self):
        """Returns the names of the questionable event enable register bits and their values.

            These values determine which questionable bits propagate to the questionable event register.
        """

        response = self.device.query(f'STATus:QUEStionable:SOURce{self.module_number}:ENABle?', check_errors=False)
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
        self.device.command(f'STATus:QUEStionable:SOURce{self.module_number}:ENABle {integer_representation}', check_errors=False)

    def get_present_operation_status(self):
        """Returns the names of the operation status register bits and their values."""

        response = self.device.query(f'STATus:OPERation:SOURce{self.module_number}:CONDition?', check_errors=False)
        status_register = SSMSystemSourceModuleOperationRegister.from_integer(response)

        return status_register

    def get_operation_events(self):
        """Returns the names of operation event status register bits that are currently high.

            The event register is latching and values are reset when queried.
        """

        response = self.device.query(f'STATus:OPERation:SOURce{self.module_number}:EVENt?', check_errors=False)
        status_register = SSMSystemSourceModuleOperationRegister.from_integer(response)

        return status_register

    def get_operation_event_enable_mask(self):
        """Returns the names of the operation event enable register bits and their values.

            These values determine which operation bits propagate to the operation event register.
        """

        response = self.device.query(f'STATus:OPERation:SOURce{self.module_number}:ENABle?', check_errors=False)
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
        self.device.command(f'STATus:OPERation:SOURce{self.module_number}:ENABle {integer_representation}', check_errors=False)

    def get_identify_state(self):
        """Returns the identification state for the given pod."""
        response = bool(int(self.device.query(f'SOURce{self.module_number}:IDENtify?', check_errors=False)))
        return response

    def set_identify_state(self, state):
        """Configures the identification state for the given pod.

            Args:
                state (bool):
                    The desired state for the LED, 1 for identify, 0 for normal state.
        """
        self.device.command(f'SOURce{self.module_number}:IDENtify {int(state)}', check_errors=False)

    def get_dark_mode_state(self):
        """Returns the dark mode state for the given pod."""
        response = self.device.query(f'SOURce{self.module_number}:DMODe?', cherk_errors=False)
        return response

    def set_dark_mode_state(self, state):
        """Configures the dark mode state for the given pod.

            Args:
                state (bool):
                    The desired operation for the LED, 1 for normal mode, 0 for dark mode.
        """
        self.device.command(f'SOURce{self.module_number}:DMODe {state}', check_errors=False)

    def get_voltage_output_limit_high(self):
        """Returns the present voltage high output limit."""
        response = float(self.device.query(f'SOURce{self.module_number}:VOLTage:LIMit:HIGH?', cherk_errors=False))
        return response

    def set_voltage_output_limit_high(self, limit):
        """Configures the high voltage output limit.

            The voltage output limits are software defined limits preventing the user from entering an output which
            could potentially damage the module's load. When the shape is not DC, the limit is applied to the sum of
            the offset and amplitude. The high voltage output limit is bounded between -10 V and 10 V, and must be
            greater than the low voltage output limit.

            Args:
                limit (float):
                    The desired high output limit.
        """
        self.device.command(f'SOURce{self.module_number}:VOLTage:LIMit:HIGH {limit}', check_errors=False)

    def get_voltage_output_limit_low(self):
        """Returns the present voltage low output limit."""
        response = float(self.device.query(f'SOURce{self.module_number}:VOLTage:LIMit:LOW?', cherk_errors=False))
        return response

    def set_voltage_output_limit_low(self, limit):
        """Configures the low voltage output limit.

            The voltage output limits are software defined limits preventing the user from entering an output which
            could potentially damage the module's load. When the shape is not DC, the limit is applied to the sum of
            the offset and amplitude. The low voltage output limit is bounded between -10 V and 10 V, and must be less
            than the high voltage output limit.

            Args:
                limit (float):
                    The desired low voltage output limit.
        """
        self.device.command(f'SOURce{self.module_number}:VOLTage:LIMit:LOW {limit}', check_errors=False)

    def get_current_output_limit_high(self):
        """Returns the present current high output limit."""
        response = float(self.device.query(f'SOURce{self.module_number}:CURRent:LIMit:HIGH?', cherk_errors=False))
        return response

    def set_current_output_limit_high(self, limit):
        """Configures the high current output limit.

            The current output limits are software defined limits preventing the user from entering an output which
            could potentially damage the module's load. When the shape is not DC, the limit is applied to the sum of
            the offset and amplitude. The high current output limit is bounded between -10 V and 10 V, and must be
            greater than the low current output limit.

            Args:
                limit (float):
                    The desired high output limit.
        """
        self.device.command(f'SOURce{self.module_number}:CURRent:LIMit:HIGH {str(limit)}', check_errors=False)

    def get_current_output_limit_low(self):
        """Returns the present current low output limit."""
        response = float(self.device.query(f'SOURce{self.module_number}:CURRent:LIMit:LOW?', cherk_errors=False))
        return response

    def set_disable_on_compliance(self, disable_on_compliance):
        """Configures the module for disable on compliance.

            When disable on compliance is turned on, the module will disable output when in compliance.
            Otherwise, the module will continue to output, even when in compliance.

            Args:
                disable_on_compliance (bool):
                    1 for the module to disable when in compliance; 0 for the module to remain enabled, even in
                    compliance.
        """
        self.device.command(f'SOURce{self.module_number}:DOCompliance {int(disable_on_compliance)}', check_errors=False)

    def get_disable_on_compliance(self):
        """Returns the present state of disable on compliance."""
        response = bool(self.device.query(f'SOURce{self.module_number}:DOCompliance?', check_errors=False))
        return response

    def set_current_output_limit_low(self, limit):
        """Configures the low current output limit.

            The current output limits are software defined limits preventing the user from entering an output which
            could potentially damage the module's load. When the shape is not DC, the limit is applied to the sum of
            the offset and amplitude. The low current output limit is bounded between -10 V and 10 V, and must be less
            than the high current output limit.

            Args:
                limit (float):
                    The desired low current output limit.
        """
        self.device.command(f'SOURce{self.module_number}:CURRent:LIMit:LOW {str(limit)}', check_errors=False)

    def reset_settings(self):
        """Resets the settings for the module to their power on defaults."""

        self.device.command(f'SOURce{self.module_number}:PRESet')

    def unload(self):
        """Unloads the module."""

        self.device.command(f'SOURce{self.module_number}:UNLoad')

    def get_load_state(self):
        """Returns the loaded state for the module."""

        response = bool(int(self.device.query(f'SOURce{self.module_number}:LOAD?')))
        return response

    def get_self_cal_datetime(self):
        """Returns the self calibration date and time for the module."""

        response = self.device.query(f'SOURce{self.module_number}:SCALibration:DATE?').split(',')
        return datetime(int(response[0]), int(response[1]), int(response[2]), int(response[3]), int(response[4]), int(response[5]))

    def get_self_cal_temperature(self):
        """Returns the self calibration temperature for the module."""

        response = float(self.device.query(f'SOURce{self.module_number}:SCALibration:TEMP?'))
        return response

    @requires_firmware_version('1.7.0')
    def get_source_sweep_step_size(self, sweep_type):
        """Returns the step size of the source sweep for the module.

            Step size is a calculated parameter derived from the relevant sweep type's span and points.

        Args:
            sweep_type (SourceSweepType):
                The type of sweep for which to return the step size.
        """

        response = float(self.device.query(f'SOURce{self.module_number}:{sweep_type}:STEP?'))
        return response

    @requires_firmware_version('1.7.0')
    def get_source_sweep_time(self):
        """Returns the overall runtime of the source sweep for the module in seconds.

            Sweep time is a calculated parameter derived from the dwell time and number of points.
        """

        response = float(self.device.query(f'SOURce{self.module_number}:SWEep:TIME?'))
        return response

    @requires_firmware_version('1.7.0')
    def get_source_sweep_state(self):
        """Returns the state of the source sweep on the module."""

        response = bool(int(self.device.query(f'SOURce{self.module_number}:SWEep:STATus?')))
        return response

    @requires_firmware_version('1.7.0')
    def set_sweep_configuration(self, sweep_settings):
        """Configures a source sweep for the module.

        Args:
            sweep_settings (SourceSweepSettings):
                The configuration for a specific sweep on the module.
        """

        # Reset all sweep parameters to fixed
        self.device.command(f'SOURce{self.module_number}:VOLTage:MODE FIXed')
        self.device.command(f'SOURce{self.module_number}:CURRent:MODE FIXed')
        self.device.command(f'SOURce{self.module_number}:OFFSet:MODE FIXed')
        self.device.command(f'SOURce{self.module_number}:FREQuency:MODE FIXed')

        self.device.command(f'SOURce{self.module_number}:SWEep:DWELl {sweep_settings.dwell}')
        self.device.command(f'SOURce{self.module_number}:SWEep:POINts {sweep_settings.points}')
        self.device.command(f'SOURce{self.module_number}:SWEep:SPACing {sweep_settings.spacing}')
        self.device.command(f'SOURce{self.module_number}:SWEep:DIRection {sweep_settings.direction}')
        self.device.command(f'SOURce{self.module_number}:SWEep:DIRection:RTRip {int(sweep_settings.round_trip)}')
        self.device.command(f'SOURce{self.module_number}:SWEep:INITialdelay {float(sweep_settings.initial_delay)}')
        self.device.command(f'SOURce{self.module_number}:SWEep:BLANking {float(sweep_settings.blanking)}')
        self.device.command(f'SOURce{self.module_number}:{sweep_settings.sweep_type}:MODE SWEep')
        self.device.command(f'SOURce{self.module_number}:{sweep_settings.sweep_type}:STARt {sweep_settings.start}')
        self.device.command(f'SOURce{self.module_number}:{sweep_settings.sweep_type}:STOP {sweep_settings.stop}')

    @requires_firmware_version('1.7.0')
    def get_sweep_configuration(self, sweep_type):
        """Returns a SourceSweepSettings of the present sweep configuration for the module.

        Args:
            sweep_type (SourceSweepType):
                The sweep type for which to return the sweep settings.
        """

        return self.device.SourceSweepSettings(
            sweep_type,
            float(self.device.query(f'SOURce{self.module_number}:{sweep_type}:STARt?')),
            float(self.device.query(f'SOURce{self.module_number}:{sweep_type}:STOP?')),
            int(self.device.query(f'SOURce{self.module_number}:SWEep:POINts?')),
            float(self.device.query(f'SOURce{self.module_number}:SWEep:DWELl?')),
            self.device.query(f'SOURce{self.module_number}:SWEep:DIRection?'),
            bool(int(self.device.query(f'SOURce{self.module_number}:SWEep:DIRection:RTRip?'))),
            self.device.query(f'SOURce{self.module_number}:SWEep:SPACing?'),
            float(self.device.query(f'SOURce{self.module_number}:SWEep:INITialdelay?')),
            float(self.device.query(f'SOURce{self.module_number}:SWEep:BLANking?')))

    @requires_firmware_version('1.7.0')
    def disable_all_sweeping(self):
        """Disables all source signals that support sweeping on the module."""

        for sweep_type in self.device.SourceSweepType:
            self.device.command(f'SOURce{self.module_number}:{sweep_type}:MODE FIXED')

    @requires_firmware_version('1.7.0')
    def disable_sweeping(self, sweep_type):
        """Disables the sweeping of the specified sweep type on the module.

        Args:
            sweep_type (SourceSweepType):
                The type of sweep to disable.
        """

        self.device.command(f'SOURce{self.module_number}:{sweep_type}:MODE FIXED')

    def set_voltage_ramp_configuration(self, stop_amplitude, start_amplitude=None, slew_rate=1.0, round_trip=False):
        """Sets up a parameter sweep that ramps the voltage output to the desired amplitude.

            Uses the smallest possible step size.

        Args:
            stop_amplitude (float):
                The voltage amplitude of the output when the ramp completes.
            start_amplitude (float):
                The voltage amplitude of the output when the ramp starts. Default is the present amplitude setting.
            slew_rate (float):
                The rate in volts per second to ramp the output. Default is 1 volt per second.
            round_trip (bool):
                Ramps to the stop amplitude then ramps back to the start amplitude when true
        """
        # Use the present voltage amplitude as the starting point if no start is specified
        if start_amplitude is None:
            start_amplitude = self.get_voltage_amplitude()

        ramp_total_time = abs(stop_amplitude - start_amplitude) / abs(slew_rate)

        # The ramp time is doubled if it is round trip
        if round_trip:
            ramp_total_time *= 2

        if ramp_total_time != 0:
            # Determine the shortest dwell time that can be used without exceeding the maximum number of points
            dwell_time = math.ceil(ramp_total_time / (self.device.min_sweep_dwell * self.device.max_sweep_points)) * self.device.min_sweep_dwell
            num_points = round(ramp_total_time / dwell_time)
        else:
            dwell_time = self.device.min_sweep_dwell
            num_points = 2

        sweep_config = self.device.SourceSweepSettings(sweep_type=self.device.SourceSweepType.VOLTAGE_AMPLITUDE,
                                                       start=start_amplitude,
                                                       stop=stop_amplitude,
                                                       points=num_points,
                                                       dwell=dwell_time,
                                                       direction=self.device.SourceSweepSettings.Direction.UP,
                                                       round_trip=round_trip,
                                                       initial_delay=0.0,
                                                       blanking=0.0)
        self.set_sweep_configuration(sweep_config)

    def set_current_ramp_configuration(self, stop_amplitude, start_amplitude=None, slew_rate=0.001, round_trip=False):
        """Sets up a parameter sweep that ramps the current output to the desired amplitude.

            Uses the smallest possible step size.

        Args:
            stop_amplitude (float):
                The current amplitude of the output when the ramp completes.
            start_amplitude (float):
                The current amplitude of the output when the ramp starts. Default is the present amplitude setting.
            slew_rate (float):
                The rate in amps per second to ramp the output. Default is 1 mA per second.
            round_trip (bool):
                Ramps to the stop amplitude then ramps back to the start amplitude when true
        """
        # Use the present voltage amplitude as the starting point if no start is specified
        if start_amplitude is None:
            start_amplitude = self.get_current_amplitude()

        ramp_total_time = abs(stop_amplitude - start_amplitude) / abs(slew_rate)

        # The ramp time is doubled if it is round trip
        if round_trip:
            ramp_total_time *= 2

        if ramp_total_time != 0:
            # Determine the shortest dwell time that can be used without exceeding the maximum number of points
            dwell_time = math.ceil(ramp_total_time / (self.device.min_sweep_dwell * self.device.max_sweep_points)) * self.device.min_sweep_dwell
            num_points = round(ramp_total_time / dwell_time)
        else:
            dwell_time = self.device.min_sweep_dwell
            num_points = 2

        sweep_config = self.device.SourceSweepSettings(sweep_type=self.device.SourceSweepType.CURRENT_AMPLITUDE,
                                                       start=start_amplitude,
                                                       stop=stop_amplitude,
                                                       points=num_points,
                                                       dwell=dwell_time,
                                                       direction=self.device.SourceSweepSettings.Direction.UP,
                                                       round_trip=round_trip,
                                                       initial_delay=0.0,
                                                       blanking=0.0)
        self.set_sweep_configuration(sweep_config)

    @requires_firmware_version('1.7.0')
    def do_dc_sweep_step_and_measure(self,
                                     start_amplitude,
                                     stop_amplitude,
                                     *optional_custom_data_sources,
                                     dwell_time='AUTO',
                                     number_of_points='AUTO',
                                     settle_time=0.0,
                                     initial_delay=0.0,
                                     sweep_spacing='LINEAR',
                                     round_trip=False,
                                     include_source_amplitude=True,
                                     include_relative_time=False):
        """Immediately do a DC source sweep and returns data for each point in the sweep.

        Args:
            start_amplitude (float):
                The starting source value of the sweep in volts or amps
            stop_amplitude (float):
                The ending source value of the sweep in volts or amps
            dwell_time (float):
                Time duration of each step in seconds, defaults to AUTO
            number_of_points (int):
                How many steps to take going from the start to the stop amplitude.
                AUTO chooses a decade step size that results in between 100 and 1,000 points
            optional_custom_data_sources (SSMSystemDataSourceMnemonic or str, int):
                Variable length list of pairs of (DATA_SOURCE, CHANNEL_INDEX).
                Defaults to DC on the source's matching measure channel if unspecified.
                If specified only the specified custom data sources will be collected.
                If specified the corresponding measure channel will not be configured automatically.
            settle_time (float):
                How long to wait before taking a measurement after a step change.
                Defaults to zero. Must be shorter than the dwell time.
            initial_delay (float):
                Time to wait before starting the sweep, defaults to zero.
            sweep_spacing (str or SweepSpacing enum):
                LINEAR or LOGARITHMIC sweep
            round_trip (bool):
                Sweeps to the stop amplitude then sweeps back to the start amplitude when true.
                Returns double the sweep number of points when true.
            include_source_amplitude (bool):
                The source amplitude is included in the returned data when true
            include_relative_time (bool):
                The time since the start of the sweep is in the returned data when true
        """
        self.set_shape('DC')

        if dwell_time == 'AUTO':
            # default of 3 power line cycles
            dwell_time = self._calculate_dwell_time_for_shape('DC', 3)

        if number_of_points == 'AUTO':
            number_of_points = self._calculate_number_of_sweep_points(start_amplitude, stop_amplitude, sweep_spacing)

        # if custom data sources are not specified, automatically configure the corresponding measure module
        if not optional_custom_data_sources:
            measure_module = self.device.get_measure_module(self.module_number)
            averaging_nplcs = (dwell_time - settle_time) * self.device.get_line_frequency()
            measure_module.setup_dc_measurement(averaging_nplcs)

        # determine if the source will provide current or voltage
        if self.get_source_function() == 'VOLTAGE':
            sweep_type = self.device.SourceSweepType.VOLTAGE_AMPLITUDE
        else:
            sweep_type = self.device.SourceSweepType.CURRENT_AMPLITUDE

        # configure the sweep
        sweep_config = self.device.SourceSweepSettings(sweep_type=sweep_type,
                                                       start=start_amplitude,
                                                       stop=stop_amplitude,
                                                       points=number_of_points,
                                                       dwell=dwell_time,
                                                       spacing=sweep_spacing,
                                                       direction=self.device.SourceSweepSettings.Direction.UP,
                                                       round_trip=round_trip,
                                                       initial_delay=initial_delay,
                                                       blanking=settle_time)
        self.set_sweep_configuration(sweep_config)

        # double the number of points to stream if doing a round trip sweep
        if round_trip:
            number_of_points *= 2

        # Configure data streaming which initiates the configured sweep
        if optional_custom_data_sources:
            sweep_data = self.device.get_data(1 / dwell_time, number_of_points, *optional_custom_data_sources)
        else:
            data_sources = []
            if include_relative_time:
                data_sources.append(('RTIME', self.module_number))
            if include_source_amplitude:
                data_sources.append(('SAMP', self.module_number))
            data_sources.append(('MDC', self.module_number))
            sweep_data = self.device.get_data(1 / dwell_time, number_of_points, *data_sources)

        return sweep_data

    def get_voltage_sense_mode(self):
        """Returns the source voltage source sense for the specified module as either LOCal or REMote"""

        return self.device.query(f"SOURce{self.module_number}:VOLTage:SMODe?")

    def set_voltage_sense_mode(self, state):
        """Sets the source voltage source sense for the specified module

        Args:
            state (str):
                Voltage source sense ('LOCal' or 'REMote')
        """

        self.device.command(f"SOURce{self.module_number}:VOLTage:SMODe {state}")

    def get_readback_dc(self):
        """Returns the DC source readback measurement"""

        response = float(self.device.query(f"FETCh:SOURce{self.module_number}:READback:DC?"))
        return response

    def get_readback_rms(self):
        """Returns the RMS source readback measurement"""

        response = float(self.device.query(f"FETCh:SOURce{self.module_number}:READback:RMS?"))
        return response

    def get_readback_nplcycles(self):
        """Returns the source readback averaging time in number of power line cycles (NPLC) of the module"""

        response = float(self.device.query(f"SOURce{self.module_number}:READback:NPLCycles?"))
        return response

    def get_requested_readback_nplcycles(self):
        """Returns the requested source readback averaging time in number of power line cycles (NPLC) of the specified module"""

        response = float(self.device.query(f"SOURce{self.module_number}:READback:NPLCycles:REQuested?"))
        return response

    def get_actual_readback_nplcycles(self):
        """Returns the actual source readback averaging time in number of power line cycles (NPLC) of the specified module"""

        response = float(self.device.query(f"SOURce{self.module_number}:READback:NPLCycles:ACTual?"))
        return response

    def set_readback_nplcycles(self, value):
        """Sets the source readback averaging time in number of power line cycles (NPLC) of the module.
         
            The NPLC value must be between 0.01 and 600.00.

        Args:
            value (float):
                The averaging time in number of power line cycles (NPLC)
        """

        self.device.command(f"SOURce{self.module_number}:READback:NPLCycles {value}")

    def _calculate_number_of_sweep_points(self, start_value, stop_value, sweep_spacing):
        """Calculates the number of sweep points based on the start and stop values and the sweep spacing.

        Args:
            start_value (float): The starting value of the sweep.
            stop_value (float): The stopping value of the sweep.
            sweep_spacing (float): LINEAR or LOGARITHMIC spacing between sweep points.

        Returns:
            int: The number of sweep points.
        """
        if sweep_spacing == 'LINEAR':
            step_size = 10 ** (math.floor(math.log10(abs(stop_value - start_value))) - 2)
            number_of_points = round(abs(stop_value - start_value) / step_size + 1)
        else:
            step_size = 10 ** (math.floor(math.log10(abs(stop_value / start_value))) - 2)
            number_of_points = round(abs(stop_value / start_value) / step_size + 1)
        return number_of_points

    def _calculate_dwell_time_for_shape(self, source_shape, power_line_cycles=3):
        """Calculates the dwell time based on the source shape and power line cycles.

        Args:
            source_shape (str): The shape of the source signal ('DC', 'SINUSOID', 'SQUARE', 'TRIANGLE').
            power_line_cycles (int): The number of power line cycles to use for the calculation.

        Returns:
            float: The calculated dwell time in seconds.
        """
        min_dwell_for_shape = self.device.source_shape_dwell_times[source_shape]
        return round(power_line_cycles / self.device.get_line_frequency() / min_dwell_for_shape, 0) * min_dwell_for_shape

    def _get_ac_sweep_parameter_and_data_source(self, ac_sweep_parameter, source_frequency, source_amplitude, source_offset):
        """Configures the AC source sweep based on the specified parameter and returns the corresponding data source mnemonic and sweep type.

        Args:
            ac_sweep_parameter (str): The AC parameter to sweep ('OFFSET', 'FREQUENCY', 'AMPLITUDE').
            source_frequency (float): The AC frequency in Hz.
            source_amplitude (float): The AC amplitude in volts or amps.
            source_offset (float): The AC offset in volts or amps.
            excitation_mode (str): The excitation mode ('VOLTAGE' or 'CURRENT').

        Returns:
            tuple: A tuple containing the data source mnemonics and sweep type.
        """

        # Determine if the source will provide current or voltage
        excitation_mode = self.get_source_function()

        if ac_sweep_parameter == "OFFSET":
            if source_frequency is None or source_amplitude is None:
                raise ValueError("source_frequency and source_amplitude are required when sweeping 'OFFSET'.")
            self.set_frequency(source_frequency)
            if excitation_mode == "VOLTAGE":
                self.set_voltage_amplitude(source_amplitude)
            else:
                self.set_current_amplitude(source_amplitude)
            return self.device.SourceSweepType.OFFSET, SSMSystemEnums.DataSourceMnemonic.SOURCE_OFFSET

        if ac_sweep_parameter == "FREQUENCY":
            if source_amplitude is None or source_offset is None:
                raise ValueError("source_amplitude and source_offset are required when sweeping 'FREQUENCY'.")
            if excitation_mode == "VOLTAGE":
                self.set_voltage_amplitude(source_amplitude)
                self.set_voltage_offset(source_offset)
            else:
                self.set_current_amplitude(source_amplitude)
                self.set_current_offset(source_offset)
            return self.device.SourceSweepType.FREQUENCY, SSMSystemEnums.DataSourceMnemonic.SOURCE_FREQUENCY

        if ac_sweep_parameter == "AMPLITUDE":
            if source_frequency is None or source_offset is None:
                raise ValueError("source_frequency and source_offset are required when sweeping 'AMPLITUDE'.")
            self.set_frequency(source_frequency)
            if excitation_mode == "VOLTAGE":
                self.set_voltage_offset(source_offset)
            else:
                self.set_current_offset(source_offset)
            return (
                self.device.SourceSweepType.VOLTAGE_AMPLITUDE
                if excitation_mode == "VOLTAGE"
                else self.device.SourceSweepType.CURRENT_AMPLITUDE,
                SSMSystemEnums.DataSourceMnemonic.SOURCE_AMPLITUDE,
            )

        raise ValueError("ac_sweep_parameter must be 'OFFSET', 'FREQUENCY', or 'AMPLITUDE'.")

    def do_ac_amplitude_sweep_step_and_measure(self, start_amplitude, stop_amplitude, ac_shape, source_frequency,
                            source_offset=0, optional_custom_data_sources=None, **kwargs):
        """Sweep AC amplitude at fixed frequency and offset.

        Args:
            start_amplitude (float): The starting amplitude of the sweep in volts or amps.
            stop_amplitude (float): The ending amplitude of the sweep in volts or amps.
            ac_shape (str): The AC waveform shape, e.g., 'SINUSOID', 'SQUARE', 'TRIANGLE'.
            source_frequency (float): The AC frequency in Hz.
            source_offset (float): The AC offset in volts or amps. Default is 0.
            optional_custom_data_sources (SSMSystemDataSourceMnemonic or str, int): Variable length list of pairs of (DATA_SOURCE, CHANNEL_INDEX).
            kwargs: Additional keyword arguments to pass to the _do_ac_parameter_sweep_step_and_measure method.

        Returns:
            list: A list of tuples containing the measured data for each point in the sweep.
        """

        return self._do_ac_parameter_sweep_step_and_measure('AMPLITUDE',
                                                            start_amplitude,
                                                            stop_amplitude,
                                                            *optional_custom_data_sources,
                                                            ac_shape=ac_shape,
                                                            source_frequency=source_frequency,
                                                            source_offset=source_offset,
                                                            **kwargs)

    def do_ac_frequency_sweep_step_and_measure(self, start_frequency, stop_frequency, source_amplitude, ac_shape,
                           source_offset=0, optional_custom_data_sources=None, **kwargs):
        """Sweep AC frequency at fixed amplitude and offset.

        Args:
            start_frequency (float): The starting frequency of the sweep in Hz.
            stop_frequency (float): The ending frequency of the sweep in Hz.
            source_amplitude (float): The AC amplitude in volts or amps.
            ac_shape (str): The AC waveform shape, e.g., 'SINUSOID', 'SQUARE', 'TRIANGLE'.
            source_offset (float): The AC offset in volts or amps. Default is 0.
            optional_custom_data_sources (SSMSystemDataSourceMnemonic or str, int): Variable length list of pairs of (DATA_SOURCE, CHANNEL_INDEX).
            kwargs: Additional keyword arguments to pass to the _do_ac_parameter_sweep_step_and_measure method.

        Returns:
            list: A list of tuples containing the measured data for each point in the sweep.
        """

        return self._do_ac_parameter_sweep_step_and_measure('FREQUENCY',
                                                            start_frequency,
                                                            stop_frequency,
                                                            *optional_custom_data_sources,
                                                            ac_shape=ac_shape,
                                                            source_amplitude=source_amplitude,
                                                            source_offset=source_offset,
                                                            **kwargs)

    def do_ac_offset_sweep_step_and_measure(self, start_offset, stop_offset, ac_shape, source_amplitude, source_frequency,
                         optional_custom_data_sources=None, **kwargs):
        """Sweep AC offset at fixed amplitude and frequency.

        Args:
            start_offset (float): The starting offset of the sweep in volts or amps.
            stop_offset (float): The ending offset of the sweep in volts or amps.
            source_amplitude (float): The AC amplitude in volts or amps.
            ac_shape (str): The AC waveform shape, e.g., 'SINUSOID', 'SQUARE', 'TRIANGLE'.
            source_frequency (float): The AC frequency in Hz.
            optional_custom_data_sources (SSMSystemDataSourceMnemonic or str, int): Variable length list of pairs of (DATA_SOURCE, CHANNEL_INDEX).
            kwargs: Additional keyword arguments to pass to the _do_ac_parameter_sweep_step_and_measure method.

        Returns:
            list: A list of tuples containing the measured data for each point in the sweep.
        """

        return self._do_ac_parameter_sweep_step_and_measure('OFFSET',
                                                            start_offset,
                                                            stop_offset,
                                                            *optional_custom_data_sources,
                                                            ac_shape=ac_shape,
                                                            source_amplitude=source_amplitude,
                                                            source_frequency=source_frequency,
                                                            **kwargs)
    def _do_ac_parameter_sweep_step_and_measure(self,
                                                ac_sweep_parameter,
                                                start_value,
                                                stop_value,
                                                *optional_custom_data_sources,
                                                ac_shape='SINUSOID',
                                                source_amplitude=None,
                                                source_frequency=None,
                                                source_offset=None,
                                                dwell_time='AUTO',
                                                number_of_points='AUTO',
                                                settle_time=0.0,
                                                initial_delay=0.0,
                                                sweep_spacing='LINEAR',
                                                round_trip=False,
                                                include_source_sweep_parameter=True,
                                                include_relative_time=False):
        """Immediately runs an AC parameter(amplitude, frequency, offset) source sweep and returns data for each point in the sweep.

        Args:
            ac_sweep_parameter (str):
                The AC parameter to sweep, 'OFFSET', 'FREQUENCY', 'AMPLITUDE'.
            ac_shape (str):
                The AC waveform shape, e.g., 'SINUSOID', 'SQUARE', 'TRIANGLE'.
            start_value (float):
                The starting value of the AC parameter sweep, e.g., amplitude(volts/amps), offset(volts/amps), or frequency(Hz).
            stop_value (float):
                The ending value of the AC parameter sweep, e.g., amplitude(volts/amps), offset(volts/amps), or frequency(Hz).
            source_amplitude (float):
                The AC voltage amplitude in volts or amps.
            source_frequency (float):
                The AC frequency in Hz.
            source_offset (float):
                The AC offset in volts or amps.
            dwell_time (float):
                Time duration of each step in seconds, defaults to AUTO.
            number_of_points (int):
                How many steps to take going from the start to the stop amplitude.
                AUTO chooses a decade step size that results in between 100 and 1,000 points
            optional_custom_data_sources (SSMSystemDataSourceMnemonic or str, int):
                Variable length list of pairs of (DATA_SOURCE, CHANNEL_INDEX).
                Defaults to AC on the source's matching measure channel if unspecified.
                If specified only the specified custom data sources will be collected.
                If specified the corresponding measure channel will not be configured automatically.
            settle_time (float):
                How long to wait before taking a measurement after a step change.
                Defaults to zero. Must be shorter than the dwell time.
            initial_delay (float):
                Time to wait before starting the sweep, defaults to zero.
            sweep_spacing (str or SweepSpacing enum):
                LINEAR or LOGARITHMIC sweep.
            round_trip (bool):
                Sweeps to the stop amplitude then sweeps back to the start amplitude when true.
                Returns double the sweep number of points when true.
            include_source_sweep_parameter (bool):
                The source sweep parameter is included in the returned data when true
            include_relative_time (bool):
                The time since the start of the sweep is in the returned data when true
        """
        self.set_shape(ac_shape)

        sweep_type, data_source_mnemonics = self._get_ac_sweep_parameter_and_data_source(ac_sweep_parameter,
                                                                                        source_frequency,
                                                                                        source_amplitude,
                                                                                        source_offset)

        if dwell_time == 'AUTO':
            # default of 3 power line cycles
            dwell_time = self._calculate_dwell_time_for_shape(ac_shape, 3)

        if number_of_points == 'AUTO':
            number_of_points = self._calculate_number_of_sweep_points(start_value, stop_value, sweep_spacing)

        # if custom data sources are not specified, automatically configure the corresponding measure module
        if not optional_custom_data_sources:
            measure_module = self.device.get_measure_module(self.module_number)
            averaging_nplcs = (dwell_time - settle_time) * self.device.get_line_frequency()
            measure_module.setup_ac_measurement(averaging_nplcs)

        sweep_config = self.device.SourceSweepSettings(sweep_type=sweep_type,
                                                       start=start_value,
                                                       stop=stop_value,
                                                       points=number_of_points,
                                                       dwell=dwell_time,
                                                       spacing=sweep_spacing,
                                                       direction=self.device.SourceSweepSettings.Direction.UP,
                                                       round_trip=round_trip,
                                                       initial_delay=initial_delay,
                                                       blanking=settle_time)
        self.set_sweep_configuration(sweep_config)

        # double the number of points to stream if doing a round trip sweep
        if round_trip:
            number_of_points *= 2

        # Configure data streaming which initiates the configured sweep
        if optional_custom_data_sources:
            sweep_data = self.device.get_data(1 / dwell_time, number_of_points, *optional_custom_data_sources)
        else:
            data_sources = []
            if include_relative_time:
                data_sources.append((SSMSystemEnums.DataSourceMnemonic.RELATIVE_TIME, self.module_number))
            if include_source_sweep_parameter:
                data_sources.append((data_source_mnemonics, self.module_number))
            data_sources.append((SSMSystemEnums.DataSourceMnemonic.MEASURE_THETA, self.module_number))
            data_sources.append((SSMSystemEnums.DataSourceMnemonic.MEASURE_R, self.module_number))
            sweep_data = self.device.get_data(1 / dwell_time, number_of_points, *data_sources)

        return sweep_data

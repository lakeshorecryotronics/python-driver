"""Implements functionality unique to the Lake Shore M81."""

import struct
from base64 import b64decode
from threading import Lock

from .requires_firmware_version import requires_firmware_version
from .xip_instrument import XIPInstrument


class SSMSystem(XIPInstrument):
    """Class for interaction with the M81 instrument"""

    vid_pid = [(0x1FB9, 0x0704), (0x10C4, 0xEA60)]

    def __init__(self,
                 serial_number=None,
                 com_port=None,
                 baud_rate=921600,
                 flow_control=True,
                 timeout=2.0,
                 ip_address=None,
                 tcp_port=7777,
                 **kwargs):

        # Call the parent init, then fill in values specific to SSM
        XIPInstrument.__init__(self, serial_number, com_port, baud_rate, flow_control, timeout, ip_address, tcp_port, **kwargs)
        # self.status_byte_register = StatusByteRegister
        # self.standard_event_register = StandardEventRegister
        # self.operation_register = TeslameterOperationRegister
        # self.questionable_register = TeslameterQuestionableRegister

        # Instantiate pods
        self.num_source_pods = 3
        self.num_measure_pods = 3
        self.source = [SourcePod(i + 1, self) for i in range(self.num_source_pods)]
        self.measure = [MeasurePod(i + 1, self) for i in range(self.num_measure_pods)]

        self.stream_lock = Lock()

    def get_source_pod(self, pod_number):
        """Returns a SourcePod instance for the given port number"""

        try:
            return self.source[pod_number - 1]
        except IndexError:
            raise IndexError('Invalid pod number. Must be between 1 and {}'.format(self.num_source_pods))

    def get_measure_pod(self, pod_number):
        """Returns a MeasurePod instance for the given port number"""

        try:
            return self.measure[pod_number - 1]
        except IndexError:
            raise IndexError('Invalid pod number. Must be between 1 and {}'.format(self.num_measure_pods))

    @requires_firmware_version('0.3')
    def stream_data(self, rate, num_points, *data_sources):
        """Generator object to stream data from the instrument. Coming in 0.3."""

        with self.stream_lock:
            self.command('TRACe:RESEt')
            self.command('TRACe:FORMat:ELEMents {}'.format(','.join(data_sources)))
            self.command('TRACe:FORMat:ENCOding B64')
            self.command('TRACe:RATE {}'.format(rate))

            bytes_per_row = self.query('TRACe:FORMat:BCOunt?')
            binary_format = '<' + self.query('TRACe:FORMat:BFORmat?')

            if num_points is not None:
                self.command('TRACe:STARt {}'.format(num_points))
            else:
                self.command('TRACe:STARt')

            num_collected = 0
            while num_points is None or num_collected < num_points:
                b64_string = ''
                while not b64_string:
                    b64_string = self.query('TRACe:DATA:ALL?')

                new_bytes = b64decode(b64_string)
                rows = [new_bytes[i:i + bytes_per_row] for i in range(0, len(new_bytes), bytes_per_row)]

                for row in rows:
                    data = struct.unpack(binary_format, row)

                    yield data

    @requires_firmware_version('0.3')
    def get_data(self, rate, num_points, *data_sources):
        """Like stream_data, but returns a list. Coming in 0.3."""

        return list(self.stream_data(rate, num_points, *data_sources))

    @requires_firmware_version('0.3')
    def log_data_to_csv_file(self, rate, num_points, file, *data_sources):
        """Like stream_data, but logs directly to a CSV file. Coming in 0.3."""

        header = self.query('TRACe:DATA:HEADer?')
        file.write(header + '\n')

        for row in self.stream_data(rate, num_points, *data_sources):
            file.write(','.join(str(x) for x in row) + '\n')


class BasePod:
    """Class for interaction with a specific channel, not specific to source or measure"""

    def __init__(self, pod_number, device):
        self.pod_number = pod_number
        self.device = device


class SourcePod(BasePod):
    """Class for interaction with a specific source channel of the M81 instrument"""

    def get_pod_name(self):
        """Returns the name of the pod (i.e. BCS-10)"""

        return self.device.query('SOURce{}:NAME?'.format(self.pod_number)).strip('\"')

    def get_pod_serial(self):
        """Returns the serial number of the pod (i.e. LSA1234)"""

        return self.device.query('SOURce{}:SERial?'.format(self.pod_number)).strip('\"')

    def get_hw_version(self):
        """Returns the hardware version of the pod"""

        return int(self.device.query('SOURce{}:HWVersion?'.format(self.pod_number)))

    def get_enable_state(self):
        """Returns the output state of the pod"""

        return bool(int(self.device.query('SOURce{}:STATe?'.format(self.pod_number))))

    def set_enable_state(self, state):
        """Set the enable state of the pod

            Args:
                state (bool):
                    The new output state
        """

        self.device.command('SOURce{}:STATe {}'.format(self.pod_number, str(int(state))))

    def enable(self):
        """Sets the enable state of the pod to True"""

        self.set_enable_state(True)

    def disable(self):
        """Sets the enable state of the pod to False"""

        self.set_enable_state(False)

    def get_excitation_mode(self):
        """Returns the excitation mode of the pod. 'CURRENT' or 'VOLTAGE'."""

        return self.device.query('SOURce{}:FUNCtion:MODE?'.format(self.pod_number))

    def set_excitation_mode(self, excitation_mode):
        """Sets the excitation mode of the pod

            Args:
                excitation_mode (str):
                    The new excitation mode ('CURRENT' or "VOLTAGE')
        """

        self.device.command('SOURce{}:FUNCtion:MODE {}'.format(self.pod_number, excitation_mode))

    def go_to_current_mode(self):
        """Sets the excitation mode of the pod to 'CURRENT'"""

        self.set_excitation_mode('CURRent')

    def go_to_voltage_mode(self):
        """Sets the excitation mode of the pod to 'CURRENT'"""

        self.set_excitation_mode('VOLTage')

    def get_shape(self):
        """Returns the signal shape of the pod. 'DC' or 'SINUSOID'."""

        return self.device.query('SOURce{}:FUNCtion:SHAPe?'.format(self.pod_number))

    def set_shape(self, shape):
        """Sets the signal shape of the pod

            Args:
                shape (str):
                    The new signal shape ('DC' or 'SINUSOID')
        """

        self.device.command('SOURce{}:FUNCtion:SHAPe {}'.format(self.pod_number, shape))

    def get_frequency(self):
        """Returns the excitation frequency of the pod"""

        return float(self.device.query('SOURce{}:FREQuency?'.format(self.pod_number)))

    def set_frequency(self, frequency):
        """Sets the excitation frequency of the pod

            Args:
                frequency (float):
                    The new excitation frequency
        """
        self.device.command('SOURce{}:FREQuency {}'.format(self.pod_number, str(frequency)))

    def get_sync_state(self):
        """Returns whether the source channel synchronization feature is engaged

            If true, this channel will ignore its own frequency, and instead track the frequency of the synchronization source.
            If false, this channel will generate its own frequency.
        """

        return bool(int(self.device.query('SOURce{}:SYNChronize:STATe?'.format(self.pod_number))))

    def get_sync_source(self):
        """Returns the channel used for frequency synchronization"""

        return self.device.query('SOURce{}:SYNChronize:SOURce?'.format(self.pod_number))

    def get_sync_phase_shift(self):
        """Returns the phase shift applied between the synchronization source and this channel"""

        return float(self.device.query('SOURce{}:SYNChronize:PHASe?'.format(self.pod_number)))

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
        self.device.command('SOURce{}:SYNChronize:SOURce {}'.format(self.pod_number, source))
        self.device.command('SOURce{}:SYNChronize:PHASe {}'.format(self.pod_number, str(phase_shift)))
        self.device.command('SOURce{}:SYNChronize:STATe {}'.format(self.pod_number, str(int(enable_sync))))

    def get_duty(self):
        """Returns the duty cycle of the pod"""

        return float(self.device.query('SOURce{}:DCYCle?'.format(self.pod_number)))

    def set_duty(self, duty):
        """Sets the duty cycle of the pod

            Args:
                duty (float):
                    The new duty cycle
        """

        self.device.command('SOURce{}:DCYCle {}'.format(self.pod_number, str(duty)))

    def get_coupling(self):
        """Returns the coupling type of the pod. 'AC' or 'DC'."""

        return self.device.query('SOURce{}:COUPling?'.format(self.pod_number))

    def set_coupling(self, coupling):
        """Sets the coupling of the pod

            Args:
                coupling (str):
                    The new coupling type ('AC', or 'DC')
        """
        self.device.command('SOURce{}:COUPling {}'.format(self.pod_number, coupling))

    def use_ac_coupling(self):
        """Sets the coupling type of the pod to 'AC'"""

        self.set_coupling('AC')

    def use_dc_coupling(self):
        """Sets the coupling type of the pod to 'DC'"""

        self.set_coupling('DC')

    def get_guard_state(self):
        """Returns the guard state of the pod"""

        return bool(int(self.device.query('SOURce{}:GUARd?'.format(self.pod_number))))

    def set_guard_state(self, guard_state):
        """Sets the guard state of the pod

            Args:
                guard_state (bool):
                    The new guard state (True to enable guards, False to disable guards)
        """

        self.device.command('SOURce{}:GUARd {}'.format(self.pod_number, str(int(guard_state))))

    def enable_guards(self):
        """Sets the guard state of the pod to True"""

        self.set_guard_state(True)

    def disable_guards(self):
        """Sets the guard state of the pod to False"""

        self.set_guard_state(False)

    def get_cmr_state(self):
        """Returns the Common Mode Reduction (CMR) state of the pod"""

        return bool(int(self.device.query('SOURce{}:GUARd?'.format(self.pod_number))))

    def set_cmr_state(self, cmr_state):
        """Sets the Common Mode Reduction (CMR) state of the pod

            Args:
                cmr_state (bool):
                    The new CMR state (True to enable guards, False to disable guards)
        """

        self.device.command('SOURce{}:GUARd {}'.format(self.pod_number, str(int(cmr_state))))

    def enable_cmr(self):
        """Sets the CMR state of the pod to True"""

        self.set_cmr_state(True)

    def disable_cmr(self):
        """Sets the CMR state of the pod to False"""

        self.set_cmr_state(False)

    def get_i_range(self):
        """Returns the present current range of the pod in Amps"""

        return float(self.device.query('SOURce{}:CURRent:RANGe?'.format(self.pod_number)))

    def get_i_ac_range(self):
        """Returns the present AC current range of the pod in Amps"""

        return float(self.device.query('SOURce{}:CURRent:RANGe:AC?'.format(self.pod_number)))

    def get_i_dc_range(self):
        """Returns the present DC current range of the pod in Amps"""

        return float(self.device.query('SOURce{}:CURRent:RANGe:DC?'.format(self.pod_number)))

    def get_i_autorange_status(self):
        """Returns whether automatic selection of the current range is enabled for this pod"""

        return bool(int(self.device.query('SOURce{}:CURRent:RANGe:AUTO?'.format(self.pod_number))))

    def configure_i_range(self, autorange, max_level=None, max_ac_level=None, max_dc_level=None):
        """Sets up current ranging for this pod

            Args:
                autorange (bool):
                    True to enable automatic range selection. False for manual ranging.

                max_level (float):
                    The largest current that needs to be sourced.

                max_ac_level (float):
                    The largest AC current that needs to be sourced. Separate AC and DC ranges are only available on some pods.

                max_dc_level (float):
                    The largest DC current that needs to be sourced. Separate AC and DC ranges are only available on some pods.
        """

        if autorange:
            if max_level is not None or max_ac_level is not None or max_dc_level is not None:
                raise ValueError('If autorange is selected, a manual range cannot be specified.')

            self.device.command('SOURce{}:CURRent:RANGe:AUTO 1'.format(self.pod_number))
        else:
            if max_level is not None:
                if max_ac_level is not None or max_dc_level is not None:
                    raise ValueError('Either a single range, or separate AC and DC ranges can be supplied, not both.')

                self.device.command('SOURce{}:CURRent:RANGe {}'.format(self.pod_number, str(max_level)))
            else:
                if max_ac_level is not None:
                    self.device.command('SOURce{}:CURRent:RANGe:AC {}'.format(self.pod_number, str(max_ac_level)))
                if max_dc_level is not None:
                    self.device.command('SOURce{}:CURRent:RANGe:DC {}'.format(self.pod_number, str(max_dc_level)))

    def get_i_amplitude(self):
        """Returns the current amplitude for the pod in Amps"""

        return float(self.device.query('SOURce{}:CURRent:LEVel:AMPLitude?'.format(self.pod_number)))

    def set_i_amplitude(self, amplitude):
        """Sets the current amplitude for the pod

            Args:
                amplitude (float):
                    The new current amplitude in Amps
        """
        self.device.command('SOURce{}:CURRent:LEVel:AMPLitude {}'.format(self.pod_number, str(amplitude)))

    def get_i_offset(self):
        """Returns the current offset for the pod in Amps"""

        return float(self.device.query('SOURce{}:CURRent:LEVel:OFFSet?'.format(self.pod_number)))

    def set_i_offset(self, offset):
        """Sets the current offset for the pod

            Args:
                offset (float):
                    The new current offset in Amps
        """

        self.device.command('SOURce{}:CURRent:LEVel:OFFSet {}'.format(self.pod_number, str(offset)))

    def apply_dc_current(self, level, enable_output=True):
        """Apply DC current

            Args:
                level (float):
                    DC current level in Amps

                enable_output (bool):
                    Set the enable state of the pod to True
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
                    Set the enable state of the pod to True
        """

        self.set_excitation_mode('CURRent')
        self.set_frequency(frequency)
        self.set_shape('SINusoid')
        self.set_i_amplitude(amplitude)
        self.set_i_offset(offset)

        if enable_output:
            self.enable()

    def get_i_limit(self):
        """Returns the current limit enforced by the pod in Amps"""

        return float(self.device.query('SOURce{}:CURRent:PROTection?'.format(self.pod_number)))

    def set_i_limit(self, i_limit):
        """Sets the current limit enforced by the pod

            Args:
                i_limit (float):
                    The new limit to apply in Amps
        """
        self.device.command('SOURce{}:CURRent:PROTection {}'.format(self.pod_number, str(i_limit)))

    def get_i_limit_status(self):
        """Returns whether the current limit circuitry is presently engaged and limiting the current sourced by the pod"""

        return bool(int(self.device.query('SOURce{}:CURRent:PROTection:TRIPped?'.format(self.pod_number))))

    def get_voltage_range(self):
        """Returns the present voltage range of the pod in Volts"""

        return float(self.device.query('SOURce{}:VOLTage:RANGe?'.format(self.pod_number)))

    def get_voltage_ac_range(self):
        """Returns the present AC voltage range of the pod in Volts"""

        return float(self.device.query('SOURce{}:VOLTage:RANGe:AC?'.format(self.pod_number)))

    def get_voltage_dc_range(self):
        """Returns the present DC voltage range of the pod in Volts"""

        return float(self.device.query('SOURce{}:VOLTage:RANGe:DC?'.format(self.pod_number)))

    def get_voltage_autorange_status(self):
        """Returns whether automatic selection of the voltage range is enabled for this pod"""

        return bool(int(self.device.query('SOURce{}:VOLTage:RANGe:AUTO?'.format(self.pod_number))))

    def configure_voltage_range(self, autorange, max_level=None, max_ac_level=None, max_dc_level=None):
        """Sets up voltage ranging for this pod

            Args:
                autorange (bool):
                    True to enable automatic range selection. False for manual ranging.

                max_level (float):
                    The largest voltage that needs to be sourced.

                max_ac_level (float):
                    The largest AC voltage that needs to be sourced. Separate AC and DC ranges are only available on some pods.

                max_dc_level (float):
                    The largest DC voltage that needs to be sourced. Separate AC and DC ranges are only available on some pods.
        """

        if autorange:
            if max_level is not None or max_ac_level is not None or max_dc_level is not None:
                raise ValueError('If autorange is selected, a manual range cannot be specified.')

            self.device.command('SOURce{}:VOLTage:RANGe:AUTO 1'.format(self.pod_number))
        else:
            if max_level is not None:
                if max_ac_level is not None or max_dc_level is not None:
                    raise ValueError('Either a single range, or separate AC and DC ranges can be supplied, not both.')

                self.device.command('SOURce{}:VOLTage:RANGe {}'.format(self.pod_number, str(max_level)))
            else:
                if max_ac_level is not None:
                    self.device.command('SOURce{}:VOLTage:RANGe:AC {}'.format(self.pod_number, str(max_ac_level)))
                if max_dc_level is not None:
                    self.device.command('SOURce{}:VOLTage:RANGe:DC {}'.format(self.pod_number, str(max_dc_level)))

    def get_voltage_amplitude(self):
        """Returns the voltage amplitude for the pod in Volts"""

        return float(self.device.query('SOURce{}:VOLTage:LEVel:AMPLitude?'.format(self.pod_number)))

    def set_voltage_amplitude(self, amplitude):
        """Sets the voltage amplitude for the pod

            Args:
                amplitude (float):
                    The new voltage amplitude in Volts
        """

        self.device.command('SOURce{}:VOLTage:LEVel:AMPLitude {}'.format(self.pod_number, str(amplitude)))

    def get_voltage_offset(self):
        """Returns the voltage offset for the pod in Volts"""

        return float(self.device.query('SOURce{}:VOLTage:LEVel:OFFSet?'.format(self.pod_number)))

    def set_voltage_offset(self, offset):
        """Sets the voltage offset for the pod

            Args:
                offset (float):
                    The new voltage offset in Volts
        """

        self.device.command('SOURce{}:VOLTage:LEVel:OFFSet {}'.format(self.pod_number, str(offset)))

    def apply_dc_voltage(self, level, enable_output=True):
        """Apply DC voltage

            Args:
                level (float):
                    DC voltage level in Volts

                enable_output (bool):
                    Set the enable state of the pod to True
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
                    Set the enable state of the pod to True
        """

        self.set_excitation_mode('VOLTage')
        self.set_frequency(frequency)
        self.set_shape('SINusoid')
        self.set_i_amplitude(amplitude)
        self.set_i_offset(offset)

        if enable_output:
            self.enable()

    def get_voltage_limit(self):
        """Returns the voltage limit enforced by the pod in Volts"""

        return float(self.device.query('SOURce{}:VOLTage:PROTection?'.format(self.pod_number)))

    def set_voltage_limit(self, v_limit):
        """Sets the voltage limit enforced by the pod

            Args:
                v_limit (float):
                    The new limit to apply in Volts
        """

        self.device.command('SOURce{}:VOLTage:PROTection {}'.format(self.pod_number, str(v_limit)))

    def get_voltage_limit_status(self):
        """Returns whether the voltage limit circuitry is presently engaged and limiting the voltage at the output of the pod"""

        return bool(int(self.device.query('SOURce{}:VOLTage:PROTection:TRIPped?'.format(self.pod_number))))


class MeasurePod(BasePod):
    """Class for interaction with a specific measure channel of the M81 instrument"""

    def get_pod_name(self):
        """Returns the name of the pod (i.e. VMP-10)"""

        return self.device.query('SENSe{}:NAME?'.format(self.pod_number)).strip('\"')

    def get_pod_serial(self):
        """Returns the serial number of the pod (i.e. LSA1234)"""

        return self.device.query('SENSe{}:SERial?'.format(self.pod_number)).strip('\"')

    def get_hw_version(self):
        """Returns the hardware version of the pod"""

        return int(self.device.query('SENSe{}:HWVersion?'.format(self.pod_number)))

    def get_averaging_time(self):
        """Returns the averaging time of the pod in Power Line Cycles. Not relevant in Lock In mode."""

        return float(self.device.query('SENSe{}:NPLCycles?'.format(self.pod_number)))

    def set_averaging_time(self, nplc):
        """Sets the averaging time of the pod. Not relevant in Lock In mode.

            Args:
                nplc (float):
                    The new number of power line cycles to average
        """

        self.device.command('SENSe{}:NPLCycles {}'.format(self.pod_number, float(nplc)))

    def get_mode(self):
        """Returns the measurement mode of the pod. 'DC', 'AC', or 'LIA'."""

        return self.device.query('SENSe{}:MODE?'.format(self.pod_number))

    def set_mode(self, mode):
        """Sets the measurement mode of the pod

            Args:
                mode (str):
                    The new measurement mode ('DC', 'AC', or 'LIA')
        """

        self.device.command('SENSe{}:MODE {}'.format(self.pod_number, mode))

    def get_coupling(self):
        """Return input coupling of the pod. 'AC' or 'DC'."""

        return self.device.query('SENSe{}:COUPling?'.format(self.pod_number))

    def set_coupling(self, coupling):
        """Sets the input coupling of the pod

            Args:
                coupling (str):
                    The new input coupling ('AC' or 'DC')
        """

        self.device.command('SENSe{}:COUPling {}'.format(self.pod_number, coupling))

    def use_ac_coupling(self):
        """Sets the input coupling of the pod to 'AC'"""

        self.set_coupling('AC')

    def use_dc_coupling(self):
        """Sets the input coupling of the pod to 'DC'"""

        self.set_coupling('DC')

    def get_input_configuration(self):
        """Returns the input configuration of the pod. 'AB', 'A', or 'GROUND'."""
        return self.device.query('SENSe{}:CONFiguration?'.format(self.pod_number))


    def set_input_configuration(self, input_configuration):
        """Sets the input configuration of the pod

            Args:
                input_configuration (str):
                    The new input configuration ('AB', 'A', or 'GROUND')
        """

        self.device.command('SENSe{}:CONFiguration {}'.format(self.pod_number, input_configuration))

    def get_bias_voltage(self):
        """Return the bias voltage applied on the amplifier input in Volts"""

        return float(self.device.query('SENSe{}:BIAS:VOLTage:DC?'.format(self.pod_number)))

    def set_bias_voltage(self, bias_voltage):
        """Sets the bias voltage applied on the amplifier input

            Args:
                bias_voltage (float):
                    The new bias voltage in Volts
        """

        self.device.command('SENSe{}:BIAS:VOLTage:DC {}'.format(self.pod_number, str(bias_voltage)))

    def get_filter_state(self):
        """Returns whether the hardware filter is engaged"""

        return bool(int(self.device.query('SENSe{}:FILTer:STATe?'.format(self.pod_number))))

    def get_lowpass_corner_frequency(self):
        """Returns the low pass filter cuttoff frequency. 'NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', 'F3000', 'F10000', or 'F30000'."""

        return self.device.query('SENSe{}:FILTer:LPASs:FREQuency?'.format(self.pod_number))

    def get_lowpass_rolloff(self):
        """Returns the low pass filter roll-off. 'R6' or 'R12'."""

        return self.device.query('SENSe{}:FILTer:LPASs:ATTenuation?'.format(self.pod_number))

    def get_highpass_corner_frequency(self):
        """Returns the high pass filter cuttoff frequency. 'NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', 'F3000', 'F10000', or 'F30000'."""

        return self.device.query('SENSe{}:FILTer:HPASs:FREQuency?'.format(self.pod_number))

    def get_highpass_rolloff(self):
        """Returns the high pass filter roll-off. 'R6' or 'R12'."""

        return self.device.query('SENSe{}:FILTer:HPASs:ATTenuation?'.format(self.pod_number))

    def get_gain_allocation_strategy(self):
        """Returns the gain allocation strategy used for the hardware filter. 'NOISE', or 'RANGE'."""

        return self.device.query('SENSe{}:FILTer:OPTimization?'.format(self.pod_number))

    def set_gain_allocation_strategy(self, optimization_type):
        """Sets the gain allocation strategy used for the hardware filter

            Args:
                optimization_type (str):
                    The new optimization type ('NOISE', or 'RANGE')
        """

        self.device.command('SENSe{}:FILTer:OPTimization {}'.format(self.pod_number, optimization_type))

    def configure_input_lowpass_filter(self, corner_frequency, rolloff='R12'):
        """Configure the input low pass filter

            Args:
                corner_frequency (str):
                    The low pass corner frequency ('NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', 'F3000', 'F10000', or 'F30000'). F10 = 10 Hz, etc.

                rolloff (str):
                    The low pass roll-off ('R6' or 'R12'). R6 = 6 dB/Octave, R12 = 12 dB/Octave.
        """

        self.device.command('SENSe{}:FILTer:LPASs:FREQuency {}'.format(self.pod_number, corner_frequency))
        self.device.command('SENSe{}:FILTer:HPASs:ATTenuation {}'.format(self.pod_number, rolloff))
        self.device.command('SENSe{}:FILTer:STATe 1'.format(self.pod_number))

    def configure_input_highpass_filter(self, corner_frequency, rolloff='R12'):
        """Configure the input high pass filter

            Args:
                corner_frequency (str):
                    The high pass corner frequency ('NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', 'F3000', 'F10000', or 'F30000'). F10 = 10 Hz, etc.

                rolloff (str):
                    The high pass roll-off ('R6' or 'R12'). R6 = 6 dB/Octave, R12 = 12 dB/Octave.
        """

        self.device.command('SENSe{}:FILTer:HPASs:FREQuency {}'.format(self.pod_number, corner_frequency))
        self.device.command('SENSe{}:FILTer:HPASs:ATTenuation {}'.format(self.pod_number, rolloff))
        self.device.command('SENSe{}:FILTer:STATe 1'.format(self.pod_number))

    def disable_input_filters(self):
        """Disables the hardware filters"""

        self.device.command('SENSe{}:FILTer:STATe 0'.format(self.pod_number))

    def get_i_range(self):
        """Returns the current range in Amps"""

        return float(self.device.query('SENSe{}:CURRent:RANGe?'.format(self.pod_number)))

    def get_i_autorange_status(self):
        """Returns whether autoranging is enabled for the pod"""

        return bool(int(self.device.query('SENSe{}:CURRent:RANGe:AUTO?'.format(self.pod_number))))

    def configure_i_range(self, autorange, max_level):
        """Configure current ranging for the pod

            Args:
                autorange (bool):
                    True to enable real time range decisions by the pod. False for manual ranging.

                max_level (float):
                    The largest current that needs to be measured by the pod in Amps.
        """

        if autorange:
            if max_level is not None:
                raise ValueError('If autorange is selected, a manual range cannot be specified.')

            self.device.command('SENSe{}:CURRent:RANGe:AUTO 1'.format(self.pod_number))
        else:
            if max_level is not None:
                self.device.command('SENSe{}:CURRent:RANGe {}'.format(self.pod_number, str(max_level)))

    def get_voltage_range(self):
        """Returns the voltage range in Volts"""

        return float(self.device.query('SENSe{}:VOLTage:RANGe?'.format(self.pod_number)))

    def get_voltage_autorange_status(self):
        """Returns whether autoranging is enabled for the pod"""

        return bool(int(self.device.query('SENSe{}:VOLTage:RANGe:AUTO?'.format(self.pod_number))))

    def configure_voltage_range(self, autorange, max_level):
        """Configure voltage ranging for the pod

            Args:
                autorange (bool):
                    True to enable real time range decisions by the pod. False for manual ranging.

                max_level (float):
                    The largest voltage that needs to be measured by the pod in Volts.
        """

        if autorange:
            if max_level is not None:
                raise ValueError('If autorange is selected, a manual range cannot be specified.')

            self.device.command('SENSe{}:VOLTage:RANGe:AUTO 1'.format(self.pod_number))
        else:
            if max_level is not None:
                self.device.command('SENSe{}:VOLTage:RANGe {}'.format(self.pod_number, str(max_level)))

    def get_reference_source(self):
        """Returns the lock in reference source. 'S1', 'S2', 'S3', 'RIN'."""

        return self.device.query('SENSe{}:LIA:RSOurce?'.format(self.pod_number))

    def set_reference_source(self, reference_source):
        """Sets the lock in reference source

            Args:
                reference_source (str):
                    The new reference source ('S1', 'S2', 'S3', 'RIN')
        """

        self.device.command('SENSe{}:LIA:RSOurce {}'.format(self.pod_number, reference_source))

    def get_reference_harmonic(self):
        """Returns the lock in reference harmonic"""

        return int(self.device.query('SENSe{}:LIA:DHARmonic?'.format(self.pod_number)))

    def set_reference_harmonic(self, harmonic):
        """Sets the lock in reference harmonic

            Args:
                harmonic (int):
                    The new reference harmonic. 1 is the fundamental frequency, 2 is twice the fundamental frequency, etc.
        """

        self.device.command('SENSe{}:LIA:DHARmonic {}'.format(self.pod_number, str(harmonic)))

    def get_reference_phase_shift(self):
        """Returns the lock in reference phase shift in degrees"""

        return float(self.device.query('SENSe{}:LIA:DPHase?'.format(self.pod_number)))

    def set_reference_phase_shift(self, phase_shift):
        """Sets the lock in reference phase shift

            Args:
                phase_shift (float):
                    The new reference phase shift in degrees
        """
        self.device.command('SENSe{}:LIA:DPHase {}'.format(self.pod_number, str(phase_shift)))

    @requires_firmware_version('0.3')
    def auto_phase(self):
        """Executes a one time adjustment of the reference phase shift such that the present phase indication is zero. Coming in 0.3."""

        self.device.command('SENSe{}:LIA:DPHase:AUTO'.format(self.pod_number))

    def get_lock_in_time_constant(self):
        """Returns the lock in time constant in seconds"""

        return float(self.device.query('SENSe{}:LIA:TIMEconstant?'.format(self.pod_number)))

    def set_lock_in_time_constant(self, time_constant):
        """Sets the lock in time constant

            Args:
                time_constant (float):
                    The new time constant in seconds
        """
        self.device.command('SENSe{}:LIA:TIMEconstant {}'.format(self.pod_number, str(time_constant)))

    def get_lock_in_rolloff(self):
        """Returns the lock in PSD output filter roll-off for the present pod. 'R6', 'R12', 'R18' or 'R12'."""

        return self.device.query('SENSe{}:LIA:ROLLoff?'.format(self.pod_number))

    def set_lock_in_rolloff(self, rolloff):
        """Sets the lock in PSD output filter roll-off

            Args:
                rolloff (str):
                    The new PSD output filter roll-off ('R6', 'R12', 'R18' or 'R12')
        """

        self.device.command('SENSe{}:LIA:ROLLoff {}'.format(self.pod_number, rolloff))

    def get_lock_in_fir_state(self):
        """Returns the state of the lock in PSD output FIR filter"""

        return bool(int(self.device.query('SENSe{}:LIA:FIR:STATe?'.format(self.pod_number))))

    def set_lock_in_fir_state(self, state):
        """Sets the state of the lock in PSD output FIR filter

            Args:
                state (bool):
                    The new state of the PSD output FIR filter
        """

        self.device.command('SENSe{}:LIA:FIR:STATe {}'.format(self.pod_number, str(int(state))))

    def enable_lock_in_fir(self):
        """Sets the state of the lock in PSD output FIR filter to True."""

        self.set_lock_in_fir_state(True)

    def disable_lock_in_fir(self):
        """Sets the state of the lock in PSD output FIR filter to False."""

        self.set_lock_in_fir_state(False)

    def setup_dc_measurement(self, nplc=1):
        """Setup the pod for DC measurement

            Args:
                nplc (float):
                    The new number of power line cycles to average
        """

        self.set_mode('DC')
        self.set_averaging_time(nplc)

    def setup_ac_measurement(self, nplc=1):
        """Setup the pod for DC measurement

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
        """Setup the pod for Lock In measurment

            Args:
                reference_source (str):
                    Lock in reference source ('S1', 'S2', 'S3', 'RIN')

                time_constant (float):
                    Time constant in seconds

                rolloff (str):
                    Lock in PSD output filter roll-off ('R6', 'R12', 'R18' or 'R12')

                reference_phase_shift (float):
                    Lock in reference phase shift in degrees

                reference_harmonic (int):
                    Lock in reference harmonic. 1 is the fundamental frequency, 2 is twice the fundamental frequency, etc.

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

    def get_dc(self):
        """Returns the present DC indication in pod units"""

        return float(self.device.query('FETCh:SENSe{}:DC?'.format(self.pod_number)))

    def get_rms(self):
        """Returns the present RMS indication in pod units"""

        return float(self.device.query('FETCh:SENSe{}:RMS?'.format(self.pod_number)))

    def get_peak_to_peak(self):
        """Returns the present peak to peak indication in pod units"""

        return float(self.device.query('FETCh:SENSe{}:PTPeak?'.format(self.pod_number)))

    def get_positive_peak(self):
        """Returns the present positive peak indication in pod units"""

        return float(self.device.query('FETCh:SENSe{}:PPEak?'.format(self.pod_number)))

    def get_negative_peak(self):
        """Returns the present negative peak indication in pod units"""

        return float(self.device.query('FETCh:SENSe{}:NPEak?'.format(self.pod_number)))

    def get_lock_in_x(self):
        """Returns the present X indication from the lock in"""

        return float(self.device.query('FETCh:SENSe{}:LIA:X?'.format(self.pod_number)))

    def get_lock_in_y(self):
        """Returns the present Y indication from the lock in"""

        return float(self.device.query('FETCh:SENSe{}:LIA:Y?'.format(self.pod_number)))

    def get_lock_in_magnitude(self):
        """Returns the present magnitude indication from the lock in"""

        return float(self.device.query('FETCh:SENSe{}:LIA:R?'.format(self.pod_number)))

    def get_lock_in_angle(self):
        """Returns the present angle indication from the lock in"""

        return float(self.device.query('FETCh:SENSe{}:LIA:THETa?'.format(self.pod_number)))

    def get_lock_in_frequency(self):
        """Returns the present detected frequency from the Phase Locked Loop (PLL)"""

        return float(self.device.query('FETCh:SENSe{}:LIA:FREQuency?'.format(self.pod_number)))

    def get_pll_lock_status(self):
        """Returns the present lock status of the PLL. True if locked, False if unlocked."""

        return bool(int(self.device.query('FETCh:SENSe{}:LIA:LOCK?'.format(self.pod_number))))

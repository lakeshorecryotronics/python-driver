"""Implements functionality unique to the Lake Shore M81."""

import struct
from base64 import b64decode
from threading import Lock

from lakeshore.xip_instrument import XIPInstrument, XIPInstrumentException, RegisterBase


class SSMSystemQuestionableRegister(RegisterBase):
    """Class object representing the questionable status register"""

    bit_names = [
        "s1_summary",
        "s2_summary",
        "s3_summary",
        "m1_summary",
        "m2_summary",
        "m3_summary",
        "critical_startup_error",
        "critical_runtime_error",
        "heartbeat",
        "calibration",
        "data_stream_overflow"
    ]

    # pylint: disable=too-many-arguments
    def __init__(self,
                 s1_summary,
                 s2_summary,
                 s3_summary,
                 m1_summary,
                 m2_summary,
                 m3_summary,
                 critical_startup_error,
                 critical_runtime_error,
                 heartbeat,
                 calibration,
                 data_stream_overflow):
        self.s1_summary = s1_summary
        self.s2_summary = s2_summary
        self.s3_summary = s3_summary
        self.m1_summary = m1_summary
        self.m2_summary = m2_summary
        self.m3_summary = m3_summary
        self.critical_startup_error = critical_startup_error
        self.critical_runtime_error = critical_runtime_error
        self.heartbeat = heartbeat
        self.calibration = calibration
        self.data_stream_overflow = data_stream_overflow


class SSMSystemModuleQuestionableRegister(RegisterBase):
    """Class object representing the questionable status register of a module"""

    bit_names = [
        "read_error",
        "unrecognized_pod_error",
        "port_direction_error",
        "factory_calibration_failure",
        "self_calibration_failure"
    ]

    def __init__(
            self,
            read_error=False,
            unrecognized_pod_error=False,
            port_direction_error=False,
            factory_calibration_failure=False,
            self_calibration_failure=False):
        self.read_error = read_error
        self.unrecognized_pod_error = unrecognized_pod_error
        self.port_direction_error = port_direction_error
        self.factory_calibration_failure = factory_calibration_failure
        self.self_calibration_failure = self_calibration_failure


class SSMSystemOperationRegister(RegisterBase):
    """Class object representing the operation status register"""

    bit_names = [
        "s1_summary",
        "s2_summary",
        "s3_summary",
        "m1_summary",
        "m2_summary",
        "m3_summary",
        "data_stream_in_progress"
    ]

    def __init__(self,
                 s1_summary,
                 s2_summary,
                 s3_summary,
                 m1_summary,
                 m2_summary,
                 m3_summary,
                 data_stream_in_progress):
        self.s1_summary = s1_summary
        self.s2_summary = s2_summary
        self.s3_summary = s3_summary
        self.m1_summary = m1_summary
        self.m2_summary = m2_summary
        self.m3_summary = m3_summary
        self.data_stream_in_progress = data_stream_in_progress


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

        self.operation_register = SSMSystemOperationRegister
        self.questionable_register = SSMSystemQuestionableRegister

        # Instantiate modules
        self.source_modules = [SourceModule(i + 1, self) for i in range(self.get_num_source_channels())]
        self.measure_modules = [MeasureModule(i + 1, self) for i in range(self.get_num_measure_channels())]

        self.stream_lock = Lock()

    def get_num_measure_channels(self):
        """Returns the number of measure channels supported by the instrument"""

        return int(self.query('SENSe:NCHannels?'))

    def get_num_source_channels(self):
        """Returns the number of source channels supported by the instrument"""

        return int(self.query('SOURce:NCHannels?'))

    def get_source_module(self, port_number):
        """Returns a SourceModule instance for the given port number"""

        try:
            return self.source_modules[port_number - 1]
        except IndexError:
            raise IndexError('Invalid port number. Must be between 1 and {}'.format(self.get_num_source_channels()))

    def get_source_pod(self, port_number):
        """alias of get_source_module"""
        return self.get_source_module(port_number)

    def get_source_module_by_name(self, module_name):
        """Return the SourceModule instance that matches the specified name"""

        return self._locate_module_by_name(module_name, self.source_modules)

    def get_measure_module(self, port_number):
        """Returns a MeasureModule instance for the given port number"""

        try:
            return self.measure_modules[port_number - 1]
        except IndexError:
            raise IndexError('Invalid port number. Must be between 1 and {}'.format(self.get_num_measure_channels()))

    def get_measure_pod(self, port_number):
        """alias of get_measure_module"""
        return self.get_measure_module(port_number)

    def get_measure_module_by_name(self, module_name):
        """Return the MeasureModule instance that matches the specified name"""

        return self._locate_module_by_name(module_name, self.measure_modules)

    @staticmethod
    def _locate_module_by_name(module_name, set_of_modules):
        module_names = []
        for module in set_of_modules:
            try:
                module_names.append(module.get_name())
            except XIPInstrumentException as exception:
                if '-241,"Hardware missing;' not in str(exception):
                    raise
                module_names.append(None)

        num_matches = len([name for name in module_names if name == module_name])

        if num_matches < 1:
            raise XIPInstrumentException('No module was found with the name {}.'.format(module_name))
        if num_matches > 1:
            raise XIPInstrumentException('Module name conflict: more than one module is named {}.'.format(module_name))

        return set_of_modules[module_names.index(module_name)]

    data_source_types = {
        'RTIMe': float,
        'SAMPlitude': float,
        'SOFFset': float,
        'SFRequency': float,
        'SRANge': float,
        'SVLimit': lambda s: bool(int(s)),
        'SILimit': lambda s: bool(int(s)),
        'MDC': float,
        'MRMs': float,
        'MPPeak': float,
        'MNPeak': float,
        'MPTPeak': float,
        'MX': float,
        'MY': float,
        'MR': float,
        'MTHeta': float,
        'MRANge': float,
        'MOVerload': lambda s: bool(int(s)),
        'MSETtling': lambda s: bool(int(s)),
        'MUNLock': lambda s: bool(int(s)),
        'MRFRequency': float,
        'GPIStates': int,
        'GPOStates': int,
    }

    data_source_lookup = {}
    for mnemonic, channel_index in data_source_types.items():
        short_form = ''.join(c for c in mnemonic if not c.islower())
        data_source_lookup[mnemonic.upper()] = channel_index
        data_source_lookup[short_form.upper()] = channel_index

    def get_multiple(self, *data_sources):
        """Gets a list of values corresponding to the input data sources.

            Args:
                data_sources (str, int): Variable length list of pairs of (DATASOURCE_MNEMONIC, CHANNEL_INDEX).

            Returns:
                Tuple of values corresponding to the given data sources
        """

        elements = ','.join('{},{}'.format(mnemonic, index) for (mnemonic, index) in data_sources)
        response_values_with_indices = enumerate(self.query('FETCh? {}'.format(elements)).split(','))

        return tuple((self.data_source_lookup[data_sources[i][0].upper()])(value) for (i, value) in response_values_with_indices)

    def stream_data(self, rate, num_points, *data_sources):
        r"""Generator object to stream data from the instrument.

            Args:
                rate (int): Desired transfer rate in points/sec.
                num_points (int): Number of points to return. None to stream indefinitely.
                data_sources (str, int): Variable length list of pairs of (DATASOURCE_MNEMONIC, CHANNEL_INDEX).

            Yields:
                A single row of stream data as a tuple
        """

        with self.stream_lock:
            self.command('TRACe:RESEt')
            self._configure_stream_elements(data_sources)
            self.command('TRACe:FORMat:ENCOding B64')
            self.command('TRACe:RATE {}'.format(rate))

            bytes_per_row = int(self.query('TRACe:FORMat:ENCOding:B64:BCOunt?'))
            binary_format = '<' + self.query('TRACe:FORMat:ENCOding:B64:BFORmat?').strip('\"')

            if num_points is not None:
                self.command('TRACe:STARt {}'.format(num_points))
            else:
                self.command('TRACe:STARt')

            num_collected = 0
            while num_points is None or num_collected < num_points:
                b64_string = ''
                while not b64_string:
                    b64_string = self.query('TRACe:DATA:ALL?', check_errors=False)

                new_bytes = b64decode(b64_string)
                rows = [new_bytes[i:i + bytes_per_row] for i in range(0, len(new_bytes), bytes_per_row)]

                for row in rows:
                    data = struct.unpack(binary_format, row)
                    num_collected += 1

                    yield data

            overflow_occurred = bool(int(self.query('TRACe:DATA:OVERflow?', check_errors=True)))

            if overflow_occurred:
                raise XIPInstrumentException('Data loss occurred during this data stream.')

    def get_data(self, rate, num_points, *data_sources):
        r"""Like stream_data, but returns a list.

            Args:
                rate (int): Desired transfer rate in points/sec.
                num_points (int): Number of points to return.
                data_sources (str, int): Variable length list of pairs of (DATASOURCE_MNEMONIC, CHANNEL_INDEX).

            Returns:
                All available stream data as a list of tuples
        """

        return list(self.stream_data(rate, num_points, *data_sources))

    def log_data_to_csv_file(self, rate, num_points, file, *data_sources, **kwargs):
        """Like stream_data, but logs directly to a CSV file.

            Args:
                rate (int): Desired transfer rate in points/sec.
                file (IO): File to log to.
                num_points (int): Number of points to log.
                data_sources (str, int): Pairs of (DATASOURCE_MNEMONIC, CHANNEL_INDEX).
                write_header (bool): If true, a header row is written with column names.
        """
        write_header = kwargs.pop('write_header', True)

        if write_header:
            self._configure_stream_elements(data_sources)
            header = self.query('TRACe:FORMat:HEADer?').strip('\"')
            file.write(header + '\n')

        for row in self.stream_data(rate, num_points, *data_sources):
            file.write(','.join(str(x) for x in row) + '\n')

    def _configure_stream_elements(self, data_sources):
        elements = ','.join('{},{}'.format(mnemonic, index) for (mnemonic, index) in data_sources)
        self.command('TRACe:FORMat:ELEMents {}'.format(elements))

    def get_ref_in_edge(self):
        """Returns the active edge of the reference input. 'RISing' or 'FALLing'."""

        return self.query('INPut:REFerence:EDGe?')

    def set_ref_in_edge(self, edge):
        """Sets the active edge of the reference input

            Args:
                edge (str):
                    The new active edge ('RISing', or 'FALLing')
        """

        self.command('INPut:REFerence:EDGe {}'.format(edge))

    def get_ref_out_source(self):
        """Returns the channel used for the reference output. 'S1', 'S2', or 'S3'."""

        return self.query('OUTPut:REFerence:SOURce?')

    def set_ref_out_source(self, ref_out_source):
        """Sets the channel used for the reference output.

            Args:
                ref_out_source (str):
                    The new reference out source ('S1', 'S2', or 'S3')
        """

        self.command('OUTPut:REFerence:SOURce {}'.format(ref_out_source))

    def get_ref_out_state(self):
        """Returns the enable state of reference out"""

        return bool(int(self.query('OUTPut:REFerence:STATe?')))

    def set_ref_out_state(self, ref_out_state):
        """Sets the enable state of reference out

            Args:
                ref_out_state (bool):
                    The new reference out state (True to enable reference out, False to disable reference out)
        """

        self.command('OUTPut:REFerence:STATe {}'.format(str(int(ref_out_state))))

    def enable_ref_out(self):
        """Sets the enable state of reference out to True"""

        self.set_ref_out_state(True)

    def disable_ref_out(self):
        """Sets the enable state of reference out to False"""

        self.set_ref_out_state(False)

    def configure_ref_out(self, ref_out_source, ref_out_state=True):
        """Configure the reference output

            Args:
                ref_out_source (str):
                    The new reference out source ('S1', 'S2', or 'S3')

                ref_out_state (bool):
                    The new reference out state (True to enable reference out, False to disable reference out)
        """

        self.set_ref_out_source(ref_out_source)
        self.set_ref_out_state(ref_out_state)

    def get_mon_out_mode(self):
        """Returns the channel used for the monitor output. 'M1', 'M2', 'M3', or 'MANUAL'."""

        return self.query('OUTPut:MONitor:MODe?')

    def set_mon_out_mode(self, mon_out_source):
        """Sets the channel used for the monitor output.

            Args:
                mon_out_source (str):
                    The new monitor out source ('M1', 'M2', 'M3', or 'MANUAL')
        """

        self.command('OUTPut:MONitor:MODe {}'.format(mon_out_source))

    def get_mon_out_state(self):
        """Returns the enable state of monitor out"""

        return bool(int(self.query('OUTPut:MONitor:STATe?')))

    def set_mon_out_state(self, mon_out_state):
        """Sets the enable state of monitor out

            Args:
                mon_out_state (bool):
                    The new monitor out state (True to enable monitor out, False to disable monitor out)
        """

        self.command('OUTPut:MONitor:STATe {}'.format(str(int(mon_out_state))))

    def enable_mon_out(self):
        """Sets the enable state of monitor out to True"""

        self.set_mon_out_state(True)

    def disable_mon_out(self):
        """Sets the enable state of monitor out to False"""

        self.set_mon_out_state(False)

    def configure_mon_out(self, mon_out_source, mon_out_state=True):
        """Configure the monitor output

            Args:
                mon_out_source (str):
                    The new monitor out source ('M1', 'M2', or 'M3')

                mon_out_state (bool):
                    The new monitor out state (True to enable monitor out, False to disable monitor out)
        """

        self.set_mon_out_mode(mon_out_source)
        self.set_mon_out_state(mon_out_state)

    def get_head_self_cal_status(self):
        """Returns the status of the last head self calibration"""

        self.command('CALibration:SCALibration:STATus?')

    def run_head_self_calibration(self):
        """"Runs a self calibration for the head"""

        self.command('CALibration:SCALibration:RUN')

    def reset_head_self_calibration(self):
        """"Restore the factory self calibration"""

        self.command('CALibration:SCALibration:RESet')

    def set_mon_out_manual_level(self, manual_level):
        """Set the manual level of monitor out when the mode is MANUAL

            Args:
                manual_level (float):
                    The new monitor out manual level
        """

        self.command('OUTPut:MONitor:MLEVel {}'.format(str(manual_level)))

    def get_mon_out_manual_level(self):
        """Returns the manual level of monitor out"""

        return float(self.query('OUTPut:MONitor:MLEVel?'))

    def configure_mon_out_manual_mode(self, manual_level, mon_out_state=True):
        """Configures the monitor output for manual mode

            Args:
                manual_level (float):
                    The new monitor out manual level

                mon_out_state (bool):
                    The new monitor out state (True to enable monitor out, False to disable monitor out)
        """

        self.set_mon_out_manual_level(manual_level)
        self.set_mon_out_mode('MANUAL')
        self.set_mon_out_state(mon_out_state)


class BaseModule:
    """Class for interaction with a specific channel, not specific to source or measure"""

    def __init__(self, module_number, device):
        self.module_number = module_number
        self.device = device


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
        """Sets the excitation mode of the module to 'CURRENT'"""

        self.set_excitation_mode('VOLTage')

    def get_shape(self):
        """Returns the signal shape of the module. 'DC' or 'SINUSOID'."""

        return self.device.query('SOURce{}:FUNCtion:SHAPe?'.format(self.module_number))

    def set_shape(self, shape):
        """Sets the signal shape of the module

            Args:
                shape (str):
                    The new signal shape ('DC' or 'SINUSOID')
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


class MeasureModule(BaseModule):
    """Class for interaction with a specific measure channel of the M81 instrument"""

    def get_name(self):
        """Returns the user-settable name of the module"""

        return self.device.query('SENSe{}:NAME?'.format(self.module_number)).strip('\"')

    def set_name(self, new_name):
        """Set the name of the module"""

        self.device.command('SOURce{}:NAME "{}"'.format(self.module_number, new_name))

    def get_model(self):
        """Returns the model of the module (i.e. VM-10)"""

        return self.device.query('SENSe{}:MODel?'.format(self.module_number)).strip('\"')

    def get_serial(self):
        """Returns the serial number of the module (i.e. LSA1234)"""

        return self.device.query('SENSe{}:SERial?'.format(self.module_number)).strip('\"')

    def get_hw_version(self):
        """Returns the hardware version of the module"""

        return int(self.device.query('SENSe{}:HWVersion?'.format(self.module_number)))

    def get_self_cal_status(self):
        """Returns the status of the last self calibration of the module"""

        return self.device.query('SENSe{}:SCALibration:STATus?'.format(self.module_number))

    def run_self_cal(self):
        """Run a self calibration for the module"""

        self.device.command('SENSe{}:SCALibration:RUN'.format(self.module_number))

    def reset_self_cal(self):
        """Restore factory self calibration for the module"""

        self.device.command('SENSe{}:SCALibration:RESet'.format(self.module_number))

    def get_averaging_time(self):
        """Returns the averaging time of the module in Power Line Cycles. Not relevant in Lock In mode."""

        return float(self.device.query('SENSe{}:NPLCycles?'.format(self.module_number)))

    def set_averaging_time(self, nplc):
        """Sets the averaging time of the module. Not relevant in Lock In mode.

            Args:
                nplc (float):
                    The new number of power line cycles to average
        """

        self.device.command('SENSe{}:NPLCycles {}'.format(self.module_number, float(nplc)))

    def get_mode(self):
        """Returns the measurement mode of the module. 'DC', 'AC', or 'LIA'."""

        return self.device.query('SENSe{}:MODE?'.format(self.module_number))

    def set_mode(self, mode):
        """Sets the measurement mode of the module

            Args:
                mode (str):
                    The new measurement mode ('DC', 'AC', or 'LIA')
        """

        self.device.command('SENSe{}:MODE {}'.format(self.module_number, mode))

    def get_coupling(self):
        """Return input coupling of the module. 'AC' or 'DC'."""

        return self.device.query('SENSe{}:COUPling?'.format(self.module_number))

    def set_coupling(self, coupling):
        """Sets the input coupling of the module

            Args:
                coupling (str):
                    The new input coupling ('AC' or 'DC')
        """

        self.device.command('SENSe{}:COUPling {}'.format(self.module_number, coupling))

    def use_ac_coupling(self):
        """Sets the input coupling of the module to 'AC'"""

        self.set_coupling('AC')

    def use_dc_coupling(self):
        """Sets the input coupling of the module to 'DC'"""

        self.set_coupling('DC')

    def get_input_configuration(self):
        """Returns the input configuration of the module. 'AB', 'A', or 'GROUND'."""
        return self.device.query('SENSe{}:CONFiguration?'.format(self.module_number))

    def set_input_configuration(self, input_configuration):
        """Sets the input configuration of the module

            Args:
                input_configuration (str):
                    The new input configuration ('AB', 'A', or 'GROUND')
        """

        self.device.command('SENSe{}:CONFiguration {}'.format(self.module_number, input_configuration))

    def get_bias_voltage(self):
        """Return the bias voltage applied on the amplifier input in Volts"""

        return float(self.device.query('SENSe{}:BIAS:VOLTage:DC?'.format(self.module_number)))

    def set_bias_voltage(self, bias_voltage):
        """Sets the bias voltage applied on the amplifier input

            Args:
                bias_voltage (float):
                    The new bias voltage in Volts
        """

        self.device.command('SENSe{}:BIAS:VOLTage:DC {}'.format(self.module_number, str(bias_voltage)))

    def get_filter_state(self):
        """Returns whether the hardware filter is engaged"""

        return bool(int(self.device.query('SENSe{}:FILTer:STATe?'.format(self.module_number))))

    def get_lowpass_corner_frequency(self):
        """Returns the low pass filter cuttoff frequency. 'NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', 'F3000', 'F10000', or 'F30000'."""

        return self.device.query('SENSe{}:FILTer:LPASs:FREQuency?'.format(self.module_number))

    def get_lowpass_rolloff(self):
        """Returns the low pass filter roll-off. 'R6' or 'R12'."""

        return self.device.query('SENSe{}:FILTer:LPASs:ATTenuation?'.format(self.module_number))

    def get_highpass_corner_frequency(self):
        """Returns the high pass filter cuttoff frequency. 'NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', 'F3000', 'F10000', or 'F30000'."""

        return self.device.query('SENSe{}:FILTer:HPASs:FREQuency?'.format(self.module_number))

    def get_highpass_rolloff(self):
        """Returns the high pass filter roll-off. 'R6' or 'R12'."""

        return self.device.query('SENSe{}:FILTer:HPASs:ATTenuation?'.format(self.module_number))

    def get_gain_allocation_strategy(self):
        """Returns the gain allocation strategy used for the hardware filter. 'NOISE', or 'RESERVE'."""

        return self.device.query('SENSe{}:FILTer:OPTimization?'.format(self.module_number))

    def set_gain_allocation_strategy(self, optimization_type):
        """Sets the gain allocation strategy used for the hardware filter

            Args:
                optimization_type (str):
                    The new optimization type ('NOISE', or 'RESERVE')
        """

        self.device.command('SENSe{}:FILTer:OPTimization {}'.format(self.module_number, optimization_type))

    def configure_input_lowpass_filter(self, corner_frequency, rolloff='R12'):
        """Configure the input low pass filter

            Args:
                corner_frequency (str):
                    The low pass corner frequency ('NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', 'F3000', 'F10000', or 'F30000'). F10 = 10 Hz, etc.

                rolloff (str):
                    The low pass roll-off ('R6' or 'R12'). R6 = 6 dB/Octave, R12 = 12 dB/Octave.
        """

        self.device.command('SENSe{}:FILTer:LPASs:FREQuency {}'.format(self.module_number, corner_frequency))
        self.device.command('SENSe{}:FILTer:LPASs:ATTenuation {}'.format(self.module_number, rolloff))
        self.device.command('SENSe{}:FILTer:STATe 1'.format(self.module_number))

    def configure_input_highpass_filter(self, corner_frequency, rolloff='R12'):
        """Configure the input high pass filter

            Args:
                corner_frequency (str):
                    The high pass corner frequency ('NONE', 'F10', 'F30', 'F100', 'F300', 'F1000', 'F3000', 'F10000', or 'F30000'). F10 = 10 Hz, etc.

                rolloff (str):
                    The high pass roll-off ('R6' or 'R12'). R6 = 6 dB/Octave, R12 = 12 dB/Octave.
        """

        self.device.command('SENSe{}:FILTer:HPASs:FREQuency {}'.format(self.module_number, corner_frequency))
        self.device.command('SENSe{}:FILTer:HPASs:ATTenuation {}'.format(self.module_number, rolloff))
        self.device.command('SENSe{}:FILTer:STATe 1'.format(self.module_number))

    def disable_input_filters(self):
        """Disables the hardware filters"""

        self.device.command('SENSe{}:FILTer:STATe 0'.format(self.module_number))

    def get_i_range(self):
        """Returns the current range in Amps"""

        return float(self.device.query('SENSe{}:CURRent:RANGe?'.format(self.module_number)))

    def get_i_autorange_status(self):
        """Returns whether autoranging is enabled for the module"""

        return bool(int(self.device.query('SENSe{}:CURRent:RANGe:AUTO?'.format(self.module_number))))

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

            self.device.command('SENSe{}:CURRent:RANGe:AUTO 1'.format(self.module_number))
        else:
            if max_level is not None:
                self.device.command('SENSe{}:CURRent:RANGe {}'.format(self.module_number, str(max_level)))

    def get_voltage_range(self):
        """Returns the voltage range in Volts"""

        return float(self.device.query('SENSe{}:VOLTage:RANGe?'.format(self.module_number)))

    def get_voltage_autorange_status(self):
        """Returns whether autoranging is enabled for the module"""

        return bool(int(self.device.query('SENSe{}:VOLTage:RANGe:AUTO?'.format(self.module_number))))

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

            self.device.command('SENSe{}:VOLTage:RANGe:AUTO 1'.format(self.module_number))
        else:
            if max_level is not None:
                self.device.command('SENSe{}:VOLTage:RANGe {}'.format(self.module_number, str(max_level)))

    def get_reference_source(self):
        """Returns the lock in reference source. 'S1', 'S2', 'S3', 'RIN'."""

        return self.device.query('SENSe{}:LIA:RSOurce?'.format(self.module_number))

    def set_reference_source(self, reference_source):
        """Sets the lock in reference source

            Args:
                reference_source (str):
                    The new reference source ('S1', 'S2', 'S3', 'RIN')
        """

        self.device.command('SENSe{}:LIA:RSOurce {}'.format(self.module_number, reference_source))

    def get_reference_harmonic(self):
        """Returns the lock in reference harmonic"""

        return int(self.device.query('SENSe{}:LIA:DHARmonic?'.format(self.module_number)))

    def set_reference_harmonic(self, harmonic):
        """Sets the lock in reference harmonic

            Args:
                harmonic (int):
                    The new reference harmonic. 1 is the fundamental frequency, 2 is twice the fundamental frequency, etc.
        """

        self.device.command('SENSe{}:LIA:DHARmonic {}'.format(self.module_number, str(harmonic)))

    def get_reference_phase_shift(self):
        """Returns the lock in reference phase shift in degrees"""

        return float(self.device.query('SENSe{}:LIA:DPHase?'.format(self.module_number)))

    def set_reference_phase_shift(self, phase_shift):
        """Sets the lock in reference phase shift

            Args:
                phase_shift (float):
                    The new reference phase shift in degrees
        """
        self.device.command('SENSe{}:LIA:DPHase {}'.format(self.module_number, str(phase_shift)))

    def auto_phase(self):
        """Executes a one time adjustment of the reference phase shift such that the present phase indication is zero. Coming in 0.3."""

        self.device.command('SENSe{}:LIA:DPHase:AUTO'.format(self.module_number))

    def get_lock_in_time_constant(self):
        """Returns the lock in time constant in seconds"""

        return float(self.device.query('SENSe{}:LIA:TIMEconstant?'.format(self.module_number)))

    def set_lock_in_time_constant(self, time_constant):
        """Sets the lock in time constant

            Args:
                time_constant (float):
                    The new time constant in seconds
        """
        self.device.command('SENSe{}:LIA:TIMEconstant {}'.format(self.module_number, str(time_constant)))

    def get_lock_in_rolloff(self):
        """Returns the lock in PSD output filter roll-off for the present module. 'R6', 'R12', 'R18' or 'R24'."""

        return self.device.query('SENSe{}:LIA:ROLLoff?'.format(self.module_number))

    def set_lock_in_rolloff(self, rolloff):
        """Sets the lock in PSD output filter roll-off

            Args:
                rolloff (str):
                    The new PSD output filter roll-off ('R6', 'R12', 'R18' or 'R24')
        """

        self.device.command('SENSe{}:LIA:ROLLoff {}'.format(self.module_number, rolloff))

    def get_lock_in_fir_state(self):
        """Returns the state of the lock in PSD output FIR filter"""

        return bool(int(self.device.query('SENSe{}:LIA:FIR:STATe?'.format(self.module_number))))

    def set_lock_in_fir_state(self, state):
        """Sets the state of the lock in PSD output FIR filter

            Args:
                state (bool):
                    The new state of the PSD output FIR filter
        """

        self.device.command('SENSe{}:LIA:FIR:STATe {}'.format(self.module_number, str(int(state))))

    def enable_lock_in_fir(self):
        """Sets the state of the lock in PSD output FIR filter to True."""

        self.set_lock_in_fir_state(True)

    def disable_lock_in_fir(self):
        """Sets the state of the lock in PSD output FIR filter to False."""

        self.set_lock_in_fir_state(False)

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
        """Setup the module for Lock In measurment

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

    def get_multiple(self, *data_sources):
        r"""Gets a list of values corresponding to the input data sources for this module.

            Args:
                data_sources (str): Variable length list of DATASOURCE_MNEMONIC.

            Returns:
                Tuple of values corresponding to the given data sources for this module
        """

        elements = [(data_source, self.module_number) for data_source in data_sources]
        return self.device.get_multiple(*elements)

    def get_dc(self):
        """Returns the present DC indication in module units"""

        return float(self.device.query('FETCh:SENSe{}:DC?'.format(self.module_number)))

    def get_rms(self):
        """Returns the present RMS indication in module units"""

        return float(self.device.query('FETCh:SENSe{}:RMS?'.format(self.module_number)))

    def get_peak_to_peak(self):
        """Returns the present peak to peak indication in module units"""

        return float(self.device.query('FETCh:SENSe{}:PTPeak?'.format(self.module_number)))

    def get_positive_peak(self):
        """Returns the present positive peak indication in module units"""

        return float(self.device.query('FETCh:SENSe{}:PPEak?'.format(self.module_number)))

    def get_negative_peak(self):
        """Returns the present negative peak indication in module units"""

        return float(self.device.query('FETCh:SENSe{}:NPEak?'.format(self.module_number)))

    def get_lock_in_x(self):
        """Returns the present X indication from the lock in"""

        return float(self.device.query('FETCh:SENSe{}:LIA:X?'.format(self.module_number)))

    def get_lock_in_y(self):
        """Returns the present Y indication from the lock in"""

        return float(self.device.query('FETCh:SENSe{}:LIA:Y?'.format(self.module_number)))

    def get_lock_in_r(self):
        """Returns the present magnitude indication from the lock in"""

        return float(self.device.query('FETCh:SENSe{}:LIA:R?'.format(self.module_number)))

    def get_lock_in_theta(self):
        """Returns the present angle indication from the lock in"""

        return float(self.device.query('FETCh:SENSe{}:LIA:THETa?'.format(self.module_number)))

    def get_lock_in_frequency(self):
        """Returns the present detected frequency from the Phase Locked Loop (PLL)"""

        return float(self.device.query('FETCh:SENSe{}:LIA:FREQuency?'.format(self.module_number)))

    def get_pll_lock_status(self):
        """Returns the present lock status of the PLL. True if locked, False if unlocked."""

        return bool(int(self.device.query('FETCh:SENSe{}:LIA:LOCK?'.format(self.module_number))))

    def get_present_questionable_status(self):
        """Returns the names of the questionable status register bits and their values"""

        response = self.device.query('STATus:QUEStionable:SENSe{}:CONDition?'.format(self.module_number), check_errors=False)
        status_register = SSMSystemModuleQuestionableRegister.from_integer(response)

        return status_register

    def get_questionable_events(self):
        """Returns the names of questionable event status register bits that are currently high.
        The event register is latching and values are reset when queried."""

        response = self.device.query('STATus:QUEStionable:SENSe{}:EVENt?'.format(self.module_number), check_errors=False)
        status_register = SSMSystemModuleQuestionableRegister.from_integer(response)

        return status_register

    def get_questionable_event_enable_mask(self):
        """Returns the names of the questionable event enable register bits and their values.
        These values determine which questionable bits propagate to the questionable event register."""

        response = self.device.query('STATus:QUEStionable:SENSe{}:ENABle?'.format(self.module_number), check_errors=False)
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
        self.device.command('STATus:QUEStionable:SENSe{}:ENABle {}'.format(self.module_number, integer_representation), check_errors=False)

    def get_present_operation_status(self):
        """Returns the names of the operation status register bits and their values"""

        response = self.device.query('STATus:OPERation:SENSe{}:CONDition?'.format(self.module_number), check_errors=False)
        status_register = SSMSystemMeasureModuleOperationRegister.from_integer(response)

        return status_register

    def get_operation_events(self):
        """Returns the names of operation event status register bits that are currently high.
        The event register is latching and values are reset when queried."""

        response = self.device.query('STATus:OPERation:SENSe{}:EVENt?'.format(self.module_number), check_errors=False)
        status_register = SSMSystemMeasureModuleOperationRegister.from_integer(response)

        return status_register

    def get_operation_event_enable_mask(self):
        """Returns the names of the operation event enable register bits and their values.
        These values determine which operation bits propagate to the operation event register."""

        response = self.device.query('STATus:OPERation:SENSe{}:ENABle?'.format(self.module_number), check_errors=False)
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
        self.device.command('STATus:OPERation:SENSe{}:ENABle {}'.format(self.module_number, integer_representation), check_errors=False)

    def get_identify_state(self):
        """Returns the identification state for the given pod."""
        response = bool(int(self.device.query('SENSe{}:IDENtify?'.format(self.module_number), check_errors=False)))
        return response

    def set_identify_state(self, state):
        """Returns the identification state for the given pod.

            Args:
                state (bool):
                    The desired state for the LED, 1 for identify, 0 for normal state
        """
        self.device.command('SENSe{}:IDENtify {}'.format(self.module_number, int(state)), check_errors=False)

from datetime import datetime
from tests.utils import TestWithFakeSSMS, TestWithFakeSSMSSourceModule, TestWithFakeSSMSMeasureModule
from lakeshore import ssm_system, ssm_measure_module, ssm_source_module, ssm_base_module
from base64 import b64encode
from struct import pack
from os import remove
import sys


class TestSSMSSYSTEM(TestWithFakeSSMS):
    def test_get_num_measure_channels(self):
        self.fake_connection.setup_response('3;No error')
        response = self.dut.get_num_measure_channels()
        self.assertEqual(response, 3)
        self.assertIn('SENSe:NCHannels?', self.fake_connection.get_outgoing_message())

    def test_get_num_source_channels(self):
        self.fake_connection.setup_response('3;No error')
        response = self.dut.get_num_source_channels()
        self.assertEqual(response, 3)
        self.assertIn('SOURce:NCHannels?', self.fake_connection.get_outgoing_message())

    def test_get_source_module_valid_port(self):
        self.fake_connection.setup_response('No error')
        response = self.dut.get_source_module(1)
        self.assertTrue(isinstance(response, ssm_system.SourceModule))

    def test_get_source_module_invalid_port(self):
        self.fake_connection.setup_response('3;No error')
        with self.assertRaisesRegex(IndexError, 'Invalid port number. Must be between 1 and 3'):
            self.dut.get_source_module(5)

    def test_get_source_pod(self):
        self.fake_connection.setup_response('No error')
        response = self.dut.get_source_pod(1)
        self.assertTrue(isinstance(response, ssm_system.SourceModule))

    def test_get_source_module_by_name(self):
        self.fake_connection.setup_response('Module_name1;No error')
        self.fake_connection.setup_response('Module_name2;No error')
        self.fake_connection.setup_response('Module_name3;No error')
        response = self.dut.get_source_module_by_name('Module_name1')
        self.assertTrue(isinstance(response, ssm_system.SourceModule))

    def test_get_measure_module(self):
        self.fake_connection.setup_response('No error')
        response = self.dut.get_measure_module(1)
        self.assertTrue(isinstance(response, ssm_system.MeasureModule))

    def test_get_measure_pod(self):
        self.fake_connection.setup_response('No error')

    def test_get_measure_module_by_name(self):
        self.fake_connection.setup_response('Module_name1;No error')
        self.fake_connection.setup_response('Module_name2;No error')
        self.fake_connection.setup_response('Module_name3;No error')
        response = self.dut.get_measure_module_by_name('Module_name1')
        self.assertTrue(isinstance(response, ssm_system.MeasureModule))

    def test_get_measure_module_invalid_port(self):
        self.fake_connection.setup_response('3;No error')
        with self.assertRaisesRegex(IndexError, 'Invalid port number. Must be between 1 and 3'):
            self.dut.get_measure_module(5)

    def test_fetch_multiple(self):
        self.fake_connection.setup_response('5.63,4.31,1.33;No error')
        response = self.dut.fetch_multiple(("MX", 1), ("MY", 2), ("MR", 3))
        self.assertEqual(response, (5.63, 4.31, 1.33))
        self.assertIn('FETCh? MX,1,MY,2,MR,3', self.fake_connection.get_outgoing_message())

    def test_read_multiple(self):
        self.fake_connection.setup_response('5.63,4.31,1.33;No error')
        response = self.dut.read_multiple(("MDC", 1), ("MRMS", 2), ("MPTPeak", 3))
        self.assertEqual(response, (5.63, 4.31, 1.33))
        self.assertIn('READ? MDC,1,MRMS,2,MPTPeak,3', self.fake_connection.get_outgoing_message())

    def test_stream_data(self):
        """Test stream data"""

        list_data = [(False, 45.6521), (True, 1.258), (False, 65.8974)]

        my_data = []
        for data in list_data:
            for value in data:
                my_data.append(value)

        list_format = '<?d?d?d'
        pack_data = pack(list_format, *my_data)
        if sys.version_info[0] < 3:
            encoded_data = str(b64encode(pack_data))
        else:
            encoded_data = str(b64encode(pack_data))[2:-1]

        # Response for trace reset command
        self.fake_connection.setup_response('No error')
        # Response for configure_stream_elements
        self.fake_connection.setup_response('No error')
        # Response for format encoding command
        self.fake_connection.setup_response('No error')
        # Response for rate command
        self.fake_connection.setup_response('No error')
        # Response for bytes per row query
        self.fake_connection.setup_response('9;No error')
        # Response for binary format
        self.fake_connection.setup_response('\"?d\";No error')
        # Response for trace start
        self.fake_connection.setup_response('No error')
        # Response for trace data, check errors set to false
        self.fake_connection.setup_response(encoded_data)
        # Response for overflow
        self.fake_connection.setup_response('0;No error')

        response = self.dut.stream_data(10, 3, ("MX", 1), ("MY", 2), ("MR", 3))
        response_list = []
        for data in response:
            response_list.append(data)

        self.assertEqual(response_list, list_data)
        self.assertIn('TRACe:RESEt', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:FORMat:ELEMents MX,1,MY,2,MR,3', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:FORMat:ENCOding B64', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:RATE 10', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:FORMat:ENCOding:B64:BCOunt?', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:FORMat:ENCOding:B64:BFORmat?', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:STARt 3', self.fake_connection.get_outgoing_message())

    def test_get_data(self):
        """Test get data"""

        list_data = [(True, 12.568), (False, 0.258), (True, 15.74)]

        my_data = []
        for data in list_data:
            for value in data:
                my_data.append(value)

        list_format = '<?d?d?d'
        pack_data = pack(list_format, *my_data)
        if sys.version_info[0] < 3:
            encoded_data = str(b64encode(pack_data))
        else:
            encoded_data = str(b64encode(pack_data))[2:-1]

        # Response for trace reset command
        self.fake_connection.setup_response('No error')
        # Response for configure_stream_elements
        self.fake_connection.setup_response('No error')
        # Response for format encoding command
        self.fake_connection.setup_response('No error')
        # Response for rate command
        self.fake_connection.setup_response('No error')
        # Response for bytes per row query
        self.fake_connection.setup_response('9;No error')
        # Response for binary format
        self.fake_connection.setup_response('?d;No error')
        # Response for trace start
        self.fake_connection.setup_response('No error')
        # Response for trace data, check errors set to false
        self.fake_connection.setup_response(encoded_data)
        # Response for overflow
        self.fake_connection.setup_response('0;No error')

        response = self.dut.get_data(10, 3, ("MX", 1), ("MY", 2), ("MR", 3))
        response_list = []
        for data in response:
            response_list.append(data)

        self.assertEqual(response_list, list_data)
        self.assertIn('TRACe:RESEt', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:FORMat:ELEMents MX,1,MY,2,MR,3', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:FORMat:ENCOding B64', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:RATE 10', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:FORMat:ENCOding:B64:BCOunt?', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:FORMat:ENCOding:B64:BFORmat?', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:STARt 3', self.fake_connection.get_outgoing_message())

    def test_log_data_to_csv_file(self):
        """Test CSV log"""

        list_data = [(True, 21.545), (False, 0.25), (True, 165.53)]

        my_data = []
        for data in list_data:
            for value in data:
                my_data.append(value)

        list_format = '<?d?d?d'
        pack_data = pack(list_format, *my_data)
        if sys.version_info[0] < 3:
            encoded_data = str(b64encode(pack_data))
        else:
            encoded_data = str(b64encode(pack_data))[2:-1]

        # Create a CSV file identical to the expected output
        with open('expected_log_data.csv', 'w') as csv_file:
            csv_file.write('MX,1\n')
            for row in list_data:
                csv_file.write(','.join(str(x) for x in row) + '\n')

        # Response for format elements
        self.fake_connection.setup_response('No error')
        # Response for trace format header
        self.fake_connection.setup_response('MX,1;No error')
        # Response for trace reset command
        self.fake_connection.setup_response('No error')
        # Response for configure_stream_elements
        self.fake_connection.setup_response('No error')
        # Response for format encoding command
        self.fake_connection.setup_response('No error')
        # Response for rate command
        self.fake_connection.setup_response('No error')
        # Response for bytes per row query
        self.fake_connection.setup_response('9;No error')
        # Response for binary format
        self.fake_connection.setup_response('?d;No error')
        # Response for trace start
        self.fake_connection.setup_response('No error')
        # Response for trace data, check errors set to false
        self.fake_connection.setup_response(encoded_data)
        # Response for overflow
        self.fake_connection.setup_response('0;No error')

        with open('output_log_data.csv', 'w') as csv_file:
            self.dut.log_data_to_csv_file(10, 3, csv_file, ("MX", 1))

        # Compare that the output file and expected are identical
        expected_log = open('expected_log_data.csv', 'r');
        output_log = open('output_log_data.csv', 'r');
        self.assertEqual(expected_log.read(), output_log.read())
        expected_log.close()
        output_log.close()

        # Cleanup
        remove('expected_log_data.csv')
        remove('output_log_data.csv')

        self.assertIn('TRACe:FORMat:ELEMents MX,1', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:FORMat:HEADer?', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:RESEt', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:FORMat:ELEMents MX,1', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:FORMat:ENCOding B64', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:RATE 10', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:FORMat:ENCOding:B64:BCOunt?', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:FORMat:ENCOding:B64:BFORmat?', self.fake_connection.get_outgoing_message())
        self.assertIn('TRACe:STARt 3', self.fake_connection.get_outgoing_message())

    def test_get_ref_in_edge(self):
        self.fake_connection.setup_response('RISing;No error')
        response = self.dut.get_ref_in_edge()
        self.assertEqual(response, 'RISing')
        self.assertIn('INPut:REFerence:EDGe?', self.fake_connection.get_outgoing_message())

    def test_set_ref_in_edge(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_ref_in_edge('FALLing')
        self.assertIn('INPut:REFerence:EDGe FALLing', self.fake_connection.get_outgoing_message())

    def test_get_ref_out_source(self):
        self.fake_connection.setup_response('S1;No error')
        response = self.dut.get_ref_out_source()
        self.assertEqual(response, 'S1')
        self.assertIn('OUTPut:REFerence:SOURce?', self.fake_connection.get_outgoing_message())

    def test_set_ref_out_source(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_ref_out_source('S2')
        self.assertIn('OUTPut:REFerence:SOURce S2', self.fake_connection.get_outgoing_message())

    def test_get_ref_out_state(self):
        self.fake_connection.setup_response('0;No error')
        response = self.dut.get_ref_out_state()
        self.assertEqual(response, False)
        self.assertIn('OUTPut:REFerence:STATe?', self.fake_connection.get_outgoing_message())

    def test_set_ref_out_state(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_ref_out_state(True)
        self.assertIn('OUTPut:REFerence:STATe 1', self.fake_connection.get_outgoing_message())

    def test_enable_ref_out(self):
        self.fake_connection.setup_response('No error')
        self.dut.enable_ref_out()
        self.assertIn('OUTPut:REFerence:STATe 1', self.fake_connection.get_outgoing_message())

    def test_disable_ref_out(self):
        self.fake_connection.setup_response('No error')
        self.dut.disable_ref_out()
        self.assertIn('OUTPut:REFerence:STATe 0', self.fake_connection.get_outgoing_message())

    def test_configure_ref_out(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut.configure_ref_out('S2', False)
        self.assertIn('OUTPut:REFerence:SOURce S2', self.fake_connection.get_outgoing_message())
        self.assertIn('OUTPut:REFerence:STATe 0', self.fake_connection.get_outgoing_message())

    def test_get_mon_out_mode(self):
        self.fake_connection.setup_response('M3;No error')
        response = self.dut.get_mon_out_mode()
        self.assertEqual(response, 'M3')
        self.assertIn('OUTPut:MONitor:MODe?', self.fake_connection.get_outgoing_message())

    def test_set_mon_out_mode(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_mon_out_state(True)
        self.assertIn('OUTPut:MONitor:STATe 1', self.fake_connection.get_outgoing_message())

    def test_get_mon_out_state(self):
        self.fake_connection.setup_response('0;No error')
        response = self.dut.get_mon_out_state()
        self.assertEqual(response, False)
        self.assertIn('OUTPut:MONitor:STATe?', self.fake_connection.get_outgoing_message())

    def test_set_mon_out_state(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_mon_out_state(True)
        self.assertIn('OUTPut:MONitor:STATe 1', self.fake_connection.get_outgoing_message())

    def test_enable_mon_out(self):
        self.fake_connection.setup_response('No error')
        self.dut.enable_mon_out()
        self.assertIn('OUTPut:MONitor:STATe 1', self.fake_connection.get_outgoing_message())

    def test_disable_mon_out(self):
        self.fake_connection.setup_response('No error')
        self.dut.disable_mon_out()
        self.assertIn('OUTPut:MONitor:STATe 0', self.fake_connection.get_outgoing_message())

    def test_configure_mon_out(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut.configure_mon_out('M1', False)
        self.assertIn('OUTPut:MONitor:MODe M1', self.fake_connection.get_outgoing_message())
        self.assertIn('OUTPut:MONitor:STATe 0', self.fake_connection.get_outgoing_message())

    def test_get_mon_out_scale(self):
        self.fake_connection.setup_response('2.5;No error')
        response = self.dut.get_mon_out_scale()
        self.assertEqual(response, 2.5)
        self.assertIn('OUTPut:MONitor:SCALe?', self.fake_connection.get_outgoing_message())

    def test_get_head_self_cal_status(self):
        self.fake_connection.setup_response('No error')
        self.dut.get_head_self_cal_status()
        self.assertIn('CALibration:SCALibration:STATus?', self.fake_connection.get_outgoing_message())

    def test_run_head_self_calibration(self):
        self.fake_connection.setup_response('No error')
        self.dut.run_head_self_calibration()
        self.assertIn('CALibration:SCALibration:RUN', self.fake_connection.get_outgoing_message())

    def test_reset_head_self_calibration(self):
        self.fake_connection.setup_response('No error')
        self.dut.reset_head_self_calibration()
        self.assertIn('CALibration:SCALibration:RESet', self.fake_connection.get_outgoing_message())

    def test_set_mon_out_manual_level(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_mon_out_manual_level(55.63)
        self.assertIn('OUTPut:MONitor:MLEVel 55.63', self.fake_connection.get_outgoing_message())

    def test_get_mon_out_manual_level(self):
        self.fake_connection.setup_response('26.85;No error')
        response = self.dut.get_mon_out_manual_level()
        self.assertEqual(response, 26.85)
        self.assertIn('OUTPut:MONitor:MLEVel?', self.fake_connection.get_outgoing_message())

    def test_configure_mon_out_manual_mode(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut.configure_mon_out_manual_mode(37.84, False)
        self.assertIn('OUTPut:MONitor:MLEVel 37.84', self.fake_connection.get_outgoing_message())
        self.assertIn('OUTPut:MONitor:MODe MANUAL', self.fake_connection.get_outgoing_message())
        self.assertIn('OUTPut:MONitor:STATe 0', self.fake_connection.get_outgoing_message())

    def test_get_head_self_cal_datetime(self):
        self.fake_connection.setup_response('1985,10,26,1,20,0;No error')
        response = self.dut.get_head_self_cal_datetime()
        self.assertEqual(response, datetime(1985,10,26,1,20,0))

    def test_get_head_self_cal_temperature(self):
        self.fake_connection.setup_response('232.778;No error')
        response = self.dut.get_head_self_cal_temperature()
        self.assertEqual(response, 232.778)

    def test_get_head_cal_datetime(self):
        self.fake_connection.setup_response('1985,10,26,1,20,0;No error')
        response = self.dut.get_head_cal_datetime()
        self.assertEqual(response, datetime(1985,10,26,1,20,0))

    def test_get_head_cal_temperature(self):
        self.fake_connection.setup_response('232.778;No error')
        response = self.dut.get_head_cal_temperature()
        self.assertEqual(response, 232.778)


class TestSourceModule(TestWithFakeSSMSSourceModule):
    def test_fetch_multiple(self):
        self.fake_connection.setup_response('3.45,2.89,0.73;No error')
        response = self.dut_module.fetch_multiple('SRANge', 'MDC', 'MY')
        self.assertEqual(response, (3.45, 2.89, 0.73))
        self.assertIn('FETCh? SRANge,1,MDC,1,MY,1', self.fake_connection.get_outgoing_message())

    def test_get_name(self):
        self.fake_connection.setup_response('"module_1_name";No error')
        response = self.dut_module.get_name()
        self.assertEqual(response, 'module_1_name')
        self.assertIn('SOURce1:NAME?', self.fake_connection.get_outgoing_message())

    def test_get_notes(self):
        self.fake_connection.setup_response('"module_1_notes";No error')
        response = self.dut_module.get_notes()
        self.assertEqual(response, 'module_1_notes')
        self.assertIn('SOURce1:NOTes?', self.fake_connection.get_outgoing_message())

    def test_set_name(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_name('New_Module_Name')
        self.assertIn('SOURce1:NAME "New_Module_Name"', self.fake_connection.get_outgoing_message())

    def test_set_notes(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_notes('New_Module_Notes')
        self.assertIn('SOURce1:NOTes "New_Module_Notes"', self.fake_connection.get_outgoing_message())

    def test_get_model(self):
        self.fake_connection.setup_response('BCS-10;No error')
        response = self.dut_module.get_model()
        self.assertEqual(response, 'BCS-10')
        self.assertIn('SOURce1:MODel?', self.fake_connection.get_outgoing_message())

    def test_get_serial(self):
        self.fake_connection.setup_response('BCS2345;No error')
        response = self.dut_module.get_serial()
        self.assertEqual(response, 'BCS2345')
        self.assertIn('SOURce1:SERial?', self.fake_connection.get_outgoing_message())

    def test_get_hw_version(self):
        self.fake_connection.setup_response('2;No error')
        response = self.dut_module.get_hw_version()
        self.assertEqual(response, 2)
        self.assertIn('SOURce1:HWVersion?', self.fake_connection.get_outgoing_message())

    def test_get_self_cal_status(self):
        self.fake_connection.setup_response('Pass;No error')
        response = self.dut_module.get_self_cal_status()
        self.assertEqual(response, 'Pass')
        self.assertIn('SOURce1:SCALibration:STATus?', self.fake_connection.get_outgoing_message())

    def test_run_self_cal(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.run_self_cal()
        ## Why does this method have a return if command() returns None?
        self.assertIn('SOURce1:SCALibration:RUN', self.fake_connection.get_outgoing_message())

    def test_reset_self_cal(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.reset_self_cal()
        self.assertIn('SOURce1:SCALibration:RESet', self.fake_connection.get_outgoing_message())

    def test_get_enable_state(self):
        self.fake_connection.setup_response('0;No error')
        response = self.dut_module.get_enable_state()
        self.assertEqual(response, False)
        self.assertIn('SOURce1:STATe?', self.fake_connection.get_outgoing_message())

    def test_set_enable_state(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_enable_state(True)
        self.assertIn('SOURce1:STATe 1', self.fake_connection.get_outgoing_message())

    def test_enable(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.enable()
        self.assertIn('SOURce1:STATe 1', self.fake_connection.get_outgoing_message())

    def test_disable(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.disable()
        self.assertIn('SOURce1:STATe 0', self.fake_connection.get_outgoing_message())

    def test_get_excitation_mode(self):
        self.fake_connection.setup_response('VOLTAGE;No error')
        response = self.dut_module.get_excitation_mode()
        self.assertEqual(response, 'VOLTAGE')
        self.assertIn('SOURce1:FUNCtion:MODE?', self.fake_connection.get_outgoing_message())

    def test_set_excitation_mode(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_excitation_mode('CURRENT')
        self.assertIn('SOURce1:FUNCtion:MODE CURRENT', self.fake_connection.get_outgoing_message())

    def test_go_to_current_mode(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.go_to_current_mode()
        self.assertIn('SOURce1:FUNCtion:MODE CURRent', self.fake_connection.get_outgoing_message())

    def test_go_to_voltage_mode(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.go_to_voltage_mode()
        self.assertIn('SOURce1:FUNCtion:MODE VOLTage', self.fake_connection.get_outgoing_message())

    def test_get_shape(self):
        self.fake_connection.setup_response('SINUSOID; No error')
        response = self.dut_module.get_shape()
        self.assertEqual(response, 'SINUSOID')
        self.assertIn('SOURce1:FUNCtion:SHAPe?', self.fake_connection.get_outgoing_message())

    def test_set_shape(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_shape('DC')
        self.assertIn('SOURce1:FUNCtion:SHAPe DC', self.fake_connection.get_outgoing_message())

    def test_get_frequency(self):
        self.fake_connection.setup_response('1000;No error')
        self.dut_module.get_frequency()
        self.assertIn('SOURce1:FREQuency?', self.fake_connection.get_outgoing_message())

    def test_set_frequency(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_frequency(1000)
        self.assertIn('SOURce1:FREQuency 1000', self.fake_connection.get_outgoing_message())

    def test_get_sync_state(self):
        self.fake_connection.setup_response('0;No error')
        response = self.dut_module.get_sync_state()
        self.assertEqual(response, False)
        self.assertIn('SOURce1:SYNChronize:STATe?', self.fake_connection.get_outgoing_message())

    def test_get_sync_source(self):
        self.fake_connection.setup_response('1;No error')
        response = self.dut_module.get_sync_source()
        self.assertEqual(response, '1')
        self.assertIn('SOURce1:SYNChronize:SOURce?', self.fake_connection.get_outgoing_message())

    def test_get_sync_phase_shift(self):
        self.fake_connection.setup_response('45;No error')
        response = self.dut_module.get_sync_phase_shift()
        self.assertEqual(response, 45.0)
        self.assertIn('SOURce1:SYNChronize:PHASe?', self.fake_connection.get_outgoing_message())

    def test_configure_sync(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_sync('S1', 60, False)
        self.assertIn('SOURce1:SYNChronize:SOURce S1', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:SYNChronize:PHASe 60', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:SYNChronize:STATe 0', self.fake_connection.get_outgoing_message())

    def test_get_duty(self):
        self.fake_connection.setup_response('50;No error')
        response = self.dut_module.get_duty()
        self.assertEqual(response, 50)
        self.assertIn('SOURce1:DCYCle?', self.fake_connection.get_outgoing_message())

    def test_set_duty(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_duty(65)
        self.assertIn('SOURce1:DCYCle 65', self.fake_connection.get_outgoing_message())

    def test_get_coupling(self):
        self.fake_connection.setup_response('AC;No error')
        response = self.dut_module.get_coupling()
        self.assertEqual(response, 'AC')
        self.assertIn('SOURce1:COUPling?', self.fake_connection.get_outgoing_message())

    def test_set_coupling(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_coupling('DC')
        self.assertIn('SOURce1:COUPling DC', self.fake_connection.get_outgoing_message())

    def test_use_ac_coupling(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.use_ac_coupling()
        self.assertIn('SOURce1:COUPling AC', self.fake_connection.get_outgoing_message())

    def test_use_dc_coupling(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.use_dc_coupling()
        self.assertIn('SOURce1:COUPling DC', self.fake_connection.get_outgoing_message())

    def test_get_guard_state(self):
        self.fake_connection.setup_response('1;No error')
        response = self.dut_module.get_guard_state()
        self.assertEqual(response, True)
        self.assertIn('SOURce1:GUARd?', self.fake_connection.get_outgoing_message())

    def test_set_guard_state(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_guard_state(True)
        self.assertIn('SOURce1:GUARd 1', self.fake_connection.get_outgoing_message())

    def test_enable_guards(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.enable_guards()
        self.assertIn('SOURce1:GUARd 1', self.fake_connection.get_outgoing_message())

    def test_disable_guards(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.disable_guards()
        self.assertIn('SOURce1:GUARd 0', self.fake_connection.get_outgoing_message())

    def test_get_cmr_source(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.get_cmr_source()
        self.assertIn('SOURce1:CMR:SOURce?', self.fake_connection.get_outgoing_message())

    def test_set_cmr_source(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_cmr_source('EXTernal')
        self.assertIn('SOURce1:CMR:SOURce EXTernal', self.fake_connection.get_outgoing_message())

    def test_get_cmr_state(self):
        self.fake_connection.setup_response('1;No error')
        response = self.dut_module.get_cmr_state()
        self.assertEqual(response, True)
        self.assertIn('SOURce1:CMR:STATe?', self.fake_connection.get_outgoing_message())

    def test_set_cmr_state(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_cmr_state(False)
        self.assertIn('SOURce1:CMR:STATe 0', self.fake_connection.get_outgoing_message())

    def test_enable_cmr(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.enable_cmr()
        self.assertIn('SOURce1:CMR:STATe 1', self.fake_connection.get_outgoing_message())

    def test_disable_cmr(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.disable_cmr()
        self.assertIn('SOURce1:CMR:STATe 0', self.fake_connection.get_outgoing_message())

    def test_configure_cmr(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_cmr('EXTernal', False)
        self.assertIn('SOURce1:CMR:SOURce EXTernal', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:CMR:STATe 0', self.fake_connection.get_outgoing_message())

    def test_get_current_range(self):
        self.fake_connection.setup_response('2;No error')
        response = self.dut_module.get_current_range()
        self.assertEqual(response, 2)
        self.assertIn('SOURce1:CURRent:RANGe?', self.fake_connection.get_outgoing_message())

    def test_get_current_ac_range(self):
        self.fake_connection.setup_response('0.5;No error')
        response = self.dut_module.get_current_ac_range()
        self.assertEqual(response, 0.5)
        self.assertIn('SOURce1:CURRent:RANGe:AC?', self.fake_connection.get_outgoing_message())

    def test_get_current_dc_range(self):
        self.fake_connection.setup_response('1.52;No error')
        response = self.dut_module.get_current_dc_range()
        self.assertEqual(response, 1.52)
        self.assertIn('SOURce1:CURRent:RANGe:DC?', self.fake_connection.get_outgoing_message())

    def test_get_current_autorange_status(self):
        self.fake_connection.setup_response('1;No error')
        response = self.dut_module.get_current_autorange_status()
        self.assertEqual(response, True)
        self.assertIn('SOURce1:CURRent:RANGe:AUTO?', self.fake_connection.get_outgoing_message())

    def test_configure_current_range_autorange(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_current_range(True)
        self.assertIn('SOURce1:CURRent:RANGe:AUTO 1', self.fake_connection.get_outgoing_message())

    def test_configure_current_range_autorange_exception(self):
        self.fake_connection.setup_response('No error')
        with self.assertRaisesRegex(ValueError, 'If autorange is selected, a manual range cannot be specified.'):
            self.dut_module.configure_current_range(True, 5.0, 2.5, 3.2)

    def test_configure_current_range_manual_max(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_current_range(False, 4.6)
        self.assertIn('SOURce1:CURRent:RANGe 4.6', self.fake_connection.get_outgoing_message())

    def test_configure_current_range_manual_max_ac(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_current_range(False, max_ac_level=3.2)
        self.assertIn('SOURce1:CURRent:RANGe:AC 3.2', self.fake_connection.get_outgoing_message())

    def test_configure_current_range_manual_max_dc(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_current_range(False, max_dc_level=5.5)
        self.assertIn('SOURce1:CURRent:RANGe:DC 5.5', self.fake_connection.get_outgoing_message())

    def test_configure_current_range_manual_exception(self):
        with self.assertRaisesRegex(ValueError, 'Either a single range, or separate AC and DC ranges can be supplied, not both.'):
            self.dut_module.configure_current_range(False, 5.0, 2.5)

    def test_get_current_amplitude(self):
        self.fake_connection.setup_response('0.25;No error')
        response = self.dut_module.get_current_amplitude()
        self.assertEqual(response, 0.25)
        self.assertIn('SOURce1:CURRent:LEVel:AMPLitude?', self.fake_connection.get_outgoing_message())

    def test_set_current_amplitude(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_current_amplitude(0.25)
        self.assertIn('SOURce1:CURRent:LEVel:AMPLitude 0.25', self.fake_connection.get_outgoing_message())

    def test_get_current_offset(self):
        self.fake_connection.setup_response('0.5;No error')
        response = self.dut_module.get_current_offset()
        self.assertEqual(response, 0.5)
        self.assertIn('SOURce1:CURRent:LEVel:OFFSet?', self.fake_connection.get_outgoing_message())

    def test_set_current_offset(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_current_offset(0.65)
        self.assertIn('SOURce1:CURRent:LEVel:OFFSet 0.65', self.fake_connection.get_outgoing_message())

    def test_apply_dc_current(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut_module.apply_dc_current(2.2)
        self.assertIn('SOURce1:FUNCtion:MODE CURRent', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:FUNCtion:SHAPe DC', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:CURRent:LEVel:AMPLitude 2.2', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:STATe 1', self.fake_connection.get_outgoing_message())

    def test_apply_ac_current(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut_module.apply_ac_current(2000, 2.5, 0.5)
        self.assertIn('SOURce1:FUNCtion:MODE CURRent', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:FREQuency 2000', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:FUNCtion:SHAPe SINusoid', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:CURRent:LEVel:AMPLitude 2.5', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:CURRent:LEVel:OFFSet 0.5', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:STATe 1', self.fake_connection.get_outgoing_message())

    def test_get_current_limit(self):
        self.fake_connection.setup_response('5;No error')
        response = self.dut_module.get_current_limit()
        self.assertEqual(response, 5)
        self.assertIn('SOURce1:CURRent:PROTection?', self.fake_connection.get_outgoing_message())

    def test_set_current_limit(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_current_limit(3.65)
        self.assertIn('SOURce1:CURRent:PROTection 3.65', self.fake_connection.get_outgoing_message())

    def test_get_current_limit_status(self):
        self.fake_connection.setup_response('0;No error')
        response = self.dut_module.get_current_limit_status()
        self.assertEqual(response, False)
        self.assertIn('SOURce1:CURRent:PROTection:TRIPped?', self.fake_connection.get_outgoing_message())

    def test_get_voltage_range(self):
        self.fake_connection.setup_response('5.2;No error')
        response = self.dut_module.get_voltage_range()
        self.assertEqual(response, 5.2)
        self.assertIn('SOURce1:VOLTage:RANGe?', self.fake_connection.get_outgoing_message())

    def test_get_voltage_ac_range(self):
        self.fake_connection.setup_response('4.25;No error')
        response = self.dut_module.get_voltage_ac_range()
        self.assertEqual(response, 4.25)
        self.assertIn('SOURce1:VOLTage:RANGe:AC?', self.fake_connection.get_outgoing_message())

    def test_get_voltage_dc_range(self):
        self.fake_connection.setup_response('3.65;No error')
        response = self.dut_module.get_voltage_dc_range()
        self.assertEqual(response, 3.65)
        self.assertIn('SOURce1:VOLTage:RANGe:DC?', self.fake_connection.get_outgoing_message())

    def test_get_voltage_autorange_status(self):
        self.fake_connection.setup_response('0;No error')
        response = self.dut_module.get_voltage_autorange_status()
        self.assertEqual(response, False)
        self.assertIn('SOURce1:VOLTage:RANGe:AUTO?', self.fake_connection.get_outgoing_message())

    def test_configure_voltage_range_autorange(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_voltage_range(True)
        self.assertIn('SOURce1:VOLTage:RANGe:AUTO 1', self.fake_connection.get_outgoing_message())

    def test_configure_voltage_range_autorange_exception(self):
        with self.assertRaisesRegex(ValueError, 'If autorange is selected, a manual range cannot be specified.'):
            self.dut_module.configure_voltage_range(True, 2.0)

    def test_configure_voltage_range_manual_max(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_voltage_range(False, max_level=2.5)
        self.assertIn('SOURce1:VOLTage:RANGe 2.5', self.fake_connection.get_outgoing_message())

    def test_configure_voltage_range_max_ac(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_voltage_range(False, max_ac_level=3.6)
        self.assertIn('SOURce1:VOLTage:RANGe:AC 3.6', self.fake_connection.get_outgoing_message())

    def test_configure_voltage_range_max_ac(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_voltage_range(False, max_dc_level=1.85)
        self.assertIn('SOURce1:VOLTage:RANGe:DC 1.85', self.fake_connection.get_outgoing_message())

    def test_get_voltage_amplitude(self):
        self.fake_connection.setup_response('4.35;No error')
        response = self.dut_module.get_voltage_amplitude()
        self.assertEqual(response, 4.35)
        self.assertIn('SOURce1:VOLTage:LEVel:AMPLitude?', self.fake_connection.get_outgoing_message())

    def test_set_voltage_amplitude(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_voltage_amplitude(1.23)
        self.assertIn('SOURce1:VOLTage:LEVel:AMPLitude 1.23', self.fake_connection.get_outgoing_message())

    def test_get_voltage_offset(self):
        self.fake_connection.setup_response('0.5;No error')
        response = self.dut_module.get_voltage_offset()
        self.assertEqual(response, 0.5)
        self.assertIn('SOURce1:VOLTage:LEVel:OFFSet?', self.fake_connection.get_outgoing_message())

    def test_set_voltage_offset(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_voltage_offset(0.65)
        self.assertIn('SOURce1:VOLTage:LEVel:OFFSet 0.65', self.fake_connection.get_outgoing_message())

    def test_apply_dc_voltage(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut_module.apply_dc_voltage(5.2)
        self.assertIn('SOURce1:FUNCtion:MODE VOLTage', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:FUNCtion:SHAPe DC', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:VOLTage:LEVel:AMPLitude 5.2', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:STATe 1', self.fake_connection.get_outgoing_message())

    def test_apply_ac_voltage(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut_module.apply_ac_voltage(5000, 1.63, 0.5)
        self.assertIn('SOURce1:FUNCtion:MODE VOLTage', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:FREQuency 5000', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:FUNCtion:SHAPe SINusoid', self.fake_connection.get_outgoing_message())
        # Why is current amplitude being set for apply ac voltage method?
        self.assertIn('SOURce1:VOLTage:LEVel:AMPLitude 1.63', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:VOLTage:LEVel:OFFSet 0.5', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURce1:STATe 1', self.fake_connection.get_outgoing_message())

    def test_get_voltage_limit(self):
        self.fake_connection.setup_response('1.45;No error')
        response = self.dut_module.get_voltage_limit()
        self.assertEqual(response, 1.45)
        self.assertIn('SOURce1:VOLTage:PROTection?', self.fake_connection.get_outgoing_message())

    def test_set_voltage_limit(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_voltage_limit(3.65)
        self.assertIn('SOURce1:VOLTage:PROTection 3.65', self.fake_connection.get_outgoing_message())

    def test_get_voltage_limit_status(self):
        self.fake_connection.setup_response('0;No error')
        response = self.dut_module.get_voltage_limit_status()
        self.assertEqual(response, False)
        self.assertIn('SOURce1:VOLTage:PROTection:TRIPped?', self.fake_connection.get_outgoing_message())

    def test_get_present_questionable_status(self):
        self.fake_connection.setup_response('15')
        response = self.dut_module.get_present_questionable_status()

        self.assertEqual(response.read_error, True)
        self.assertEqual(response.unrecognized_pod_error, True)
        self.assertEqual(response.port_direction_error, True)
        self.assertEqual(response.factory_calibration_failure, True)
        self.assertEqual(response.self_calibration_failure, False)

        self.assertIn('STATus:QUEStionable:SOURce1:CONDition?', self.fake_connection.get_outgoing_message())

    def test_get_questionable_events(self):
        self.fake_connection.setup_response('10')
        response = self.dut_module.get_questionable_events()

        self.assertEqual(response.read_error, False)
        self.assertEqual(response.unrecognized_pod_error, True)
        self.assertEqual(response.port_direction_error, False)
        self.assertEqual(response.factory_calibration_failure, True)
        self.assertEqual(response.self_calibration_failure, False)

        self.assertIn('STATus:QUEStionable:SOURce1:EVENt?', self.fake_connection.get_outgoing_message())

    def test_get_questionable_event_enable_mask(self):
        self.fake_connection.setup_response('25')
        response = self.dut_module.get_questionable_event_enable_mask()

        self.assertEqual(response.read_error, True)
        self.assertEqual(response.unrecognized_pod_error, False)
        self.assertEqual(response.port_direction_error, False)
        self.assertEqual(response.factory_calibration_failure, True)
        self.assertEqual(response.self_calibration_failure, True)

        self.assertIn('STATus:QUEStionable:SOURce1:ENABle?', self.fake_connection.get_outgoing_message())

    def test_set_questionable_event_enable_mask(self):
        self.fake_connection.setup_response('No error')
        # Arguments go from LSB to MSB
        register = ssm_base_module.SSMSystemModuleQuestionableRegister(False, True, True, False, True)
        self.dut_module.set_questionable_event_enable_mask(register)
        self.assertIn('STATus:QUEStionable:SOURce1:ENABle 22', self.fake_connection.get_outgoing_message())

    def test_get_present_operation_status(self):
        self.fake_connection.setup_response('2')
        response = self.dut_module.get_present_operation_status()
        self.assertEqual(response.v_limit, False)
        self.assertEqual(response.i_limit, True)
        self.assertEqual(response.sweeping, False)
        self.assertIn('STATus:OPERation:SOURce1:CONDition?', self.fake_connection.get_outgoing_message())

    def test_get_operation_events(self):
        self.fake_connection.setup_response('7')
        response = self.dut_module.get_operation_events()
        self.assertEqual(response.v_limit, True)
        self.assertEqual(response.i_limit, True)
        self.assertEqual(response.sweeping, True)
        self.assertIn('STATus:OPERation:SOURce1:EVENt?', self.fake_connection.get_outgoing_message())

    def test_get_operation_event_enable_mask(self):
        self.fake_connection.setup_response('1')
        response = self.dut_module.get_operation_event_enable_mask()
        self.assertEqual(response.v_limit, True)
        self.assertEqual(response.i_limit, False)
        self.assertEqual(response.sweeping, False)
        self.assertIn('STATus:OPERation:SOURce1:ENABle?', self.fake_connection.get_outgoing_message())

    def test_set_operation_event_enable_mask(self):
        self.fake_connection.setup_response('No error')
        register = ssm_source_module.SSMSystemSourceModuleOperationRegister(False, False, False)
        self.dut_module.set_operation_event_enable_mask(register)
        self.assertIn('STATus:OPERation:SOURce1:ENABle 0', self.fake_connection.get_outgoing_message())

    def test_get_identify_state(self):
        self.fake_connection.setup_response('0')
        response = self.dut_module.get_identify_state()
        self.assertEqual(response, False)
        self.assertIn('SOURce1:IDENtify?', self.fake_connection.get_outgoing_message())

    def test_set_identify_state(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_identify_state(True)
        self.assertIn('SOURce1:IDENtify 1', self.fake_connection.get_outgoing_message())

    def test_get_self_cal_datetime(self):
        self.fake_connection.setup_response('1985,10,26,1,20,0;No error')
        response = self.dut_module.get_self_cal_datetime()
        self.assertEqual(response, datetime(1985,10,26,1,20,0))

    def test_get_self_cal_temperature(self):
        self.fake_connection.setup_response('232.778;No error')
        response = self.dut_module.get_self_cal_temperature()
        self.assertEqual(response, 232.778)


class TestMeasureModule(TestWithFakeSSMSMeasureModule):
    def test_get_name(self):
        self.fake_connection.setup_response('Module_name;No error')
        response = self.dut_module.get_name()
        self.assertEqual(response, 'Module_name')
        self.assertIn('SENSe1:NAME?', self.fake_connection.get_outgoing_message())

    def test_set_name(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_name('New_module_name')
        self.assertIn('SENSe1:NAME "New_module_name"', self.fake_connection.get_outgoing_message())

    def test_get_model(self):
        self.fake_connection.setup_response('CM-15;No error')
        response = self.dut_module.get_model()
        self.assertEqual(response, 'CM-15')
        self.assertIn('SENSe1:MODel?', self.fake_connection.get_outgoing_message())

    def test_get_serial(self):
        self.fake_connection.setup_response('LSA1234;No error')
        response = self.dut_module.get_serial()
        self.assertEqual(response, 'LSA1234')
        self.assertIn('SENSe1:SERial?', self.fake_connection.get_outgoing_message())

    def test_get_hw_version(self):
        self.fake_connection.setup_response('125;No error')
        response = self.dut_module.get_hw_version()
        self.assertEqual(response, 125)
        self.assertIn('SENSe1:HWVersion?', self.fake_connection.get_outgoing_message())

    def test_get_self_cal_status(self):
        self.fake_connection.setup_response('Pass;No error')
        response = self.dut_module.get_self_cal_status()
        self.assertEqual(response, 'Pass')
        self.assertIn('SENSe1:SCALibration:STATus?', self.fake_connection.get_outgoing_message())

    def test_run_self_cal(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.run_self_cal()
        self.assertIn('SENSe1:SCALibration:RUN', self.fake_connection.get_outgoing_message())

    def test_reset_self_cal(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.reset_self_cal()
        self.assertIn('SENSe1:SCALibration:RESet', self.fake_connection.get_outgoing_message())

    def test_get_averaging_time(self):
        self.fake_connection.setup_response('0.35;No error')
        response = self.dut_module.get_averaging_time()
        self.assertEqual(response, 0.35)
        self.assertIn('SENSe1:NPLCycles?', self.fake_connection.get_outgoing_message())

    def test_set_averaging_time(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_averaging_time(0.5)
        self.assertIn('SENSe1:NPLCycles 0.5', self.fake_connection.get_outgoing_message())

    def test_get_mode(self):
        self.fake_connection.setup_response('DC;No error')
        response = self.dut_module.get_mode()
        self.assertEqual(response, 'DC')
        self.assertIn('SENSe1:MODE?', self.fake_connection.get_outgoing_message())

    def test_set_mode(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_mode('LIA')
        self.assertIn('SENSe1:MODE LIA', self.fake_connection.get_outgoing_message())

    def test_get_coupling(self):
        self.fake_connection.setup_response('AC;No error')
        response = self.dut_module.get_coupling()
        self.assertEqual(response, 'AC')
        self.assertIn('SENSe1:COUPling?', self.fake_connection.get_outgoing_message())

    def test_set_coupling(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_coupling('AC')
        self.assertIn('SENSe1:COUPling AC', self.fake_connection.get_outgoing_message())

    def test_use_ac_coupling(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.use_ac_coupling()
        self.assertIn('SENSe1:COUPling AC', self.fake_connection.get_outgoing_message())

    def test_use_dc_coupling(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.use_dc_coupling()
        self.assertIn('SENSe1:COUPling DC', self.fake_connection.get_outgoing_message())

    def test_get_input_configuration(self):
        self.fake_connection.setup_response('AB;No error')
        response = self.dut_module.get_input_configuration()
        self.assertEqual(response, 'AB')
        self.assertIn('SENSe1:CONFiguration?', self.fake_connection.get_outgoing_message())

    def test_set_input_configuration(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_input_configuration('GROUND')
        self.assertIn('SENSe1:CONFiguration GROUND', self.fake_connection.get_outgoing_message())

    def test_get_bias_enabled(self):
        self.fake_connection.setup_response('1;No error')
        response = self.dut_module.get_bias_voltage_enabled()
        self.assertEqual(response, True)
        self.assertIn('SENSe1:BIAS:STATe?', self.fake_connection.get_outgoing_message())

    def test_bias_enable(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.enable_bias_voltage()
        self.assertIn('SENSe1:BIAS:STATe 1', self.fake_connection.get_outgoing_message())

    def test_bias_disable(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.disable_bias_voltage()
        self.assertIn('SENSe1:BIAS:STATe 0', self.fake_connection.get_outgoing_message())

    def test_get_bias_voltage(self):
        self.fake_connection.setup_response('2.54;No error')
        response = self.dut_module.get_bias_voltage()
        self.assertEqual(response, 2.54)
        self.assertIn('SENSe1:BIAS:VOLTage:DC?', self.fake_connection.get_outgoing_message())

    def test_set_bias_voltage(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_bias_voltage(0.75)
        self.assertIn('SENSe1:BIAS:VOLTage:DC 0.75', self.fake_connection.get_outgoing_message())

    def test_get_filter_state(self):
        self.fake_connection.setup_response('0;No error')
        response = self.dut_module.get_filter_state()
        self.assertEqual(response, False)
        self.assertIn('SENSe1:FILTer:STATe?', self.fake_connection.get_outgoing_message())

    def test_get_lowpass_corner_frequency(self):
        self.fake_connection.setup_response('F3000;No error')
        response = self.dut_module.get_lowpass_corner_frequency()
        self.assertEqual(response, 'F3000')
        self.assertIn('SENSe1:FILTer:LPASs:FREQuency?', self.fake_connection.get_outgoing_message())

    def test_get_lowpass_rolloff(self):
        self.fake_connection.setup_response('R6;No error')
        response = self.dut_module.get_lowpass_rolloff()
        self.assertEqual(response, 'R6')
        self.assertIn('SENSe1:FILTer:LPASs:ATTenuation?', self.fake_connection.get_outgoing_message())

    def test_highpass_corner_frequency(self):
        self.fake_connection.setup_response('F10000;No error')
        response = self.dut_module.get_highpass_corner_frequency()
        self.assertEqual(response, 'F10000')
        self.assertIn('SENSe1:FILTer:HPASs:FREQuency?', self.fake_connection.get_outgoing_message())

    def test_get_highpass_rolloff(self):
        self.fake_connection.setup_response('R12;No error')
        response = self.dut_module.get_highpass_rolloff()
        self.assertEqual(response, 'R12')
        self.assertIn('SENSe1:FILTer:HPASs:ATTenuation?', self.fake_connection.get_outgoing_message())

    def test_get_gain_allocation_strategy(self):
        self.fake_connection.setup_response('NOISE;No error')
        response = self.dut_module.get_gain_allocation_strategy()
        self.assertEqual(response, 'NOISE')
        self.assertIn('SENSe1:FILTer:OPTimization?', self.fake_connection.get_outgoing_message())

    def test_set_gain_allocation_strategy(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_gain_allocation_strategy('RESERVE')
        self.assertIn('SENSe1:FILTer:OPTimization RESERVE', self.fake_connection.get_outgoing_message())

    def test_configure_input_lowpass_filter(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_input_lowpass_filter('F1000')
        self.assertIn('SENSe1:FILTer:LPASs:FREQuency F1000', self.fake_connection.get_outgoing_message())
        self.assertIn('SENSe1:FILTer:LPASs:ATTenuation R12', self.fake_connection.get_outgoing_message())
        self.assertIn('SENSe1:FILTer:STATe 1', self.fake_connection.get_outgoing_message())

    def test_configure_input_highpass_filter(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_input_highpass_filter('F1000')
        self.assertIn('SENSe1:FILTer:HPASs:FREQuency F1000', self.fake_connection.get_outgoing_message())
        self.assertIn('SENSe1:FILTer:HPASs:ATTenuation R12', self.fake_connection.get_outgoing_message())
        self.assertIn('SENSe1:FILTer:STATe 1', self.fake_connection.get_outgoing_message())

    def test_disable_input_filters(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.disable_input_filters()
        self.assertIn('SENSe1:FILTer:STATe 0', self.fake_connection.get_outgoing_message())

    def test_get_current_range(self):
        self.fake_connection.setup_response('1.25;No error')
        response = self.dut_module.get_current_range()
        self.assertEqual(response, 1.25)
        self.assertIn('SENSe1:CURRent:RANGe?', self.fake_connection.get_outgoing_message())

    def test_get_current_autorange_status(self):
        self.fake_connection.setup_response('1;No error')
        response = self.dut_module.get_current_autorange_status()
        self.assertEqual(response, True)
        self.assertIn('SENSe1:CURRent:RANGe:AUTO?', self.fake_connection.get_outgoing_message())

    def test_configure_current_range_manual(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_current_range(False, 2.5)
        self.assertIn('SENSe1:CURRent:RANGe 2.5', self.fake_connection.get_outgoing_message())

    def test_configure_current_range_auto(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_current_range(True, max_level=None)
        self.assertIn('SENSe1:CURRent:RANGe:AUTO 1', self.fake_connection.get_outgoing_message())

    def test_configure_current_range_exception(self):
        self.fake_connection.setup_response('No error')
        with self.assertRaisesRegex(ValueError,'If autorange is selected, a manual range cannot be specified.'):
            self.dut_module.configure_current_range(True, 1.5)

    def test_get_voltage_range(self):
        self.fake_connection.setup_response('6.54;No error')
        response = self.dut_module.get_voltage_range()
        self.assertEqual(response, 6.54)
        self.assertIn('SENSe1:VOLTage:RANGe?', self.fake_connection.get_outgoing_message())

    def test_get_voltage_autorange_status(self):
        self.fake_connection.setup_response('0;No error')
        response = self.dut_module.get_voltage_autorange_status()
        self.assertEqual(response, False)
        self.assertIn('SENSe1:VOLTage:RANGe:AUTO?', self.fake_connection.get_outgoing_message())

    def test_configure_voltage_range_autorange(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_voltage_range(True, max_level=None)
        self.assertIn('SENSe1:VOLTage:RANGe:AUTO 1', self.fake_connection.get_outgoing_message())

    def test_configure_voltage_range_exception(self):
        self.fake_connection.setup_response('No error')
        with self.assertRaisesRegex(ValueError, 'If autorange is selected, a manual range cannot be specified.'):
            self.dut_module.configure_voltage_range(True, 2.5)

    def test_configure_voltage_range_manual(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.configure_voltage_range(False, 2.5)
        self.assertIn('SENSe1:VOLTage:RANGe 2.5', self.fake_connection.get_outgoing_message())

    def test_get_reference_source(self):
        self.fake_connection.setup_response('S3;No error')
        response = self.dut_module.get_reference_source()
        self.assertEqual(response, 'S3')
        self.assertIn('SENSe1:LIA:RSOurce?', self.fake_connection.get_outgoing_message())

    def test_set_reference_harmonic(self):
        self.fake_connection.setup_response('3;No error')
        response = self.dut_module.get_reference_harmonic()
        self.assertEqual(response, 3)
        self.assertIn('SENSe1:LIA:DHARmonic?', self.fake_connection.get_outgoing_message())

    def test_set_reference_harmonic(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_reference_harmonic(4)
        self.assertIn('SENSe1:LIA:DHARmonic 4', self.fake_connection.get_outgoing_message())

    def test_get_reference_phase_shift(self):
        self.fake_connection.setup_response('45;No error')
        response = self.dut_module.get_reference_phase_shift()
        self.assertEqual(response, 45)
        self.assertIn('SENSe1:LIA:DPHase?', self.fake_connection.get_outgoing_message())

    def test_auto_phase(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.auto_phase()
        self.assertIn('SENSe1:LIA:DPHase:AUTO', self.fake_connection.get_outgoing_message())

    def test_get_lock_in_time_constant(self):
        self.fake_connection.setup_response('0.05;No error')
        response = self.dut_module.get_lock_in_time_constant()
        self.assertEqual(response, 0.05)
        self.assertIn('SENSe1:LIA:TIMEconstant?', self.fake_connection.get_outgoing_message())

    def test_set_lock_in_time_constant(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_lock_in_time_constant(0.025)
        self.assertIn('SENSe1:LIA:TIMEconstant 0.025', self.fake_connection.get_outgoing_message())

    def test_lock_in_settle_time(self):
        self.fake_connection.setup_response("63.41;No error")
        response = self.dut_module.get_lock_in_settle_time()
        self.assertEqual(response, 63.41)
        self.assertIn('SENSe1:LIA:STIMe? 0.01', self.fake_connection.get_outgoing_message())

    def test_lock_in_equivalent_noise_bandwidth(self):
        self.fake_connection.setup_response("125.25;No error")
        response = self.dut_module.get_lock_in_equivalent_noise_bandwidth()
        self.assertEqual(response, 125.25)
        self.assertIn('SENSe1:LIA:ENBW?', self.fake_connection.get_outgoing_message())

    def test_get_lock_in_rolloff(self):
        self.fake_connection.setup_response('R6;No error')
        response = self.dut_module.get_lock_in_rolloff()
        self.assertEqual(response, 'R6')
        self.assertIn('SENSe1:LIA:ROLLoff?', self.fake_connection.get_outgoing_message())

    def test_set_lock_in_rolloff(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_lock_in_rolloff('R18')
        self.assertIn('SENSe1:LIA:ROLLoff R18', self.fake_connection.get_outgoing_message())

    def test_get_lock_in_fir_state(self):
        self.fake_connection.setup_response('0;No error')
        response = self.dut_module.get_lock_in_fir_state()
        self.assertEqual(response, False)
        self.assertIn('SENSe1:LIA:FIR:STATe?', self.fake_connection.get_outgoing_message())

    def test_enable_lock_in_fir(self):
        self.fake_connection.setup_response('0;No error')
        response = self.dut_module.get_lock_in_fir_state()
        self.assertEqual(response, False)
        self.assertIn('SENSe1:LIA:FIR:STATe?', self.fake_connection.get_outgoing_message())

    def test_set_lock_in_fir_state(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_lock_in_fir_state(True)
        self.assertIn('SENSe1:LIA:FIR:STATe 1', self.fake_connection.get_outgoing_message())

    def test_enable_lock_in_fir(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.enable_lock_in_fir()
        self.assertIn('SENSe1:LIA:FIR:STATe 1', self.fake_connection.get_outgoing_message())

    def test_disable_lock_in_fir(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.disable_lock_in_fir()
        self.assertIn('SENSe1:LIA:FIR:STATe 0', self.fake_connection.get_outgoing_message())

    def test_setup_dc_measurement(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut_module.setup_dc_measurement()
        self.assertIn('SENSe1:MODE DC', self.fake_connection.get_outgoing_message())
        self.assertIn('SENSe1:NPLCycles 1', self.fake_connection.get_outgoing_message())

    def test_setup_ac_measurement(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut_module.setup_ac_measurement()
        self.assertIn('SENSe1:MODE AC', self.fake_connection.get_outgoing_message())
        self.assertIn('SENSe1:NPLCycles 1', self.fake_connection.get_outgoing_message())

    def test_setup_lock_in_measurement(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut_module.setup_lock_in_measurement('S2', 0.25, 'R18', 60.5, 2, True)
        self.assertIn('SENSe1:MODE LIA', self.fake_connection.get_outgoing_message())
        self.assertIn('SENSe1:LIA:RSOurce S2', self.fake_connection.get_outgoing_message())
        self.assertIn('SENSe1:LIA:TIMEconstant 0.25', self.fake_connection.get_outgoing_message())
        self.assertIn('SENSe1:LIA:ROLLoff R18', self.fake_connection.get_outgoing_message())
        self.assertIn('SENSe1:LIA:DPHase 60.5', self.fake_connection.get_outgoing_message())
        self.assertIn('SENSe1:LIA:DHARmonic 2', self.fake_connection.get_outgoing_message())
        self.assertIn('SENSe1:LIA:FIR:STATe 1', self.fake_connection.get_outgoing_message())

    def test_fetch_multiple(self):
        self.fake_connection.setup_response('2.21,5.91,2.13;No error')
        response = self.dut_module.fetch_multiple('SRANge', 'MDC', 'MY')
        self.assertEqual(response, (2.21, 5.91, 2.13))
        self.assertIn('FETCh? SRANge,1,MDC,1,MY,1', self.fake_connection.get_outgoing_message())

    def test_read_multiple(self):
        self.fake_connection.setup_response('2.21,5.91,2.13;No error')
        response = self.dut_module.read_multiple('MRANge', 'MDC', 'MPPeak')
        self.assertEqual(response, (2.21, 5.91, 2.13))
        self.assertIn('READ? MRANge,1,MDC,1,MPPeak,1', self.fake_connection.get_outgoing_message())

    def test_get_dc(self):
        self.fake_connection.setup_response('2.5;No error')
        response = self.dut_module.get_dc()
        self.assertEqual(response, 2.5)
        self.assertIn('READ:SENSe1:DC?', self.fake_connection.get_outgoing_message())

    def test_get_rms(self):
        self.fake_connection.setup_response('12.5;No error')
        response = self.dut_module.get_rms()
        self.assertEqual(response, 12.5)
        self.assertIn('READ:SENSe1:RMS?', self.fake_connection.get_outgoing_message())

    def test_get_peak_to_peak(self):
        self.fake_connection.setup_response('4.2;No error')
        response = self.dut_module.get_peak_to_peak()
        self.assertEqual(response, 4.2)
        self.assertIn('READ:SENSe1:PTPeak?', self.fake_connection.get_outgoing_message())

    def test_get_positive_peak(self):
        self.fake_connection.setup_response('2.5;No error')
        response = self.dut_module.get_positive_peak()
        self.assertEqual(response, 2.5)
        self.assertIn('READ:SENSe1:PPEak?', self.fake_connection.get_outgoing_message())

    def test_get_negative_peak(self):
        self.fake_connection.setup_response('6.32;No error')
        response = self.dut_module.get_negative_peak()
        self.assertEqual(response, 6.32)
        self.assertIn('READ:SENSe1:NPEak?', self.fake_connection.get_outgoing_message())

    def test_get_lock_in_x(self):
        self.fake_connection.setup_response('0.21;No error')
        response = self.dut_module.get_lock_in_x()
        self.assertEqual(response, 0.21)
        self.assertIn('FETCh:SENSe1:LIA:X?', self.fake_connection.get_outgoing_message())

    def test_get_lock_in_y(self):
        self.fake_connection.setup_response('0.35;No error')
        response = self.dut_module.get_lock_in_y()
        self.assertEqual(response, 0.35)
        self.assertIn('FETCh:SENSe1:LIA:Y?', self.fake_connection.get_outgoing_message())

    def test_get_lock_in_r(self):
        self.fake_connection.setup_response('2.34;No error')
        response = self.dut_module.get_lock_in_r()
        self.assertEqual(response, 2.34)
        self.assertIn('FETCh:SENSe1:LIA:R?', self.fake_connection.get_outgoing_message())

    def test_get_lock_in_theta(self):
        self.fake_connection.setup_response('62.5;No error')
        response = self.dut_module.get_lock_in_theta()
        self.assertEqual(response, 62.5)
        self.assertIn('FETCh:SENSe1:LIA:THETa?', self.fake_connection.get_outgoing_message())

    def test_get_lock_in_frequency(self):
        self.fake_connection.setup_response('5000;No error')
        response = self.dut_module.get_lock_in_frequency()
        self.assertEqual(response, 5000)
        self.assertIn('FETCh:SENSe1:LIA:FREQuency?', self.fake_connection.get_outgoing_message())

    def test_get_pll_lock_status(self):
        self.fake_connection.setup_response('0;No error')
        response = self.dut_module.get_pll_lock_status()
        self.assertEqual(response, False)
        self.assertIn('FETCh:SENSe1:LIA:LOCK?', self.fake_connection.get_outgoing_message())

    def test_get_present_questionable_status(self):
        self.fake_connection.setup_response('15')
        response = self.dut_module.get_present_questionable_status()

        self.assertEqual(response.read_error, True)
        self.assertEqual(response.unrecognized_pod_error, True)
        self.assertEqual(response.port_direction_error, True)
        self.assertEqual(response.factory_calibration_failure, True)
        self.assertEqual(response.self_calibration_failure, False)

        self.assertIn('STATus:QUEStionable:SENSe1:CONDition?', self.fake_connection.get_outgoing_message())

    def test_get_questionable_events(self):
        self.fake_connection.setup_response('10')
        response = self.dut_module.get_questionable_events()

        self.assertEqual(response.read_error, False)
        self.assertEqual(response.unrecognized_pod_error, True)
        self.assertEqual(response.port_direction_error, False)
        self.assertEqual(response.factory_calibration_failure, True)
        self.assertEqual(response.self_calibration_failure, False)

        self.assertIn('STATus:QUEStionable:SENSe1:EVENt?', self.fake_connection.get_outgoing_message())

    def test_get_questionable_event_enable_mask(self):
        self.fake_connection.setup_response('25')
        response = self.dut_module.get_questionable_event_enable_mask()

        self.assertEqual(response.read_error, True)
        self.assertEqual(response.unrecognized_pod_error, False)
        self.assertEqual(response.port_direction_error, False)
        self.assertEqual(response.factory_calibration_failure, True)
        self.assertEqual(response.self_calibration_failure, True)

        self.assertIn('STATus:QUEStionable:SENSe1:ENABle?', self.fake_connection.get_outgoing_message())

    def test_set_questionable_event_enable_mask(self):
        self.fake_connection.setup_response('No error')
        # Arguments go from LSB to MSB
        register = ssm_base_module.SSMSystemModuleQuestionableRegister(False, True, True, False, True)
        self.dut_module.set_questionable_event_enable_mask(register)
        self.assertIn('STATus:QUEStionable:SENSe1:ENABle 22', self.fake_connection.get_outgoing_message())

    def test_get_present_operation_status(self):
        self.fake_connection.setup_response('2')
        response = self.dut_module.get_present_operation_status()
        self.assertEqual(response.overload, False)
        self.assertEqual(response.settling, True)
        self.assertEqual(response.unlocked, False)
        self.assertIn('STATus:OPERation:SENSe1:CONDition?', self.fake_connection.get_outgoing_message())

    def test_get_operation_events(self):
        self.fake_connection.setup_response('7')
        response = self.dut_module.get_operation_events()
        self.assertEqual(response.overload, True)
        self.assertEqual(response.settling, True)
        self.assertEqual(response.unlocked, True)
        self.assertIn('STATus:OPERation:SENSe1:EVENt?', self.fake_connection.get_outgoing_message())

    def test_get_operation_event_enable_mask(self):
        self.fake_connection.setup_response('5')
        response = self.dut_module.get_operation_event_enable_mask()
        self.assertEqual(response.overload, True)
        self.assertEqual(response.settling, False)
        self.assertEqual(response.unlocked, True)
        self.assertIn('STATus:OPERation:SENSe1:ENABle?', self.fake_connection.get_outgoing_message())

    def test_set_operation_event_enable_mask(self):
        self.fake_connection.setup_response('No error')
        register = ssm_measure_module.SSMSystemMeasureModuleOperationRegister(False, False, True)
        self.dut_module.set_operation_event_enable_mask(register)
        self.assertIn('STATus:OPERation:SENSe1:ENABle 4', self.fake_connection.get_outgoing_message())

    def test_get_identify_state(self):
        self.fake_connection.setup_response('0')
        response = self.dut_module.get_identify_state()
        self.assertEqual(response, False)
        self.assertIn('SENSe1:IDENtify?', self.fake_connection.get_outgoing_message())

    def test_set_identify_state(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_identify_state(True)
        self.assertIn('SENSe1:IDENtify 1', self.fake_connection.get_outgoing_message())

    def test_get_frequency_range_threshold(self):
        self.fake_connection.setup_response('0.1;No error')
        response = self.dut_module.get_frequency_range_threshold()
        self.assertEqual(response, 0.1)
        self.assertIn('SENSe1:FRTHreshold?', self.fake_connection.get_outgoing_message())

    def test_set_frequency_range_threshold(self):
        self.fake_connection.setup_response('No error')
        self.dut_module.set_frequency_range_threshold(0.9)
        self.assertIn('SENSe1:FRTHreshold 0.9', self.fake_connection.get_outgoing_message())

    def test_get_self_cal_datetime(self):
        self.fake_connection.setup_response('1985,10,26,1,20,0;No error')
        response = self.dut_module.get_self_cal_datetime()
        self.assertEqual(response, datetime(1985,10,26,1,20,0))

    def test_get_self_cal_temperature(self):
        self.fake_connection.setup_response('232.778;No error')
        response = self.dut_module.get_self_cal_temperature()
        self.assertEqual(response, 232.778)


class TestSettingsProfiles(TestWithFakeSSMS):
    def test_get_summary(self):
        self.fake_connection.setup_response('"Profile description", "S1", "S2", "S3", "M1", "M2", "M3";No error')
        response = self.dut.settings_profiles.get_summary("Profile name")
        self.assertListEqual(response, ["Profile description", "S1", "S2", "S3", "M1", "M2", "M3"])

    def test_create(self):
        self.fake_connection.setup_response('No error')
        self.dut.settings_profiles.create('New profile name', 'Profile description')
        self.assertIn('PROFile:CREAte "New profile name", "Profile description"', self.fake_connection.get_outgoing_message())

    def test_get_list(self):
        self.fake_connection.setup_response('"Profile 1","Profile 2","Profile 3";No error')
        profiles = self.dut.settings_profiles.get_list()
        self.assertListEqual(profiles, ['Profile 1', 'Profile 2', 'Profile 3'])

    def test_get_list_empty(self):
        self.fake_connection.setup_response(';No error')
        profiles = self.dut.settings_profiles.get_list()
        self.assertFalse(profiles)

    def test_get_description(self):
        self.fake_connection.setup_response('"Profile description";No error')
        response = self.dut.settings_profiles.get_description("Profile name")
        self.assertEqual("Profile description", response)
        self.assertIn('PROFile:DESCription? "Profile name"', self.fake_connection.get_outgoing_message())

    def test_set_description(self):
        self.fake_connection.setup_response('No error')
        self.dut.settings_profiles.set_description("Profile name", "Updated profile description")
        self.assertIn('PROFile:DESCription "Profile name","Updated profile description"',
                      self.fake_connection.get_outgoing_message())

    def test_get_json(self):
        self.fake_connection.setup_response('"{""Property"":""Value""}";No error')
        response = self.dut.settings_profiles.get_json("Profile name")
        expected = {"Property": "Value"}
        self.assertEqual(expected, response)
        self.assertIn('PROFile:JSON? "Profile name"', self.fake_connection.get_outgoing_message())

    def test_rename(self):
        self.fake_connection.setup_response('No error')
        self.dut.settings_profiles.rename('Profile name', 'New profile name')
        self.assertIn('PROFile:REName "Profile name","New profile name"', self.fake_connection.get_outgoing_message())

    def test_update(self):
        self.fake_connection.setup_response('No error')
        self.dut.settings_profiles.update('Profile name')
        self.assertIn('PROFile:UPDate "Profile name"', self.fake_connection.get_outgoing_message())

    def test_get_valid_for_restore(self):
        self.fake_connection.setup_response('1;No error')
        response = self.dut.settings_profiles.get_valid_for_restore('Profile name')
        self.assertTrue(response)
        self.assertIn('PROFile:RESTore:VALid? "Profile name"', self.fake_connection.get_outgoing_message())

    def test_restore(self):
        self.fake_connection.setup_response('No error')
        self.dut.settings_profiles.restore('Profile name')
        self.assertIn('PROFile:RESTore "Profile name"', self.fake_connection.get_outgoing_message())

    def test_delete(self):
        self.fake_connection.setup_response('No error')
        self.dut.settings_profiles.delete('Profile name')
        self.assertIn('PROFile:DELete "Profile name"', self.fake_connection.get_outgoing_message())

    def test_delete_all(self):
        self.fake_connection.setup_response('No error')
        self.dut.settings_profiles.delete_all()
        self.assertIn('PROFile:DELete:ALL', self.fake_connection.get_outgoing_message())



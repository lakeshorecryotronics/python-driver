"""Implements functionality unique to the Lake Shore F41 and F71 Teslameters."""

from collections import namedtuple
from datetime import datetime

import iso8601

from .xip_instrument import XIPInstrument

DataPoint = namedtuple("DataPoint", ['elapsed_time', 'time_stamp',
                                     'magnitude', 'x', 'y', 'z',
                                     'field_control_set_point',
                                     'input_state'])


class Teslameter(XIPInstrument):
    """A XIP Instrument subclass that establishes Teslameter-specific parameters and methods"""

    vid_pid = [(0x1FB9, 0x0405), (0x1FB9, 0x0406)]

    def __init__(self, serial_number=None,
                 com_port=None, baud_rate=115200, flow_control=True,
                 timeout=2.0,
                 ip_address=None):
        # Call the parent init, then fill in values specific to the Teslameter
        XIPInstrument.__init__(self, serial_number, com_port, baud_rate, flow_control, timeout, ip_address)

    def stream_buffered_data(self, length_of_time_in_seconds, sample_rate_in_ms):
        """Yields a generator object for the buffered field data"""

        # Set the sample rate
        self.command("SENSE:AVERAGE:COUNT " + str(sample_rate_in_ms / 10))

        # Round the length of time to the nearest 10 milliseconds.
        length_of_time_in_seconds = round(length_of_time_in_seconds, 2)

        # Calculate the total number of samples
        total_number_of_samples = int(round(length_of_time_in_seconds * 1000 / sample_rate_in_ms, 0))
        number_of_samples = 0

        # Clear the buffer by querying it
        self.query('FETC:BUFF:DC?', check_errors=False)

        while number_of_samples <= total_number_of_samples:
            # Query the buffer.
            response = self.query('FETC:BUFF:DC?', check_errors=False)

            # Ignore the response if it contains no data
            if ';' in response:
                # Split apart the response into single data points.
                data_points = response.rstrip(';').split(';')

                for point in data_points:
                    # Split the data point along the delimiter.
                    point_data = point.split(',')

                    # Convert the time stamp into python datetime format.
                    point_data[0] = iso8601.parse_date(point_data[0])

                    # Convert the returned values from strings to floats
                    for count, _ in enumerate(point_data):
                        if count != 0:
                            point_data[count] = float(point_data[count])

                    # If the instrument does not have a field control option, insert zero as the control set point.
                    if len(point_data) == 6:
                        input_state = point_data.pop()
                        point_data.append(0.0)
                        point_data.append(input_state)

                    # Count how many samples have been collected and calculate the elapsed time.
                    number_of_samples += 1
                    elapsed_time_in_seconds = sample_rate_in_ms * number_of_samples / 1000

                    # If we have exceeded the requested number of samples, end the stream.
                    if number_of_samples > total_number_of_samples:
                        break

                    # Unpack the parsed point into a namedtuple and append it to the list
                    new_point = DataPoint(elapsed_time_in_seconds, *point_data)

                    yield new_point

    def get_buffered_data_points(self, length_of_time_in_seconds, sample_rate_in_ms):
        """Returns a list of namedtuples that contain the buffered data."""
        return list(self.stream_buffered_data(length_of_time_in_seconds, sample_rate_in_ms))

    def log_buffered_data_to_file(self, length_of_time_in_seconds, sample_rate_in_ms, file_name):
        """Creates a CSV file with the buffered data and excel-friendly timestamps."""
        # Open the file and write in header information.
        file = open(file_name + ".csv", "w")
        file.write('time elapsed,date,time,' +
                   'magnitude,x,y,z,field control set point,input state\n')

        data_stream_generator = self.stream_buffered_data(length_of_time_in_seconds, sample_rate_in_ms)

        # Parse the datetime value into a separate date and time.
        for point in data_stream_generator:
            for count, data in enumerate(point):
                if count != 1:
                    file.write(str(data) + ',')
                else:
                    file.write(datetime.strftime(data, '%m/%d/%Y') + ',' +
                               datetime.strftime(data, '%H:%M:%S.%f') + ',')
            file.write('\n')

# Author: Sebastian Merz
# Licence: GNU General Public License v3.0
# Description: script for converting binary data from a Siglent oscilloscopes and converting it into usable data
# Example:
#   from bin import bin
#   data = bin(<file_path>).convert()

import struct

class bin:
    magnitudes = [10e-24, 10e-21, 10e-18, 10e-15, 10e-12, 10e-9, 10e-6, 10e-3, 1, 10e3, 10e6, 10e9, 10e12, 10e15]
    file = ''

    def __init__(self, file):
        self.file = file

    def data_to_unit(self, data):
        result = []
        for i in range(0, int(len(data) / 16)):
            packet = data[(i+1)*16-16:(i+1)*16]
            result.append(struct.unpack('d', packet[:8])[0] * self.magnitudes[struct.unpack('i', packet[8:12])[0]])
        return result if len(result) > 1 else result[0]

    def data_to_int(self, data):
        result = []
        count = int(len(data) / 4)
        for i in range(0, count):
            packet = data[(i + 1) * 4 - 4:(i + 1) * 4]
            result.append(struct.unpack('i', packet)[0])
        return result if len(result) > 1 else result[0]


    def convert(self):
        f = open(self.file, 'rb+')
        file_data = f.read()
        channel_states = self.data_to_int(file_data[:16])
        channel_volt_division = self.data_to_unit(file_data[16:80])
        channel_offset = self.data_to_unit(file_data[80:144])
        #digital_states = self.data_to_int(file_data[144:212])
        horizontal_list = self.data_to_unit(file_data[212:244])
        wave_length = self.data_to_int(file_data[244:248])
        sample_rate = self.data_to_unit(file_data[248:264])
        #digital_wave_length = self.data_to_int(file_data[264:268])
        #digital_sample_rate = self.data_to_unit(file_data[268:284])
        #reserved = file_data[284:2048] #1764 bits reserved space
        data = file_data[2048:]
        f.close()

        print('channel_states: ', channel_states)
        print('channel_volt_division: ', channel_volt_division)
        print('channel_offset: ', channel_offset)
        #print('digital_states: ', digital_states)
        print('horizontal_list: ', horizontal_list)
        print('wave_length: ', wave_length)
        print('sample_rate: ', sample_rate)
        #print('digital_wave_length: ', digital_wave_length)
        #print('digital_sample_rate: ', digital_sample_rate)

        block_length = (1000000 if len(data) >= 14e6 or wave_length >= 1E6 else wave_length)
        block_number = int(wave_length // block_length)
        last_block_length = wave_length % block_length
        block_number = (block_number + 1 if last_block_length != 0 else block_number)
        result = []

        for block in range(0, block_number):
            if block == (block_number - 1) and last_block_length != 0:
                block_data = range(block_length * block, block_length + last_block_length)
            else:
                block_data = range(block_length * block, block_length * (block + 1))

            output = []
            for i in block_data:
                counter = 0
                volt = []
                for channel in range(0, len(channel_states)):
                    if channel_states[channel]:
                        volt_raw = int(data[i + (counter * wave_length)])
                        volt_res = (volt_raw - 128) * channel_volt_division[channel] / 25 - channel_offset[channel]
                        volt.append(float(format(volt_res, '.12f')))
                        counter += 1
                if counter > 0:
                    volt.insert(0, float(format(-horizontal_list[0] * 14 / 2 + i * (1 / sample_rate), '.12f')))
                output.append(volt)
            result.append(output)
        return result

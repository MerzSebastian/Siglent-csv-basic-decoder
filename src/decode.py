# Author: Sebastian Merz
# Licence: GNU General Public License v3.0
# Description: Script for decoding digital signal from a single or multiple CSV files which are expored from a Siglent oscilloscope (bin dump => bin2csv)
# Parameter: decode.py <input_file_or_folder> <output_folder>
# Example: decode.py ../test/samples ./

import pandas as pd
import sys
import time
import os as os
from datetime import datetime


def decode_normalized_data(val_x, val_y, single_pulse_length):
    decoded = []
    for i in range(1, len(val_x) - 2, 2):
        current_pulse_length = val_x[i + 2] - val_x[i]
        if val_y[i] == 1:
            for a in range(round(current_pulse_length / single_pulse_length)):
                decoded.append(1)
        else:
            for a in range(round(current_pulse_length / single_pulse_length)):
                decoded.append(0)
    return decoded


headers = ['Second', 'Volt']
filePaths = []
if os.path.isdir(sys.argv[1]):
    for filename in os.listdir(sys.argv[1]):
        filePaths.append(sys.argv[1] + '/' + filename)
else:
    filePaths.append(sys.argv[1])

result = ""
lastTime = time.perf_counter()
startTime = time.perf_counter()
for file in filePaths:
    print("# # # # # # # # # # # # # # # # # # # # # #")
    print("# Reading file", file, "...")
    data = pd.read_csv(file, names=headers, skiprows=6)
    print("# # Elapsed time:", round((time.perf_counter() - lastTime)*1000), "ms")
    lastTime = time.perf_counter()

    print("# Calculating threshold and cleaning data...")
    threshold = data['Volt'].max() / 2
    data['Volt'] = [(1 if i > threshold else 0) for i in data['Volt']]
    print("# # Elapsed time:", round((time.perf_counter() - lastTime)*1000), "ms")
    print("# # Threshold:", threshold, "Volt")
    lastTime = time.perf_counter()

    print("# Removing doubled data points...")
    x = []
    y = []
    for i in range(1, len(data) - 1):
        if data['Volt'][i - 1] != data['Volt'][i] and data['Volt'][i + 1] == data['Volt'][i]:
            x.extend([data['Second'][i], data['Second'][i]])
            y.extend([1 - data['Volt'][i], data['Volt'][i]])
    print("# # Elapsed time:", round((time.perf_counter() - lastTime)*1000), "ms")
    print("# # Old data points len:", len(data))
    print("# # New data points len:", len(x))
    lastTime = time.perf_counter()

    print("# Shifting time value so it starts at 0...")
    x = [x[i] - min(x) for i in range(len(x))]
    print("# # Elapsed time:", round((time.perf_counter() - lastTime)*1000), "ms")
    lastTime = time.perf_counter()

    print("# Getting shortest pulse length...")
    singlePulseLength = min([abs(x[i] - x[i + 2]) for i in range(len(y) - 2)])
    print("# # Elapsed time:", round((time.perf_counter() - lastTime)*1000), "ms")
    print("# # Calculated shorted pulse length:", singlePulseLength)
    lastTime = time.perf_counter()

    print("# Decoding data...")
    decoded_data = decode_normalized_data(x, y, singlePulseLength)
    decoded_string_data = ''.join(str(val) for val in decoded_data)
    result += decoded_string_data + '\n'
    print("# # Elapsed time:", round((time.perf_counter() - lastTime)*1000), "ms")
    print("# # Decoded data:", decoded_string_data)
    lastTime = time.perf_counter()

print("# # # # # # # # # # # # # # # # # # # # # #")
print("# Writing output file...")
f = open(sys.argv[2] + str(datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".txt", "x")
f.write(result)
f.close()
print("# # Overall time:", round((time.perf_counter() - startTime)*1000), "ms")
print("# # # # # # # # # # # # # # # # # # # # # #")

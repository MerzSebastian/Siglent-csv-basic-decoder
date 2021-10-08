# Author: Sebastian Merz
# Licence: GNU General Public License v3.0
# Description: Script for decoding digital signal from a single or multiple CSV files which are expored from a Siglent oscilloscope (bin dump => bin2csv)
# Parameter: decode.py <input_file_or_folder> <output_folder>
# Example: decode.py ../test/samples ./
import datetime as datetime
import pandas as pd
import sys
import time
import os as os
from bin import bin
from datetime import datetime
import json
import statistics


def calculate_error(current_pulse_length, single_pulse_length, pulse_count):
    return [(current_pulse_length % (pulse_count * single_pulse_length)) for _ in range(pulse_count)] #maybe calculating error outside of foreach is more efficient ? i dont know. should be fine


def decode_normalized_data(val_x, val_y, single_pulse_length):
    data = []
    error = []
    for i in range(1, len(val_x) - 2, 2):
        current_pulse_length = val_x[i + 2] - val_x[i]
        pulse_count = round(current_pulse_length / single_pulse_length)
        error += calculate_error(current_pulse_length, single_pulse_length, pulse_count)
        data += [1 if val_y[i] else 0 for _ in range(pulse_count)]
    return data, error


def normalize_data():
    print("test")


def reformat_raw_data(data):
    x = [data[0][i][0] for i in range(len(data[0]))]
    y = [data[0][i][1] for i in range(len(data[0]))]
    print(data[0] == data[1], "WTF ???????")  # WTF ???????
    return x, y


def main():
    filePaths = ([os.path.join(sys.argv[1], f) for f in os.listdir(sys.argv[1]) if f.endswith('.bin')] if os.path.isdir(sys.argv[1]) else [sys.argv[1]])

    result = {}
    lastTime = time.perf_counter()
    startTime = time.perf_counter()
    for file in filePaths:
        print("# # # # # # # # # # # # # # # # # # # # # #")
        print("Reading file", file, "...")

        xx = []
        yy = []
        data = bin(file).convert()[0]

        x, y = reformat_raw_data(bin(file).convert()[0])
        xx = x
        yy = y

        print("Elapsed time:", round((time.perf_counter() - lastTime)*1000), "ms")
        lastTime = time.perf_counter()

        print("Calculating threshold and cleaning data...")
        threshold = max(yy) / 2
        yy = [(True if i > threshold else False) for i in yy]
        print("Threshold:", threshold, "Volt")
        print("Elapsed time:", round((time.perf_counter() - lastTime)*1000), "ms")
        lastTime = time.perf_counter()

        print("Removing doubled data points...")
        x = []
        y = []
        for i in range(1, len(xx) - 1):
            if yy[i - 1] != yy[i] and yy[i + 1] == yy[i]:
                x.extend([xx[i], xx[i]])
                y.extend([1 - yy[i], yy[i]])
        print("Elapsed time:", round((time.perf_counter() - lastTime)*1000), "ms")
        lastTime = time.perf_counter()

        print("Shifting time value so it starts at 0...")
        x = [x[i] - min(x) for i in range(len(x))]
        print("Elapsed time:", round((time.perf_counter() - lastTime)*1000), "ms")
        lastTime = time.perf_counter()

        print("Getting shortest pulse length...")
        singlePulseLength = min([abs(x[i] - x[i + 2]) for i in range(len(y) - 2)])
        print("Shorted pulse length:", singlePulseLength)
        print("Elapsed time:", round((time.perf_counter() - lastTime)*1000), "ms")
        lastTime = time.perf_counter()

        print("Decoding data...")
        decoded_data, gError = decode_normalized_data(x, y, singlePulseLength)
        decoded_string_data = ''.join(str(val) for val in decoded_data)
        print("Decoded data:", decoded_string_data)
        print("Elapsed time:", round((time.perf_counter() - lastTime)*1000), "ms")
        lastTime = time.perf_counter()

        #THROW ERROR IF length of < and x are not the same

        result[os.path.basename(file)] = {
            "date": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "detectionThreshold": format(threshold, '.12f'),
            "singlePulseLength": format(singlePulseLength, '.12f'),
            "dataPointsRaw": len(data[0]),
            "maxError": format(max(gError), '.12f'),
            "avgError": format(statistics.mean(gError), '.12f'),
            "data": {
                "size": len(decoded_string_data),
                "bin": decoded_string_data,
                "times": [format(x, '.12f') for x in x],
                "errors": [format(e, '.12f') for e in gError]
            }
        }

    print("# # # # # # # # # # # # # # # # # # # # # #")
    print("Writing output file...")
    path = os.path.join(sys.argv[2], str(datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".json")
    f = open(path, "x")
    f.write(json.dumps(result))
    f.close()
    print("Written file:", path)
    print("Overall time:", round((time.perf_counter() - startTime)*1000), "ms")
    print("# # # # # # # # # # # # # # # # # # # # # #")

if __name__ == "__main__":
    main()

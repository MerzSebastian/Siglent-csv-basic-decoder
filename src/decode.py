# Author: Sebastian Merz
# Licence: GNU General Public License v3.0
# Description: Script for decoding digital signal from a single or multiple CSV files which are expored from a Siglent oscilloscope (bin dump => bin2csv)
# Parameter: decode.py <input_file_or_folder> <output_folder>
# Example: decode.py ../test/samples ./

import time
import os as os
from bin import bin
from webfetch import webfetch
import ui
from datetime import datetime
import json
import statistics
import argparse

start_time = 0
last_time = 0


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


def reformat_raw_data(data):
    x = [data[i][0] for i in range(len(data))]
    y = [data[i][1] for i in range(len(data))]
    return x, y


def remove_redundant_data_points(x, y):
    #x = [([x[i], x[i]]) for i in range(1, len(x) - 1) if (y[i - 1] != y[i]) and (y[i + 1] == y[i])]
    #y = [([1 - y[i], y[i]]) for i in range(1, len(x) - 1) if (y[i - 1] != y[i]) and (y[i + 1] == y[i])]
    xx = []
    yy = []
    for i in range(1, len(x) - 1):
        if y[i - 1] != y[i] and y[i + 1] == y[i]:
            xx.extend([x[i], x[i]])
            yy.extend([1 - y[i], y[i]])
    return xx, yy


def write_output(path, data):
    name = str(datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".json"
    _path = os.path.join(path, name)
    f = open(_path, "x")
    f.write(json.dumps(data))
    f.close()
    return name


def time_round():
    global last_time
    print("Elapsed time:", round((time.perf_counter() - last_time)*1000), "ms")
    last_time = time.perf_counter()


def time_start():
    global last_time
    global start_time
    last_time = time.perf_counter()
    start_time = time.perf_counter()


def time_overall():
    global start_time
    print("Overall elapsed time:", round((time.perf_counter() - start_time) * 1000), "ms")


def calculate(file):
    print("# # # # # # # # # # # # # # # # # # # # # #")
    print("Reading and converting binary data", file, "...")
    raw_data = bin(file).convert()[0] #doesnt work for multiple channels, have to test if channel 2, 3 and 4 works. only testet first i think
    x, y = reformat_raw_data(raw_data)
    global ui_raw_data
    ui_raw_data = [x, y]
    time_round()

    print("Calculating threshold...")
    threshold = max(y) / 2
    print("Threshold:", threshold, "Volt")
    time_round()

    print("Correct time offset...")
    y = [(True if i > threshold else False) for i in y]
    time_round()

    print("Removing doubled data points...")
    x, y = remove_redundant_data_points(x, y)
    time_round()

    print("Shifting time value so it starts at 0...")
    x = [x[i] - min(x) for i in range(len(x))]
    time_round()
    global ui_cleaned_data
    ui_cleaned_data = [x, y]

    print("Getting shortest pulse length...")
    single_pulse_length = min([abs(x[i] - x[i + 2]) for i in range(len(y) - 2)])
    print("Shortest pulse length:", format(single_pulse_length, '.12f'))
    time_round()

    print("Decoding data...")
    decoded_data, error = decode_normalized_data(x, y, single_pulse_length)
    decoded_string_data = ''.join(str(val) for val in decoded_data)
    print("Decoded data:", decoded_string_data)
    time_round()

    return {
        "date": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        "detectionThreshold": format(threshold, '.12f'),
        "singlePulseLength": format(single_pulse_length, '.12f'),
        "dataPointsRaw": len(raw_data),
        "maxError": format(max(error), '.12f'),
        "avgError": format(statistics.mean(error), '.12f'),
        "data": {
            "size": len(decoded_string_data),
            "bin": decoded_string_data,
            "times": [format(x, '.12f') for x in x],
            "errors": [format(e, '.12f') for e in error]
        }
    }


def getArguments():
    parser = argparse.ArgumentParser(description='Decoding NRZ-L-Code from Siglents binary file format into json. If you want to automatically download multiple shots over the Web-UI you have to fill the -d and -u parameters.')
    parser.add_argument('-i', '--input', action='store', help='Binary input file/folder (example: ./myfile.bin | Info: Define a empty folder for temp files if using webfetch downloading)', required=True)
    parser.add_argument('-o', '--output', action='store', help='Output folder for json result (default: ./ | example: ./output)')
    parser.add_argument('-g', '--graph', action='store_true', help='Show graph after decoding (info: Only works when decoding a single file)')
    # Additional parameter for webfetch, only use of driver and ui are defined
    parser.add_argument('-d', '--driver', action='store', help='Path to Chromedriver/Geckodriver (example: ./chromedriver.exe)')
    parser.add_argument('-u', '--url', action='store', help='URL to Siglents Web-UI (example: 192.168.178.123/dsadasdad)')
    parser.add_argument('-r', '--repetitions', action='store', help='Number of downloads (default: 1)')
    parser.add_argument('-p', '--pause', action='store', help='Pause between each download in seconds (default: 0)')
    return parser.parse_args()


def main():
    time_start()
    args = getArguments()

    #Check if file are provided by webfetch
    if args.driver and args.url:
        webfetch(args.input, args.driver, args.url, args.repetitions, args.pause) # maybe return downloaded files, should be better so old files doesnt get decoded again

    #Get all files
    file_paths = ([os.path.join(args.input, f) for f in os.listdir(args.input) if f.endswith('.bin')] if os.path.isdir(args.input) else [args.input])
    result = {}
    for file in file_paths:
        result[os.path.basename(file)] = calculate(file)

    print("# # # # # # # # # # # # # # # # # # # # # #")
    print("Writing output file...")
    path = write_output(args.output if args.output else "./", result)
    print("Written file:", path)
    time_overall()
    print("# # # # # # # # # # # # # # # # # # # # # #")
    if len(file_paths) is 1 and args.graph:
        ui.showTwoGraphs(ui_raw_data, ui_cleaned_data)


if __name__ == "__main__":
    main()

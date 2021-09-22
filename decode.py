import pandas as pd
import sys
import os as os
from datetime import datetime

def decodeNormalizedData(x, y):
    decoded = []
    for i in range(1, len(x) - 2, 2):
        currentPulseLength = x[i + 2] - x[i]
        if y[i] == 1:
            for data in range(round(currentPulseLength / singlePulseLength)):
                decoded.append("1")
        else:
            for data in range(round(currentPulseLength / singlePulseLength)):
                decoded.append("0")
    return ''.join(decoded)

headers = ['Second', 'Volt']
csvData = []
if os.path.isdir(sys.argv[1]):
    for filename in os.listdir(sys.argv[1]):
        print(sys.argv[1] + '/' + filename)
        csvData.append(pd.read_csv(sys.argv[1] + '/' + filename, names=headers, skiprows=6))
else:
    csvData.append(pd.read_csv(sys.argv[1], names=headers, skiprows=6))

result = ""
for df in csvData:
    ##remove noise by converting to 0 and 1 dependend on a threshold which is calculated by getting the highest volt value and splitting it into 2
    threshold = df['Volt'].max() / 2
    df['Volt'] = [(1 if i > threshold else 0) for i in df['Volt']]

    ##remove unneccesary values
    clean_x = []
    clean_y = []
    for i in range(1, len(df) - 1):
        if df['Volt'][i - 1] != df['Volt'][i] and df['Volt'][i + 1] == df['Volt'][i]:
            clean_x.append(df['Second'][i])
            clean_y.append(1 - df['Volt'][i])

            clean_x.append(df['Second'][i])
            clean_y.append(df['Volt'][i])

    ##set time offset so it starts at 0 on the x axis, nicer to look at
    clean_x = [clean_x[i] - min(clean_x) for i in range(len(clean_x))]
    ##get shortest pulse and take it as single 1, works for now
    singlePulseLength = min([abs(clean_x[i] - clean_x[i + 2]) for i in range(len(clean_y) - 2)])

    print("Single pulse length:", singlePulseLength)
    print("decoded data:", decodeNormalizedData(clean_x, clean_y))
    result += decodeNormalizedData(clean_x, clean_y) + '\n'


f = open(str(datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".txt", "x")
f.write(result)
f.close()

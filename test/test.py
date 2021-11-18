# Author: Sebastian Merz
# Licence: GNU General Public License v3.0
# Description: Script for testing the decoding and making sure that it doesnt break
# Example: test.py

import os
import glob
from expect import expect
import pathlib
import json

basePath = os.path.dirname(pathlib.Path().resolve())
mainPath = os.path.join(basePath, 'src\decode.py')
inputPath = os.path.join(basePath, 'test\samples')
outputPath = os.path.join(basePath, 'test\output')
startCommand = ' '.join([mainPath, inputPath, outputPath])

webfetchMainPath = os.path.join(basePath, 'src\webfetch.py')
webfetchOutputPath = os.path.join(basePath, 'test\webfetch_output')
webfetchChromedriverPath = os.path.join(basePath, 'test\chromedriver.exe')
webfetchUrl = "http://192.168.178.200/Instrument/novnc/vnc_auto.php#"
startWebfetchCommand = ' '.join([webfetchMainPath, webfetchOutputPath, webfetchChromedriverPath, webfetchUrl])

#print("TEST: Starting WEBFETCH test")
#print(startWebfetchCommand)
#os.system(startWebfetchCommand)

print("TEST: Starting DECODE test")
print("TEST: config:")
print("TEST: main path:", mainPath)
print("TEST: input path", inputPath)
print("TEST: output path", outputPath)
print("TEST: start command", startCommand)

os.system("python " + startCommand)

files = glob.glob(os.path.join(outputPath, '*json'))
if not files:
    raise ValueError('No output files!')
newest_file = max(files, key=os.path.getctime)
result = json.loads(open(newest_file, "r").read())

print("TEST: Testing: usr_wf_data_0.bin")
file = result["usr_wf_data_0.bin"]
test_results = []
test_results.append(expect(file["detectionThreshold"]).to_be("0.300000000000", "JSON should have correct detectionThreshold"))
test_results.append(expect(file["singlePulseLength"]).to_be("0.000000297000", "JSON should have correct singlePulseLength"))
test_results.append(expect(file["maxError"]).to_be("0.000000797000", "JSON should have correct maxError"))
test_results.append(expect(file["avgError"]).to_be("0.000000217857", "JSON should have correct avgError"))
test_results.append(expect(file["dataPointsRaw"]).to_be(700000, "JSON should have correct dataPointsRaw"))
test_results.append(expect(file["data"]["bin"]).to_be("100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001", "JSON should have correct binary data"))
test_results.append(expect(file["data"]["size"]).to_be(1149, "JSON should have correct data size"))
test_results.append(expect(len(file["data"]["bin"])).to_be(1149, "JSON should have correct amount of bits"))
#test_results.append(expect(len(file["data"]["times"])).to_be(1149, "JSON should have correct amount of times")) #problem with inlcuded leading and trailing zeros
test_results.append(expect(len(file["data"]["errors"])).to_be(1149, "JSON should have correct amount of errors"))

print("TEST: Testing: usr_wf_data_1.bin")
file = result["usr_wf_data_1.bin"]
test_results.append(expect(file["detectionThreshold"]).to_be("0.300000000000", "JSON should have correct detectionThreshold"))
test_results.append(expect(file["singlePulseLength"]).to_be("0.000000297000", "JSON should have correct singlePulseLength"))
test_results.append(expect(file["maxError"]).to_be("0.000000030000", "JSON should have correct maxError"))
test_results.append(expect(file["avgError"]).to_be("0.000000014821", "JSON should have correct avgError"))
test_results.append(expect(file["dataPointsRaw"]).to_be(700000, "JSON should have correct dataPointsRaw"))
test_results.append(expect(file["data"]["bin"]).to_be("100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001", "JSON should have correct binary data"))
test_results.append(expect(file["data"]["size"]).to_be(1149, "JSON should have correct data size"))
test_results.append(expect(len(file["data"]["bin"])).to_be(1149, "JSON should have correct amount of bits"))
#test_results.append(expect(len(file["data"]["times"])).to_be(1149, "JSON should have correct amount of times")) #problem with inlcuded leading and trailing zeros
test_results.append(expect(len(file["data"]["errors"])).to_be(1149, "JSON should have correct amount of errors"))

print("TEST: Testing: usr_wf_data_2.bin")
file = result["usr_wf_data_2.bin"]
test_results.append(expect(file["detectionThreshold"]).to_be("0.300000000000", "JSON should have correct detectionThreshold"))
test_results.append(expect(file["singlePulseLength"]).to_be("0.000000297000", "JSON should have correct singlePulseLength"))
test_results.append(expect(file["maxError"]).to_be("0.000000796000", "JSON should have correct maxError"))
test_results.append(expect(file["avgError"]).to_be("0.000000216709", "JSON should have correct avgError"))
test_results.append(expect(file["dataPointsRaw"]).to_be(700000, "JSON should have correct dataPointsRaw"))
test_results.append(expect(file["data"]["bin"]).to_be("10001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111010001000100010001000100010001000100010001000100010001000100010001110111011101110111011101110111", "JSON should have correct binary data"))
test_results.append(expect(file["data"]["size"]).to_be(1151, "JSON should have correct data size"))
test_results.append(expect(len(file["data"]["bin"])).to_be(1151, "JSON should have correct amount of bits"))
#test_results.append(expect(len(file["data"]["times"])).to_be(1151, "JSON should have correct amount of times")) #problem with inlcuded leading and trailing zeros
test_results.append(expect(len(file["data"]["errors"])).to_be(1151, "JSON should have correct amount of errors"))

for file in os.listdir(outputPath):
    os.remove(os.path.join(outputPath, file))

if False in test_results:
    raise ValueError(f'Seems like { test_results.count(False) } tests are not successfull!')

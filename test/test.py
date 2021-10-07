# Author: Sebastian Merz
# Licence: GNU General Public License v3.0
# Description: Script for testing the decode.py script and making sure that it doesnt break
# Example: test.py

import os
import glob
from expect import Expect
import pathlib
import json

basePath = os.path.dirname(pathlib.Path().resolve())
mainPath = os.path.join(basePath, 'src\decode.py')
inputPath = os.path.join(basePath, 'test\samples')
outputPath = os.path.join(basePath, 'test\output')
expectedPath = os.path.join(inputPath, 'expected.json')
startCommand = ' '.join([mainPath, inputPath, outputPath])

print("Starting test")
print("config:")
print("main path:", mainPath)
print("input path", inputPath)
print("output path", outputPath)
print("start command", startCommand)

os.system(startCommand)
files = glob.glob(os.path.join(outputPath, '*json'))
if not files:
    raise ValueError('No output files!')
newest_file = max(files, key=os.path.getctime)
result = json.loads(open(newest_file, "r").read())
expected = json.loads(open(expectedPath, "r").read())

for i in range(len(expected)):
    Expect(result[i]["data"]).to_be(expected[i]["data"], f"Should convert file: {result[i]['filename']}")
Expect(len(result)).to_be(len(expected), "Should have the same amount of data")

for file in os.listdir(outputPath):
    os.remove(os.path.join(outputPath, file))

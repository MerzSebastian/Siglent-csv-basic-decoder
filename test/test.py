# Author: Sebastian Merz
# Licence: GNU General Public License v3.0
# Description: Script for testing the decode.py file and making sure that it doesnt break
# Example: test.py

import os
import glob
from expect import Expect

os.system('python ../src/decode.py ./samples ./output/')

files = glob.glob(r'./output/*txt')
if not files:
    raise ValueError('No output files!')
newest_file = max(files, key=os.path.getctime)
result = open(newest_file, "r").read()
expected = open("expected.txt", "r").read()

Expect(result).to_be(expected)
for f in os.listdir("./output"):
    os.remove("./output/" + f)

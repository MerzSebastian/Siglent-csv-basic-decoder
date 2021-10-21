# Author: Sebastian Merz
# Licence: GNU General Public License v3.0
# Description: Script to automate downloading binary data from Siglent web/control UI
# Example: webfetch.py <output_folder_path> <chrome_driver_path> <web_control_url> <download_sample_count> <delay_between_downloads>

import os
import sys
from selenium import webdriver
import time
import re

output_folder = sys.argv[1]
chrome_driver = sys.argv[2]
web_ui_url = sys.argv[3]
repeats = sys.argv[4] if len(sys.argv) == 5 else 1
pause = sys.argv[5] if len(sys.argv) == 6 else 0

matched_files = [file for file in os.listdir(output_folder) if re.search("(?<=usr_wf_data)(.*)(?=.bin)", file)]

#Setting up chrome options like download folder
preferences = {"download.default_directory": output_folder}
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", preferences)
#chromeOptions.add_argument("--headless")

#Starting Chrome
driver = webdriver.Chrome(chrome_driver, options=chromeOptions)
driver.get(web_ui_url)

#Manipulate UI so everything is clickable
driver.execute_script("document.getElementById('main_right').style.display = 'block';")
driver.execute_script("document.getElementById('noVNC_main').style.width = '100%';")
for _ in repeats:
    #Click download button
    driver.find_element_by_xpath('//button[text()="Waveform Save"]').click()

    #Wait for Chrome to finish downloading and close
    #Need to implement timeout so it doesnt wait forever when it does not work
    while len([file for file in os.listdir(output_folder) if re.search("(?<=usr_wf_data)(.*)(?=.bin)", file)]) == len(matched_files):
        time.sleep(1)
    time.sleep(pause)
driver.close()


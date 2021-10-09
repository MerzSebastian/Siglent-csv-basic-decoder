import os
import sys
from selenium import webdriver
import time
import re

output_folder = sys.argv[1]
chrome_driver = sys.argv[2]
web_ui_url = sys.argv[3]

matched_files = [file for file in os.listdir(output_folder) if re.search("(?<=usr_wf_data)(.*)(?=.bin)", file)]

#Setting up chrome options like download folder
preferences = {"download.default_directory": output_folder}
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", preferences)
#chromeOptions.add_argument("--headless")
driver = webdriver.Chrome(chrome_driver, options=chromeOptions)

#Starting Chrome
driver.get(web_ui_url)

#Manipulate UI so everything is clickable
driver.execute_script("document.getElementById('main_right').style.display = 'block';")
driver.execute_script("document.getElementById('noVNC_main').style.width = '100%';")

#Click download button
driver.find_element_by_xpath('//button[text()="Waveform Save"]').click()

#Wait for Chrome to finish downloading and close
while len([file for file in os.listdir(output_folder) if re.search("(?<=usr_wf_data)(.*)(?=.bin)", file)]) == len(matched_files):
    time.sleep(1)
driver.close()

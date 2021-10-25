
# Digital data decoder for Siglent Oscilloscopes

This is a little script for converting digital data which you captured with you're Siglent oscilloscope (CSV data) into binary format



## Install
```bash
pip install -r requirements.txt
```

## Usage
#### Convert binary file or folder
```bash
decode.py <input_file_or_folder> <output_folder>
```
| Parameter  | Description |
| ------------- | ------------- |
| input_file_or_folder  | File or folder which includes binary files |
| output_folder  | Folder in which the json result is saved (default: ./) |

#### Automated downloading from Web-UI
```bash
webfetch.py <output_folder> <path_to_chromedriver> <web_ui_ip_address> <repititions> <pause_between_downloads_in_seconds>
```
| Parameter  | Description |
| ------------- | ------------- |
| output_folder | Folder in which the downloaded binary file/s is/are saved |
| path_to_chromedriver | Path to fitting chromedriver executable |
| web_ui_ip_address | IP of Web-UI |
| repititions | Number of downloads (default: 1) |
| pause_between_downloads_in_seconds | Pause between each download (default: 0) |

## Examples
#### Simple binary to digital conversion
Decoding analog data
```bash
decode.py ./bin_files ./output
```

#### Simple automated download
This will download a single binary file trough the Web-UI
```bash
webfetch.py ./output ./chromedriver.exe 192.168.178.200
```

#### Advanced automated download
This will download 15 binary file trough the Web-UI without any pause in between downloads. 
After the download is finished the next one will start immediately
```bash
webfetch.py ./output ./chromedriver.exe 192.168.178.200 0 15
```

#### Combine command
The following command downloads 15 binary files and decodes them at the end 
```bash
webfetch.py ./output_webfetch ./chromedriver.exe 192.168.178.200 0 15 && decode.py ./output_webfetch ./output_decoded
```

## Output file
Info: There is currently a bug with the amount of times there are saved. Gets fixed when UI functionality gets implemented
Json schema of the output file:
<details>
<summary>show 'code'</summary>
<p>



```{
  "type": "object",
  "required": [],
  "properties": {
    "my_file.bin": {
      "type": "object",
      "required": [],
      "properties": {
        "date": {
          "type": "string",
          "description": "time and date of execution"
        },
        "detectionThreshold": {
          "type": "string",
          "description": "Voltage threshold which determents if the signal is a 1 or a 0"
        },
        "singlePulseLength": {
          "type": "string",
          "description": "Shortest recorded pulse length (used to define a single bit)"
        },
        "dataPointsRaw": {
          "type": "number",
          "description": "amount of datapoints to begin with"
        },
        "maxError": {
          "type": "string",
          "description": "maximal rounding error when detecting amount of bits"
        },
        "avgError": {
          "type": "string",
          "description": "average rounding error when detecting amount of bits"
        },
        "data": {
          "type": "object",
          "required": [],
          "properties": {
            "size": {
              "type": "number",
	          "description": "Amount of bits in decoded binary result"
            },
            "bin": {
              "type": "string",
	          "description": "Decoded binary result"
            },
            "times": {
              "type": "array",
	          "description": "Array with times for each decoded bit",
              "items": {
                "type": "string"
              }
            },
            "errors": {
              "type": "array",
	          "description": "Array with the rounding error for each decoded bit",
              "items": {
                "type": "string"
              }
            }
          }
        }
      }
    }
  }
}
```
</p>
</details>


## Developer info
### Binary file format
The following image represent the base structure of the binary file format.<br/>
![ ](/documentation/siglent_sds1000x_bin_file_format.drawio.svg)

In this section we deal with the flow of the main functions of the script
#### The cleanup process
* Get the highest value from the data and divide it by two to determent the threshold for detecting HIGH and LOW values
* Normalizing data by replacing everything over the threshold as 1 and under as 0
* Remove doubled values

#### Decoding
Info: It has to include at least 1 single bit transmission for correct decoding.
* Searching for the quickest change between HIGH and LOW and use it as the value for a single bit (Example: 2.99998mS/bit)
* When detecting more than one bit, it divides the value by the single bit value and rounding it to get the detected amount of bits. (Example: 6.1005mS / 2.99998mS = 2,033514 = 2)


#### Web fetcher
This is a simple little script which uses selenium to automatically download binary files. <br/>
To use this script you need to get the fitting [ChromeDriver](https://chromedriver.chromium.org/downloads)

#### Tests
Script for testing purposes. Its functional but nothing more ^^
I normally would would use this while development to monitor if i broke some core functionality. <br/>
```test.py``` <br/>
if you want to test the web fetching you need to edit the following property inside the test.py script: 
```webfetchUrl```<br/>
Example output:<br/>
![ ](/documentation/test_result_example.png)




<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
OLD

# Table of Contents
1. [How to use](#how-to)
2. [Output file](#output)
3. [Components](#components)
    1. [Binary converter](#binary)
    2. [Decoder](#decode)
    3. [Web fetcher](#fetcher)
    4. [Tests](#tests)




## How to use
* Get a nice single shot of all the data you want to decode.<br/>
![ ](/documentation/siglent_sds1000x.png)
* Save the shot as a binary on a USB stick and transfer it to your pc or download it directly over the Web Control over your browser (Waveform save)<br/>
![ ](/documentation/siglent_sds1000x_save.png)
* Drag and Drop your single file or folder with multiple files onto the decode.py script to start the decoding process
* Alternatively you can use the following command to start the script via the command line <br/>
```decode.py <input_file_or_folder> <output_folder>```<br/>
![ ](/documentation/output.png)
* If you dont want to manually download the binary files you can use the integrated web fetch functionality. For a single shot do the following.
These functions are currently not integrated into each other. so for the time being its recommendet to use it like this 
(Info: the output_folder of the webfetch script should be the same as the input_file_or_folder path from the decode script)<br/>
```webfetch.py <output_folder> <path_to_chromedriver> <web_ui_ip_address> && decode.py <input_file_or_folder> <output_folder>```
* If you want to download and process multiple binary files so that you can for example differentiate which bits are constant/not changing you can use the following command:<br/>
```webfetch.py <output_folder> <path_to_chromedriver> <web_ui_ip_address> <repititions> <pause_between_downloads_in_seconds> && decode.py <input_file_or_folder> <output_folder>```
* After the script is finished it should create a json file which contains the decoded data and additional information in your specified folder. 
If you used drag and drop it will use the current directory<br/>


# ToDo
* Startup option for exporting the cleaned up data
* Startup option for showing diagrams in app
* ~~Add Siglent binary decoder, so you don't need two scripts~~
* ~~Add error rate to console output~~ => added to json output
* Refactor debugging output
* ~~Change format for saving data - json or csv~~ => json
* parallelize decoding of multiple files

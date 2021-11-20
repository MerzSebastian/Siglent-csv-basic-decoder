[![CircleCI](https://circleci.com/gh/MerzSebastian/Siglent-csv-basic-decoder.svg?style=svg)](https://circleci.com/gh/MerzSebastian/Siglent-csv-basic-decoder)
# SigToDig - Siglent Analog to Digital
Program for decoding analog data (NRZ-L-Code) captured by a Siglent oscilloscope (file format: binary) into a json file which contains the decoded binary

## Usage
#### Get latest version
Download the latest version which you can find [here](https://github.com/MerzSebastian/Siglent-csv-basic-decoder/releases).
#### Convert binary file or folder
```bash
decode.exe
```
| Parameter | Description |
| ------------- | ------------- |
| input_file_or_folder | File or folder which includes binary files |
| output_folder | Folder in which the json result is saved (default: ./) |

#### Automated downloading from Web-UI
```bash
webfetch.exe
```
| Parameter | Description |
| ------------- | ------------- |
| output_folder | Folder in which the downloaded binary file/s is/are saved |
| path_to_chromedriver | Path to chromedriver executable |
| web_ui_ip_address | IP of Web-UI |
| repetitions | Number of downloads (default: 1) |
| pause_between_downloads_in_seconds | Pause between each download (default: 0) |

## Examples
### Simple binary to digital conversion
Decoding analog data
```bash
decode.exe ./bin_files ./output
```
Sample console output
![ ](/documentation/output.png)
Sample JSON output
```json
SPACEHOLDER
```

### Simple automated download
This will download a single binary file through the Web-UI
```bash
webfetch.exe ./output ./chromedriver.exe 192.168.178.200
```

### Advanced automated download
This will download 15 binary files through the Web-UI without any pause in between downloads.
After the download is finished the next one will start immediately.
```bash
webfetch.exe ./output ./chromedriver.exe 192.168.178.200 0 15
```

### Combine command
The following command downloads 15 binary files and decodes them at the end.
```bash
webfetch.py ./output_webfetch ./chromedriver.exe 192.168.178.200 0 15 && decode.py ./output_webfetch ./output_decoded
```

## Output file
Info: There is currently a bug with the amount of times there are saved. Gets fixed when UI functionality gets implemented

Json schema of the output file:

show JSON


```json
{
   "type":"object",
   "required":[
      
   ],
   "properties":{
      "my_file.bin":{
         "type":"object",
         "required":[
            
         ],
         "properties":{
            "date":{
               "type":"string",
               "description":"time and date of execution"
            },
            "detectionThreshold":{
               "type":"string",
               "description":"Voltage threshold which determents if the signal is a 1 or a 0"
            },
            "singlePulseLength":{
               "type":"string",
               "description":"Shortest recorded pulse length (used to define a single bit)"
            },
            "dataPointsRaw":{
               "type":"number",
               "description":"amount of datapoints to begin with"
            },
            "maxError":{
               "type":"string",
               "description":"maximal rounding error when detecting amount of bits"
            },
            "avgError":{
               "type":"string",
               "description":"average rounding error when detecting amount of bits"
            },
            "data":{
               "type":"object",
               "required":[
                  
               ],
               "properties":{
                  "size":{
                     "type":"number",
                     "description":"Amount of bits in decoded binary result"
                  },
                  "bin":{
                     "type":"string",
                     "description":"Decoded binary result"
                  },
                  "times":{
                     "type":"array",
                     "description":"Array with times for each decoded bit",
                     "items":{
                        "type":"string"
                     }
                  },
                  "errors":{
                     "type":"array",
                     "description":"Array with the rounding error for each decoded bit",
                     "items":{
                        "type":"string"
                     }
                  }
               }
            }
         }
      }
   }
}
```




## Developer guide
### Install requirements
```bash
pip install -r requirements.txt
```
### Binary file format
The following image represent the base structure of the binary file format.
![ ](/documentation/siglent_sds1000x_bin_file_format.drawio.svg)

### The cleanup process
* Get the highest value from the data and divide it by two to determent the threshold for detecting HIGH and LOW values
* Normalizing data by replacing everything over the threshold as 1 and under as 0
* Remove doubled values

### Decoding
Info: It has to include at least 1 single bit transmission for correct decoding.
* Searching for the quickest change between HIGH and LOW and use it as the value for a single bit (Example: 2.99998mS/bit)
* When detecting more than one bit, it divides the value by the single bit value and rounding it to get the detected amount of bits. (Example: 6.1005mS / 2.99998mS = 2,033514 = 2)
* While decoding the error values are saved to give an indication if the proccess aws successfull. If this error value gets to big the data which you are trying to decode are probable not NZR-Code (Example: 6.1005mS / 2.99998mS = 2,033514 = 0,033514)


### Web fetcher
This is a simple little script which uses selenium to automatically download binary files.
To use this script you need to get the fitting [ChromeDriver](https://chromedriver.chromium.org/downloads)

### Tests
Script for testing purposes. Its functional but nothing more ^^
I normally would would use this while development to monitor if i broke some core functionality.
```test.py```
if you want to test the web fetching you need to edit the following property inside the test.py script:
```webfetchUrl```
Example output:
![ ](/documentation/test_result_example.png)


# ToDo
* Startup option for exporting the cleaned up data
* Startup option for showing diagrams in app
* ~~Add Siglent binary decoder, so you don't need two scripts~~
* ~~Add error rate to console output~~ => added to json output
* Refactor debugging output
* ~~Change format for saving data - json or csv~~ => json
* parallelize decoding of multiple files
* Fixing this mess of a documentation :)


# Digital data decoder for Siglent Oscilloscopes

This is a little script for converting digital data which you captured with you're Siglent oscilloscope (CSV data) into binary format

# How to use
* Get a nice single shot of all the data.
![ ](https://github.com/MerzSebastian/Siglent-csv-basic-decoder/blob/main/documentation/siglent_sds1000x.png)
* Save the shot as a binary on a USB stick and transfer it to your pc or download it directly over the Web Control over your browser (Waveform save)
![ ](https://github.com/MerzSebastian/Siglent-csv-basic-decoder/blob/main/documentation/siglent_sds1000x_save.png)
* Use the bin2csv tool which siglent is providing over the Web Control (Bin_to_CSV_Tool)
![ ](https://github.com/MerzSebastian/Siglent-csv-basic-decoder/blob/main/documentation/bin2csv.png)
* Drag and Drop your file or folder onto the decode.py to start the decoding process
* Alternatively you can use the following command to start the script via the command line
```decode.py <input_file_or_folder> <output_folder>```
![ ](https://github.com/MerzSebastian/Siglent-csv-basic-decoder/blob/main/documentation/output.png)
* The output is also saved in a text document named after the current date and time
![ ](https://github.com/MerzSebastian/Siglent-csv-basic-decoder/blob/main/documentation/output_textfile.png)


# How it Works
In this section we deal with the flow of the main functions of the script
### The cleanup process
* Get the highest value from the data and divide it by two to determent the threshold for detecting HIGH and LOW values
* Normalizing data by replacing everything over the threshold as 1 and under as 0
* Remove doubled values

### Decoding
Info: It has to include at least 1 single bit transmission for correct decoding.
* Searching for the quickest change between HIGH and LOW and use it as the value for a single bit (Example: 2.99998mS/bit)
* When detecting more than one bit, it divides the value by the single bit value and rounding it to get the detected amount of bits. (Example: 6.1005mS / 2.99998mS = 2,033514 = 2)

### Saving
Results are saved to a text file separated by /n

### Info
It's recommended to use the test.py file for development to make sure you don't accidentally break the code and didn't notice

# ToDo
* Startup option for exporting the cleaned up data
* Startup option for showing diagrams in app
* Add Siglent binary decoder, so you don't need two scripts
* Add error rate to console output
* Refactor debugging output
* Change format for saving data - json or csv

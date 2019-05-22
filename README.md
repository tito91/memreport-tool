# memreport-tool
This tool aims to visualize UE4 memreport file content. 

Current status: displaying texture size information in form of nested donut chart.

![alt text](screenshot.png)

### Dependencies

Application was created with Python 3.6.

Required packages:

- `anytree`
- `matplotlib`

### Usage
Call main.py with parameters:
- `-i <input_filename>` - obligatory parameter that provides the program with memreport file

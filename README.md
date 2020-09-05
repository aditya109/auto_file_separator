# Autonomous File Separator
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0b4ada47f0df460b8577dbceb70165e0)](https://www.codacy.com/manual/aditya109/auto_file_separator?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=aditya109/auto_file_separator&amp;utm_campaign=Badge_Grade)

Autonomous File Separator is Python-script which segragates the files under the target directory, classfiying the files based on their extensions.

## Quick Start
### For Windows OS

1.  Clone this repository 
    ```
    git clone https://github.com/aditya109/auto_file_separator
    ```
    
2.  CD into this directory.
    ```
    cd auto_file_separator
    ```
    
3.  Create a virtual environment using `venv` and activate the virtual environment
    ```
    virtualenv venv 
    .\venv\Scripts\activate
    ```

4.  Install the requirements in the created virtual environment `venv`
    ```
    pip install -r requirements.txt
    ```
 
5.  Open the `config.ini` in the `\data`.
    Edit the target field under `locations` section to provide the path of the target directory. 
    ```
    [locations]
    ; target directory location
    target=D:\TEST
    ```
    
6.  Edit the div-directories field under `locations` section to provide the names of      the categorical directories. [OPTIONAL]
    
    ```
    ; name of categorical directories
    div-directories=compressed|documents|video|programs|music
    ```
    
7.  Edit the div-directories field under `output-locations` section to provide the names of the categorical directories.
    If you want to change the location, please go ahead.
    
    **PLEASE DO NOT CHANGE FIELD NAMES, IF YOU DO, DO CHANGE IT ABOVE AS WELL**
    ```
    [output-locations]
    ; locations of div_directories
    compressed=D:\TEST\compressed
    documents=D:\TEST\documents
    video=D:\TEST\video
    programs=D:\TEST\programs
    music=D:\TEST\music
    ``` 

8.  Run the `bin\start.py`
    ```
    python bin\start.py
    ```
 
 Have Fun Hacking !
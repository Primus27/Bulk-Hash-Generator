![](readme_files/banner.png)

# Bulk Hash Generator

## Features
 - Calculate hashes for all files in a given directory
 - Output results to a file (optional)
    - Special formatting is removed
    - Custom filename (optional)

## Requirements and Installation
 - [Python 3.6+](https://www.python.org/)
 - Windows (tested), Mac (untested), Linux (tested)
 - Install all dependencies from the requirements.txt file. `pip3 install -r requirements.txt`

## Arguments
#### Required arguments:
  - `-P PATH` || `--path PATH`
    - Scan path (absolute or relative)
  
  
  - `-A ALGORITHM1...` || `--algorithm ALGORITHM1 ALGORITHM2...`
    - Algorithms to hash with:
      - blake2b
      - sha3_256
      - sha3_384
      - sha1
      - shake_128
      - sha3_224
      - sha512
      - sha3_512
      - md5
      - blake2s
      - shake_256
      - sha384
      - sha256
      - sha224


#### Optional arguments:
  - `-F` || `--fileout`
    - Enable file output
    - Each value (name & hash) is written to a new line
    - It is recommended to output to a txt file
    - Default: Disabled
   
    
  - `-FN FILENAME.txt` || `--filename FILENAME.txt`
    - Custom filename for output
    - It is recommended to output to a txt file
    - Default: hashes-DD.MM.YYYY-HH.MM.SS.txt
  
  
  - `--version`
    - Display program version


## Usage
 - Run 'hash.py' in terminal with arguments (see above)

### Starter command(s)
 - Run with md5 and sha512 hashes
    - `python3 hash.py -P PATH -A md5 sha512`

## Changelog
#### Version 1.0 - Initial release
 - Calculate common hashes of all files in any directory
    - Can be relative path or absolute path
 - Output results to file
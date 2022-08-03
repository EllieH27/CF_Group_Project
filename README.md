# CF_Group_Project
## Project Outline
Provide an interface for downloading csv files containing medical data for the university medical school. These files should be taken from an FTP server and screened for validity (a list of categories can be found below). The files should then be displayed on a user interface with both command line options and a user-friendly front end. 

## Whos doing what:
Ellie H: FTP Server
Harry B1: GUIs
Hannah M and Lucia A: Validation

## Validation Checklist
* Duplicated Batch IDs
* Missing/Misspelt Headers 
* Missing Columns on a row
* Invalid entries
* Empty files
* Incorrectly Formatted File Names
* Malformed Files (format cannot be processed?)

## File Format
Should have headings:
* batch_id
* timestamp
* reading(1-10)
Followed by each "batch" of values. Each batch ID should be unique within the file. Each batch should have 10 readings - floating point numbers between 0-9.9 with 3dp. 

The files should have the following name format:
MED_DATA_YYYYMMDDHHMMSS.csv

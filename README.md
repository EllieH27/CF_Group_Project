# CF_Group_Project
## Project Outline
Provide an interface for 

## Whos doing what:
Ellie H: FTP Server
Harry B1: GUI
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

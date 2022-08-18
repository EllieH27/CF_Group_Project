"""Module containing validation checks

Functions: filename_check, parse_csv_data, check_empty_files, check_batch_ids, check_missing_entries, check_time_entry, check_headers,
check_invalid_entries, total_valid
"""

import csv
import re
import logging

def filename_check(csv_filename: str) -> bool:
    """
    Takes in csv file name and returns validity (in form MED_DATA_YYYYMMDDHHMMSS.csv)

    Keyword arguments:
    csv_filename (file.csv) : Title of csv file containing data

    Returns:
    valid (boolean) : Whether name valid or not
    """

    valid = True

    x = re.search("^(MED_DATA_)\d{14}(.csv)$", csv_filename)
    if x is None:
        valid = False
        logging.warning(f'Invalid filename [{csv_filename}] should be in format MED_DATA_YYYYMMDDHHMMSS.csv')

    return valid


def parse_csv_data(csv_filename: str) -> list:
    """
    Returns a 2d array of strings of the csv file data

    Keyword arguments:
    csv_filename (file.csv) : Title of csv file containing data

    Returns:
    rows (list) : 2d array of rows and entires in csv file
    """

    with open(csv_filename,'r', encoding="utf-8") as file:
        csvreader = csv.reader(file)

        rows = []
        for row in csvreader:
            rows.append(row)

    logging.info('csv file read successfully')

    return rows


def check_empty_files(csv_content: str) -> bool:
    """
    Takes in csv file name and returns whether file is empty

    Keyword arguments:
    csv_filename (file.csv) : Title of csv file containing data

    Returns:
    valid (boolean) : Returns true if valid (non-empty) and false if empty
    """


    if csv_content == []:
        valid = False
        logging.warning(f'File is empty')
    else:
        valid = True

    return valid


def check_batch_ids(csv_content: str) -> bool:
    """
    Takes in csv file name and returns whether batch IDs are vaild

    Keyword arguments:
    csv_filename (file.csv) : Title of csv file containing data

    Returns:
    valid (boolean) : Checks for duplicated batch IDs and returns False is dupliacted found
    """

    valid = True
    collected_ids = []
    num_rows = len(csv_content)

    for i in range(1,num_rows):
        b_id = csv_content[i][0]
        if b_id in collected_ids:
            valid = False
            logging.warning(f'Batch ID [{b_id}] is invalid/repeated')
            break
        else:
            collected_ids.append(b_id)

    return valid


def check_missing_entries(csv_content: str) -> bool:
    """
    Takes in csv file name and checks for 12 columns and for 11 rows (including header row)

    Keyword arguments:
    csv_filename (file.csv) : Title of csv file containing data

    Returns:
    valid (boolean) : Checks rows and columns and returns False if invalid
    """

    valid = True
    num_rows = len(csv_content)

    if num_rows != 11:
        valid = False
        logging.warning(f'Number of rows [{num_rows}] is invalid (expected 11 including header)')

    for row in csv_content:
        num_columns = len(row)
        if num_columns != 12:
            valid = False
            logging.warning(f'Number of columns [{num_columns}] is invalid (expected 12)')

    return valid


def check_time_entry(csv_content: str) -> bool:
    """
    Takes in csv file name and checks the timestamp value is in form HH:MM:SS

    Keyword arguments:
    csv_filename (file.csv) : Title of csv file containing data

    Returns:
    valid (boolean) : Checks timestamp format and return True if valid
    """

    valid = True

    for i in range(1,len(csv_content)):
        row_time = csv_content[i][1]
        x = re.search("^\d\d:\d\d:\d\d$", row_time)

        if x is None:
            valid = False
            logging.warning(f'Timestamp {x} invalid. Expected format HH:MM:SS')

    return valid


def check_headers(csv_content: str) -> bool:
    """
    Takes in csv file name and returns whether headers are correct
    Expected: batch_id, timestamp, reading1, reading2, reading3, reading4, reading5, reading6, reading7, reading8, reading9, reading10

    Keyword arguments:
    csv_filename (file.csv) : Title of csv file containing data

    Returns:
    valid (boolean) : Checks for header names and returns False if not expected input
    """

    valid = True
    good_headers = ['batch_id', 'timestamp', 'reading1', 'reading2', 'reading3', 'reading4', 'reading5', 'reading6', 'reading7', 'reading8', 'reading9', 'reading10']
    try:
        header_list = csv_content[0]
    except:
        # empty file shouldn't be processed
        valid = False
        header_list = []

    incorrect_headers = ""

    # check right length
    if len(header_list) != 12:
        valid = False
        logging.warning('Header is missing. Expected 12 headers')

    # check each name
    if valid:
        for i in range(12):
            if good_headers[i] != header_list[i]:
                valid = False
                incorrect_headers += header_list[i] + " ,"

    # for logging purposes
    if incorrect_headers != "":
        logging.warning(f'{incorrect_headers} is incorrect')

    return valid


def check_invalid_entries(csv_content: str) -> bool:
    """
    Takes in csv file name and returns whether entries are valid
    All 10 readings should be represented as floating point numbers formatted up to three decimal places
    with no value exceeding 9.9


    Keyword arguments:
    csv_filename (file.csv) : Title of csv file containing data

    Returns:
    valid (boolean) : Checks for entries and returns False if invalid data
    """

    valid = True

    # Doesn't process first row
    for i in range(1,len(csv_content)):
        row = csv_content[i]
        for j in range(2,12):
            # gets each number (stored as string)
            str_entry = row[j]

            #checks number to 3dp
            x = re.search("^\d\.\d{3}$", str_entry)
            if x is None:
                logging.warning(f'{str_entry} invalid. Expected value to 3dp (Regex failed)')
                valid = False
                break

            try:
                # checks for float and number
                val = float(str_entry)
                if val > 9.9:
                    valid = False
                    logging.warning(f'{str_entry} invalid. Value must not exceed 9.9')
            except:
                # raises value error as not float
                logging.warning(f'{str_entry} invalid. Value is not a float')
                valid = False

    return valid


# ====== Final validation ======

def total_valid(csv_filename: str) -> bool:
    """
    Takes in csv file name and returns all checks for whether file is valid

    Keyword arguments:
    csv_filename (file.csv) : Title of csv file containing data

    Returns:
    valid (boolean) : Checks csv_file and returns if a valid file
    """

    valid = True
    valid_filename = filename_check(csv_filename)

    if valid_filename:
        csv_data = parse_csv_data(csv_filename)
        non_empty = check_empty_files(csv_data)

        if non_empty:

            valid_batch_ids = check_batch_ids(csv_data)
            missing_entry = check_missing_entries(csv_data)
            time_entry = check_time_entry(csv_data)
            good_headers = check_headers(csv_data)
            valid_entires = check_invalid_entries(csv_data)

            valid_list = [valid_batch_ids,missing_entry,time_entry,good_headers,valid_entires]

            if False in valid_list:
                valid = False
                logging.warning(f'Invalid file [{csv_filename}] so discarded')

        else:
            logging.warning(f'Invalid file [{csv_filename}] so discarded')
            valid = False

    else:
        logging.warning(f'Invalid file [{csv_filename}] so discarded')
        valid = False

    return valid


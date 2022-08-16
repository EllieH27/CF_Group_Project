import logging
from csv_checker import *

# sets up logging in file csv.log
logging.basicConfig(filename='csv.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# provides ways to access the Operating System and allows us to read the environment variables
import os

from datetime import datetime
from src.extract import extract_data
from src.clean_data import clean_data
from src.segment_data import segment_customers

# import the load_dotenv from the python-dotenv module
from dotenv import load_dotenv
load_dotenv() # take environment variables from .env only for local testing

# import environment variables from .env file
dbname = os.getenv("dbname")
host = os.getenv("host")
port = os.getenv("port")
user = os.getenv("user")
password = os.getenv("password")

# this creates a variable that tracks the time we executed the script
start_time = datetime.now()

# make a connection to redshift and extract online transactions cleaned data
print("\nExtracting data in sql...")
online_trans = extract_data(dbname, host, port, user, password)
print('\nExtraction in sql completed')
print("-" * 80)

# clean data
print("\nCleaning data...")
online_trans = clean_data(online_trans)
print('\nCleaning data completed')
print("-" * 80)

# segment customers
print("\nSegmenting customers...")
rfm = segment_customers(online_trans)
print("\nCustomer segmentation completed")
print("-" * 80)

# this creates a variable that calculates how long it takes to run the script
execution_time = datetime.now() - start_time
print(f"\nTotal execution time (hh:mm:ss.ms) {execution_time}")
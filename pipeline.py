#Import packages
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait

from datetime import datetime
import pandas as pd
import numpy as np
import random
import time
import os
import re
from tqdm import tqdm 

import mysql.connector
import spacy
from spacy.matcher import Matcher
from pipelines import scraper, clean_data, matcher, load

# Set the output directory
current_directory = os.getcwd()

# Set current date
now = datetime.now()
start_date = now.strftime('%Y-%m-%d')

output_directory = f"{current_directory}/data/jobstreet-{start_date}.csv"

# Read environment variables
host = os.environ.get("RDS_HOST")
user = os.environ.get("RDS_USERNAME")
password = os.environ.get("RDS_PASS")

nlp = spacy.load("en_core_web_sm")

jobs_data = scraper.scrape_jobstreet("Data Engineer", "National Capital Region")
scraper.data_to_s3(output_directory)
clean_job_data = clean_data.clean_data(jobs_data)
clean_job_data_with_tech = matcher.matcher(clean_job_data)

conn, mycursor = load.set_mysql_connection(host, user, password, 'jobstreet_db')
load.insert_into_database(clean_job_data_with_tech, 'jobstreet', mycursor, conn)
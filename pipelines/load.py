from datetime import datetime
import pandas as pd
import numpy as np
import random
import time
import os
import re
from tqdm import tqdm 

import mysql.connector

def set_mysql_connection(host, user, password, database):
    conn = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = database
    )
    
    mycursor = conn.cursor()
    
    return conn, mycursor

def insert_into_database(data, table, mycursor, conn):
    for i, row in tqdm(data.iterrows()):
        try:
            query = f"""
              INSERT INTO {table} (job_id, job_title, location, company, salary, job_url, qualification,
                                   year_of_experience, job_type, company_size, tech_language, tech_database,
                                   tech_cloud, tech_web_framework, tech_libraries, tech_developer, tech_data_viz,
                                   tech_version_control)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
              """
            info = (row['job_id'], row['title'], row['location'], row['company'], row['salary'], row['job_url'],
                   row['Qualification'], row['Years of Experience'], row['Job Type'], row['Company Size'],
                   row['languages'], row['databases'], row['cloud_platforms'], row['web_frameworks'], row['libraries'],
                   row['developers'], row['data_visualization'], row['version_controls'])
            mycursor.execute(query, info)
            conn.commit()
        except:
            pass
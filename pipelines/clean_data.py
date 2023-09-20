import pandas as pd
import numpy as np
import random
import time
import os
import re
from tqdm import tqdm 
from datetime import datetime


def clean_salary(salary):
    matches = re.findall(r"\d{1,3},\d{1,3}", str(salary))
    return int(matches[0].replace(",", "")) if matches else None

def clean_title(title):
    title = re.sub(r"""(urgent)|(hiring)|(night)|(shift)|(mid)|(morning)|(graveyard)|(gy)|(dayshift)|(set)|(asap)|(set up)|(day)|(temporary)|(work)|(from)|(home)|(wfh)|(temp)|(office)|(onsite)|(hybrid)|([-*!\[\]|:;])""", "", title, flags=re.IGNORECASE)
    
    matches = re.split(r'\s[,*/\[\]\(\)|]|(\s{2,})', str(title))
    matches = [x for x in matches if x is not None]                                      #Removing None type
    #matches = [text for text in matches if all(word.isalpha() for word in text.split())] #Removing Spaces
    matches = [text for text in matches if text.strip()]                                 
    return matches[0].strip() if matches else None

def clean_year_of_experience(experience):
    if isinstance(experience, str):
        matches = re.findall(r"\d{1,2}", experience)
        return matches[0] if matches else None
    else:
        return None  # or any other value you prefer for non-string cases

def clean_num_of_employees(employees):
    if isinstance(employees, str):
        text = re.sub("(\sEmployees)|(\semployees)|(\sEmployee)|(\semployee)", "", employees)
        return text
    else:
        return None
    
def clean_qualification(df):
    df['Qualification'] = df['Qualification'].replace({'Not Specified': None})
    return df

def clean_data(df):
    df = [["job_id", "title", "location", "company",
            "salary", "summary", "job_url", "Qualification",
            "Years of Experience", "Job Type", "Company Size"]]
    #df['title'] = df['title'].map(clean_title)
    df['salary'] = df['salary'].map(clean_salary)
    df['Years of Experience'] = df['Years of Experience'].map(clean_year_of_experience)
    df['Company Size'] = df['Company Size'].map(clean_num_of_employees)
    df = clean_qualification(df)
    return df

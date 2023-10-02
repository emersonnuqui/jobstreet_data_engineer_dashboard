from datetime import datetime
import pandas as pd
import numpy as np
import random
import time
import os
import re
from tqdm import tqdm 
import boto3
from io import StringIO


def connect_to_s3(aws_key_id, secret_key):
    # Set up S3 access
    s3 = boto3.client('s3',                                # AWS Service Name
					region_name = 'ap-southeast-2',           # Region; geo-region where our resources are located.
                    aws_access_key_id = aws_key_id,         # Key
                    aws_secret_access_key = secret_key)  # Secret Key
    return s3


def export_main_data(main_data, new_data, s3, bucket_name):
    response = s3.get_object(Bucket=bucket_name, Key=main_data)
    csv_data = response['Body'].read().decode('utf-8')

    # Load the CSV data into a Pandas DataFrame
    df = pd.read_csv(StringIO(csv_data))
    
    updated_data = pd.merge([df, new_data], ignore_index=True)
    updated_data = updated_data.drop_duplicates(subset='id')
    

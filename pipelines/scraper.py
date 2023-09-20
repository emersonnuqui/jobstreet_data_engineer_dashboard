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
import time
import re
from datetime import datetime
import pandas as pd
import os
import boto3

# Set the output directory
current_directory = os.getcwd()

def scrape_jobstreet(position, location):
    now = datetime.now()

    start_date = now.strftime('%Y-%m-%d')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
    except:
        driver = webdriver.Chrome(executable_path = f"{current_directory}/chromedriver.exe")
    driver.set_page_load_timeout(20)
    driver.maximize_window()

    url = r'https://www.jobstreet.com.ph/'
    
    driver.set_page_load_timeout(10)
    driver.get(url)
    driver.implicitly_wait(8)
    time.sleep(10)

    job_search = driver.find_element(By.ID, 'searchKeywordsField')
    job_search.clear()
    job_search.send_keys(position)

    #This will automatically put the location
    location_field = driver.find_element(By.ID, 'locationAutoSuggest')
    location_field.clear()
    location_field.send_keys(location)

    #Job posts will appear
    find = driver.find_element(By.XPATH, "//button[@type='submit']")
    find.click()
    
    jobs_list = []
    while True:
        articles = driver.find_elements(By.XPATH, "//div[@class='z1s6m00 _1hbhsw67i _1hbhsw66e _1hbhsw69q _1hbhsw68m _1hbhsw6n _1hbhsw65a _1hbhsw6ga _1hbhsw6fy']")

        time.sleep(2)
        to_frame = []
        items = 0

        for article in articles:

            time.sleep(2)

            driver.execute_script('arguments[0].click();', article)
            items += 1
            summary = driver.find_element(By.XPATH, "//div[@data-automation='jobDescription']").text.strip()
            title = driver.find_elements(By.XPATH, "//div[@class='z1s6m00 _1hbhsw6r pmwfa50 pmwfa57']//span[@class='z1s6m00 _1hbhsw64y y44q7i0 y44q7i3 y44q7i21 _1d0g9qk4 y44q7ia']")
            info = driver.find_elements(By.XPATH, "//div[@class='z1s6m00 _1hbhsw6r pmwfa50 pmwfa57']//span[@class='z1s6m00 _1hbhsw64y y44q7i0 y44q7i1 y44q7i21 _1d0g9qk4 y44q7ia']")

            other_info = {}
            for i in range(len(title)):
                title_ = title[i].text
                info_ = info[i].text
                other_info.update({title_: info_})

            loc_salary_field = driver.find_elements(By.XPATH, '//div[@class="z1s6m00 _1hbhsw66i"]')
            title_company_field = driver.find_elements(By.XPATH, '//div[@class="z1s6m00 _1hbhsw66u"]')

            location = loc_salary_field[0].text.strip()
            title = title_company_field[0].text.strip()
            company = title_company_field[1].text.strip()
            try:
                test_salary = loc_salary_field[1].text.strip()
                if re.search('php', test_salary.lower()):
                    salary = test_salary
                else:
                    salary = None
            except:
                salary = None


            # try to get url,
            job_url = driver.find_element(By.XPATH, "//span[@class='z1s6m00 _1hbhsw64y y44q7i0 y44q7i1 y44q7i21 _1d0g9qk4 y44q7ia']/a[@target='_blank']").get_attribute('href')
            #print(job_url)

            job_info = {
                'job_id': re.findall(r"\d{6,8}", job_url)[0],
                'location': location,
                'title': title,
                'company': company,
                'salary': salary,
                'summary': summary,
                'job_url': job_url,
                'date_posted': start_date}

            job_info.update(other_info)
            to_frame.append(job_info)

        framed_df = pd.DataFrame(to_frame)
        jobs_list.append(framed_df)
        
        start_url = driver.current_url
        
        #Clicks the next page 
        next_page = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH,
                "//span[normalize-space()='Next']"
                )))
        
        driver.execute_script("arguments[0].click();", next_page)
        next_url = driver.current_url
        
        time.sleep(5)
        #Scraper stops if it reaches the last page
        if start_url == next_url:
            print(f"Scraper stopped moving, scaping ended.")
            break
    jobs_data = pd.concat(jobs_list, ignore_index=True)
    jobs_data.to_csv(f"{current_directory}/data/jobstreet-{start_date}.csv", index=False)
    return jobs_data

def data_to_s3(data_directory):
    now = datetime.now()
    start_date = now.strftime('%Y-%m-%d')

    #data.to_csv('jobstreet-{start_date}.csv', index=False)

    # Set up S3 access
    s3 = boto3.client('s3',                                # AWS Service Name
					region_name = 'ap-southeast-2',           # Region; geo-region where our resources are located.
                    aws_access_key_id = os.environ.get("AWS_KEY_ID"),         # Key
                    aws_secret_access_key = os.environ.get("AWS_SECRET_ID"))  # Secret Key
    

    # Upload File
    s3.upload_file(Filename=data_directory, Bucket='jobstreet-de', Key=f'jobstreet-{start_date}.csv')
    print("Done Uploading")

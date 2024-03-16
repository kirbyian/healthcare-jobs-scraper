#!/usr/bin/env python3
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import hospital_parser_util
from selenium.webdriver.chrome.service import Service


def parse_job_page(writer, driver,url):

     job_text=driver.find_element(By.ID,"ctl00_masterPageBodyContentPlaceholder_jobTitleGroup").text

     department,is_matched,amended_job_title=hospital_parser_util.job_title_in_search_list(job_text)
     contact=''
     hospital=''
     deadline=''
     hospital=''
     formatted_deadline=''

     if is_matched:
                    try:
                     location=driver.find_element(By.XPATH,
                    "//div[@id='ctl00_masterPageBodyContentPlaceholder_jobLocationFieldRow']/div/p").text
                    except Exception as e:
                        print("Unable to find element", e)
                    try:
                     duration=driver.find_element(By.XPATH,
                     "//div[@id='ctl00_masterPageBodyContentPlaceholder_jobTypeFieldRow']/div/p").text
                    except Exception as e:
                        print("Unable to find element", e)
                    try:
                      # Find the div element
                        #div_element = driver.find_element(By.XPATH, "//div[@id='ctl00_masterPageBodyContentPlaceholder_jobDetailsGroup']")

                        # Find the first br element within the div
                        text = driver.find_element(By.XPATH,"//div[@id='ctl00_masterPageBodyContentPlaceholder_jobDetailsGroup']")

                        # Get text after the first br element
                        first_hospital_text= driver.find_element(By.XPATH,"//span[contains(text(), 'Hospital')]").text
                        # Define the regex pattern to match hospital names
                        pattern = r'\b([A-Z][a-zA-Z\s]+ Hospital)(?:,\s?[A-Z][a-zA-Z\s]+)?\b'

                        # Find all matches
                        hospitals = re.findall(pattern, first_hospital_text)

                        hospital = ', '.join(hospitals)
                    except Exception as e:
                        print("Unable to find element", e)
                    try:
                     contact= driver.find_element(By.XPATH,"//span[contains(text(), 'Informal enquiries ')]").text
                    except Exception as e:
                        print("Unable to find element", e)
                    try:
                        deadline = driver.find_element(By.XPATH,"//span[contains(text(), 'Closing Date ')]").text
                    except Exception as e:
                        print("Unable to find element", e)
                    if deadline!='':
                        formatted_deadline=hospital_parser_util.formatDate(deadline)
                    writer.writerow({'Position': amended_job_title, 'Hospital': hospital, 'Location': location, 'Link for Post': url,
                'Deadline': formatted_deadline, 'Contact': contact, 'Duration': duration, 'Department': department})
            

def scrape_job_data(writer):
    
        url = "https://www.candidatemanager.net/cm/p/pJobs.aspx?mid=*syu~op%7dfli&sid=*qmkqmk&Site=NCHD"

        browser_driver = Service('/usr/lib/chromium-browser/chromedriver')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = '/usr/bin/chromium-browser'
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--remote-debugging-pipe')
        driver = webdriver.Chrome(service=browser_driver,chrome_options=chrome_options)

        # Step 2: Perform the search
        driver.get(url)
        link_elements=[]   
        
        try:
            # Find the "Accept all" button by ID
            anchors = driver.find_elements(By.XPATH, '//table[@class="table table-striped table-hover table-sm"]//tbody//tr//a')

            links = [element.get_attribute("href") for element in anchors]

            #Process other 
            for url in links:
                # Visit each page
                driver.get(url)
                parse_job_page(writer, driver,url)

        except Exception as e:
                print(e)

        driver.quit()
    
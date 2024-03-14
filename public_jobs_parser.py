#!/usr/bin/env python3
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import hospital_parser_util
from selenium.webdriver.chrome.service import Service


def parse_job_page(url,writer, driver):
     driver.get(url)

     job_title = driver.find_element(By.XPATH,"//h1[@class='col-sm-6 mainTitle']").text

     hospital=driver.find_element(By.ID,"county_inner").text

     location=driver.find_element(By.ID,"empDepartment_inner").text
     
     #Deadline
     deadline=driver.find_element(By.ID,"closDateApplication_inner").text
     #Contact
     contact = driver.find_element(By.ID,"addInfo_inner").text.replace('\n', '')
     #Duration
     duration = "Temp" if "temp" in job_title else "Perm"

     department,match_found,job_title_amended= hospital_parser_util.job_title_in_search_list(job_title)
     #Department
     if match_found:
            if deadline!='':
                formatted_deadline=hospital_parser_util.formatDate(deadline)
            writer.writerow({'Position': job_title_amended, 'Hospital': hospital, 'Location': location, 'Link for Post': url,
            'Deadline': deadline, 'Contact': contact, 'Duration': duration, 'Department': department})


def scrape_job_data(writer):
    
        url = "https://www.publicjobs.ie/en/job-search?category=3&county=&searchphrase="

        browser_driver = Service('/usr/lib/chromium-browser/chromedriver')
        driver = webdriver.Chrome(service=browser_driver)

        # Step 2: Perform the search
        driver.get(url)
        link_elements=[]   
        
        try:
            # Find the "Accept all" button by ID
            accept_button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'cookiescript_accept')))

            # Click the "Accept all" button
            accept_button.click()
            dropdown =WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.NAME, 'jobsList_length')))

            dropdown_select = Select(dropdown)

            # Select     an option by its value (e.g., "20")
            dropdown_select.select_by_value("100")

            # Find all elements containing the links using an appropriate locator strategy
            link_elements = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.XPATH,"//button[@class='btn btn-primary jobDetailsListBtn']")))
            job_title_elements = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.XPATH, "//h2[@id='jobName']")))

            # Extract text values from job title elements
            job_titles = [title.text for title in job_title_elements]
        except Exception as e:
                print("Unable to find links", e)

#        Extract the URLs from the elements
        if link_elements and job_titles:
            # Extract the href attribute from each link element
            links = [link.get_attribute("onclick").split("jobdetails")[1] for link in link_elements]
            
            pattern = r"&Itemid=\d+&cid=\d+&campaignId=\d+"
            # Print the extracted links
            for job_title,link in zip(job_titles, links):
               # Extract the substring using regex
                department,is_valid_speciality,amended_job_title=hospital_parser_util.job_title_in_search_list(job_title)
                if is_valid_speciality:
                    match = re.search(pattern, link)
                    if match:
                        extracted_substring = match.group()
                        new_url="https://www.publicjobs.ie/en/?option=com_jobsearch&view=jobdetails"+extracted_substring
                        driver.get(new_url)
                        parse_job_page(new_url,writer,driver)
        else:
            print("No links found")

        driver.quit()
    
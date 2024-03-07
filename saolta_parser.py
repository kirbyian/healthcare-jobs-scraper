#!/usr/bin/env python3
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import hospital_parser_util


def parse_job_page(writer, driver):

     links = driver.find_elements(By.XPATH,"//td[@class='views-field views-field-title']/a")
     categories=driver.find_elements(By.XPATH,"//td[@class='views-field views-field-field-jobs-category']")
     job_links = {}

     for link in links:
        job_text = link.text
        job_href = link.get_attribute('href')
        job_links[job_text] = job_href

     category_texts = [category.text for category in categories]
     for job_text, job_href in job_links.items():

         department,is_matched,amended_job_title=hospital_parser_util.job_title_in_search_list(job_text)
         contact=''
         hospital=''
         deadline=''
         hospital=''
         category_index = list(job_links.keys()).index(job_text)
         category = category_texts[category_index]

         if(category=='Medical/Dental') and is_matched:
                    driver.get(job_href)
                    try:
                     hospital=driver.find_element(By.XPATH,
                    "//div[@class='field field-name-field-jobs-hospital field-type-list-text field-label-above']"+
                    "/div[@class='field-items']/div[@class='field-item even']").text
                    except Exception as e:
                        print("Unable to find element", e)
                    try:
                        deadline= driver.find_element(By.XPATH, "//div[@class='field field-name-field-jobs-closing-date field-type-date field-label-above']"
                    +"/div[@class='field-items']/div[@class='field-item even']").text
                    except Exception as e:
                        print("Unable to find element", e)
                    try:
                        contact = driver.find_element(By.XPATH,"//p[contains(text(), 'Informal enquiries to')]").text
                    except Exception as e:
                        print("Unable to find element", e)
                    if deadline!='':
                        formatted_deadline=hospital_parser_util.formatDate(deadline)
                    writer.writerow({'Position': amended_job_title, 'Hospital': hospital, 'Location': '', 'Link for Post': job_href,
                'Deadline': formatted_deadline, 'Contact': contact, 'Duration': '', 'Department': department})
            

def scrape_job_data(writer):
    
        url = "https://www.saolta.ie/jobs"

       # browser_driver = Service('/usr/lib/chromium-browser/chromedriver')
        driver = webdriver.Chrome()

        # Step 2: Perform the search
        driver.get(url)
        link_elements=[]   
        
        try:
            # Find the "Accept all" button by ID
            accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="popup-buttons"]/button[@class="agree-button eu-cookie-compliance-secondary-button"]')))
            # Click the "Accept all" button
            driver.execute_script("arguments[0].scrollIntoView();", accept_button)
            time.sleep(2)  # Add a short delay before interacting with the element
            accept_button.click()

  
            # Locate the pagination element
            pagination_elements = driver.find_elements(By.CSS_SELECTOR, "li.pager-item a")

            # Extract the href attribute values from the pagination elements
            pagination_urls = [element.get_attribute("href") for element in pagination_elements]

            #Process current page 
            parse_job_page(writer, driver)
            #Process other 
            for url in pagination_urls:
                # Visit each page
                driver.get(url)
                parse_job_page(writer, driver)

        except Exception as e:
                print(e)

        driver.quit()
    
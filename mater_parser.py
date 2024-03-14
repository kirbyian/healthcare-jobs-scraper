#!/usr/bin/env python3
import requests
import json
import re
from bs4 import BeautifulSoup
import hospital_parser_util


def parse_job_page(job_id):

    url = "https://www.rezoomo.com/index.cfm"

    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }

    form_data = {
    'jobId': job_id,
    'action': 'api.front.job.onMount',
    'preview': 'false',
    'companySubdomain':''
    }

    # Send a POST request with form data
    response = requests.post(url, data=form_data)
    data_dict = json.loads(response.text)
   
    description = data_dict['data']['job']['description']

    emails=extract_emails(description)
    dates=extract_closing_date(description)
    return emails,dates


def extract_emails(text):
    # Define a regular expression pattern to match mailto: links
    mailto_pattern = re.compile(r'mailto:([^\s<>"]+)')
    
    # Find all matches of mailto: links in the text
    matches = mailto_pattern.findall(text)

    # Extract email addresses from matches
    emails = [match.strip() for match in matches]

    return '; '.join(emails)

def extract_closing_date(text):
    # Define a regular expression pattern to match mailto: links
    pattern = re.compile(r'>Closing date:.*?(?=>)', re.DOTALL)
    # Find all matches of mailto: links in the text
    matches = pattern.findall(text)

    # Extract email addresses from matches
    dates = [match.strip() for match in matches]

    return '; '.join(dates)

def parse_mater_details(job,writer):
        dept,is_match,amended_job_title=hospital_parser_util.job_title_in_search_list(job['JOBNAME'])
        if is_match:
            contact,deadline=parse_job_page(job['JOBID'])
            writer.writerow({
                    'Position': amended_job_title,
                    'Hospital': job['COMPANYNAME'],
                    'Location': job['LOC'],
                    'Link for Post':job['URLJOB'],
                    'Deadline': deadline,
                    'Contact': contact, 
                    'Duration': job['JOBTYPE'],
                    'Department': dept
                })

def scrape_job_data_mater(writer):
    
        url = "https://www.rezoomo.com/index.cfm?action=find.job"

        headers = {"Content-Type": "application/json"}

    # Your JSON object
        data = {
            "locationQuery": "/jobs-with-medical/",
            "options": {"refreshSkills": True, "getDebug": False, "initial": True},
            "searchFields": {
                "query": "",
                "location": "",
                "jobFunction": "medical",
                "jobTypes": ["any"],
                "jobSkills": ["any"],
            },
            "pagination": {"offset": 0, "limit": 100},
        }

        # Sending a POST request with JSON data
        response = requests.post(url, json=data, headers=headers)
    
        data_dict = json.loads(response.text)

    
    
            # Extract job entries with specific names
        target_names = ["registrar", "consultant"]
        matching_jobs = []
    
        for job in data_dict["items"]:
                for substring in target_names:
                    if substring.lower() in job["JOBNAME"].lower():
                        matching_jobs.append(job)
                        break
    
        # Print the matching job entries
        for job in matching_jobs:
             parse_mater_details(job,writer)
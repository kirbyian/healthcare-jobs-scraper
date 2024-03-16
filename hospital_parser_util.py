from datetime import datetime


medical_search_list=['cardiol','genetics','pharma','internal','derma','gastro',
                        'endocrinol','diabet','general internal'
                        'genitourinary','geriatric','infectious disease','oncolog',
                        'nephrologo','neurol','pallative','rehab',
                         'resp','rheumatolog','gynaec','gynaco','haem']

medical_substrings_to_depts={
    'cardiol':'Cardiology',
    'genetics':'Clinical Genetics',
    'derma':'Dermatology',
    'endocrinol':'Endocrinology & Diabetes Mellitus',
    'diabet':'Endocrinology & Diabetes Mellitus',
    'gynaco':'Obs & Gyna',
    'gynaec':'Obs & Gyna',
    'gastro':'Gastro & General Physician',
    'geriatric':'Geriatrics',
    'infectious disease':'Infectious Diseases',
    'oncolog':'Oncology',
    'resp':'Resp & GIM',
    'neurol':'Neurology',
    'rheumatolog':'Rheumatology & General Physician',
    'haem':'Haematology',
    'rehab':'Rehabilitation Medicine'
}

def job_title_in_search_list(job_title):
        for substring in medical_search_list:
            amended_job_title=''
            department=''
            if 'consultant' in job_title.lower():
                amended_job_title='Consultant'
            else:
                amended_job_title='Registrar'
            if substring.lower() in job_title.lower():
                department = medical_substrings_to_depts.get(substring.lower(), "unknown")
                return department,True,amended_job_title
        return job_title,False,job_title

def isConsultantOrReg(job_title):
        for substring in medical_search_list:
            amended_job_title=''
            if 'consultant' in job_title.lower():
                amended_job_title='Consultant'
            else:
                amended_job_title='Registrar'
            if substring.lower() in job_title.lower():
                mapped_value = medical_substrings_to_depts.get(substring.lower(), "unknown")
                return mapped_value,True,amended_job_title
        return amended_job_title;

def is_date_in_format(date_str, date_format):
            try:
                datetime.strptime(date_str, date_format)
                return True
            except ValueError:
                return False
            
def formatDate(deadline):
        if is_date_in_format(deadline, "%A, %B %d, %Y"):
            date_obj = datetime.strptime(deadline, "%A, %B %d, %Y")
            return date_obj.strftime("%-d/%-m/%Y")
        elif is_date_in_format(deadline, "%d/%m/%Y %H:%M"):
            date_obj = datetime.strptime(deadline, "%d/%m/%Y %H:%M")
            return date_obj.strftime("%-d/%-m/%Y")
        else:
            return ''
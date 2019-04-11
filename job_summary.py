import urllib.request
from bs4 import BeautifulSoup

#the function takes as input a job url, returns a dictionary with various properties
#   like job title and company name, salary, educational and experience requirements

def get_job_details(url):
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")
    
    requirements_info = soup.find_all("div", class_="edu_req")
    salary_info = soup.find_all("div", class_="salary_range")
    title = soup.find_all("title")
    
    # there are two types of lines generally in requirements info
    #    educational requirements, and experience requirements
    
    # info will be the final return value
    info = {}
    # gets the page title, has info about job title and company
    # it also has the terms Bdjobs.com in it after a ||, which we discard
    job_summary = title[0].text
    job_summary = job_summary.split('||')[0]
    info['job summary'] = job_summary
    
    #Get requirements info
    for req in requirements_info:
        # get the text equivalent and break them into lines
        lines = req.text.split('\n')
        # first non-empty text line in each tag defines the type of requirement
        flag = False
        lst_req = []
        for line in lines:
            #find first non-empty line, hence the type
            if(not(flag)):
                if(len(line) > 0):
                    flag = True
                    req_type = line
                continue
            #gather all info of this type into one array line
            else:
                if(len(line) > 0):
                    lst_req.append(line)
        #combine them together in one line
        lst_req = ';'.join(lst_req)
        
        info[req_type] = lst_req
    
    #Get salary info
    txt = salary_info[0].text
    txt = txt.replace('\r','\n')
    #We do the same type of work as done before for requirements
    flag = False
    lst_salary_info = []
    lines = txt.split('\n')
    for line in lines:
        #find first non-empty line, hence the type
        if(not(flag)):
            if(len(line) > 0):
                flag = True
                salary_header = line
            continue
        #gather all info of this type into one array line
        else:
            if(len(line) > 0):
                lst_salary_info.append(line.strip(' '))
    lst_salary_info = ';'.join(lst_salary_info)
    info[salary_header] = lst_salary_info
    
    return info

url = 'http://jobs.bdjobs.com/jobdetails.asp?id=834914'
info = get_job_details(url)
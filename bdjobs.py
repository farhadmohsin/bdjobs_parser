import urllib.request
from bs4 import BeautifulSoup
import re
import csv
from datetime import date,timedelta

# We parse the data from the bdjobs.com home page
dt= date.today()
r = urllib.request.urlopen('http://bdjobs.com/').read()
soup = BeautifulSoup(r, "lxml")

#%%
#ind_jobs finds the tags for industrial categories
#fun_jobs finds the tags for the functional categories
ind_jobs = soup.find_all("div", class_="category-list padding-mobile industrial")
fun_jobs = soup.find_all("div", class_="category-list padding-mobile functional active")

#Break the text for both job categories into lines
jobs_f = fun_jobs[0].text.split('\n')
jobs_i = ind_jobs[0].text.split('\n')
#%%

job_class = []
'''For each line in functional job list, if line is not empty
    add new job to job list'''

for row in jobs_f:
    if(len(row)>0 and not('More' in row or 'Less' in row)):
        n = re.findall('\d+', row )
        job_class.append(['Functional',row.split('(')[0],int(n[0])])

'''For each line in industrial job list, if line is not empty
    add new job to job list'''        
for row in jobs_i:
    if(len(row)>0 and not('More' in row or 'Less' in row)):
        n = re.findall('\d+', row )
        job_class.append(['Industrial',row.split('(')[0],int(n[0])])

#write file with relevant info about categorical jobs
with open(dt.strftime('BdJobs %Y%m%d.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(job_class)
    
#%%

#Get all the hot jobs in the bdjobs homepage
hot = soup.find_all("div", class_="hotJobsCompany")
HotJobs = []
for tag in hot:
    #find job title for the hot job
    titles = [m.start() for m in re.finditer('title', str(tag))]
    ll = len(str(tag))
    names = []
    for st in titles:
        cnt = 0
        #the following part gets the job name from the title tag
        for j in range(st,ll):
            if(str(tag)[j] == '"'):
                cnt += 1
                if(cnt==1):
                    tt1 = j
                elif(cnt==2):
                    tt2 = j
                    break
        names.append(str(tag)[tt1+1:tt2])
    HotJobs.append(names)
    
#write hot jobs to file
with open(dt.strftime('HotJobs %Y%m%d.csv'), 'w', newline='',encoding="utf-16") as f:
    writer = csv.writer(f)
    writer.writerows(HotJobs)
    
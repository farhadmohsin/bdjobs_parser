import urllib.request
from bs4 import BeautifulSoup
import job_summary

# We parse the data from the bdjobs.com home page
r = urllib.request.urlopen('http://bdjobs.com/').read()
soup = BeautifulSoup(r, "lxml")

#%%
# Get the different functional categories and their urls 
job_cats = soup.find_all("div", class_="category-list padding-mobile functional active")
category_urls = [cat['href'] for cat in job_cats[0].find_all('a', href=True)]

#%%
#I am just running it for one of the categories, this can of course be done for all categories
# This can also be done for industrial categories as well
cat = category_urls[0]
r_new = urllib.request.urlopen(cat).read()
cat_soup = BeautifulSoup(r_new, "lxml")
jobs = cat_soup.find_all("div", class_="col-md-12")

#%%
#Get the job urls for the category chosen
# The main problem lies here, we can only get 20 jobs per page, and I cannot manage to go to next page

job_url = []
for i in range(len(jobs)):
    job0_urls = [job['href'] for job in jobs[i].find_all('a', href=True)]
    for url in job0_urls:
        if('jobdetails' in url):
            job_url.append('http://jobs.bdjobs.com/'+url)
            
#%%
#Sample, get job_summary for one of the job_urls
info = job_summary.get_job_details(job_url[0])
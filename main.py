#importables
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

#initialize the webdriver and opening the desired website
PATH ="C:\Program Files (x86)\chromedriver.exe"
url = "https://wuzzuf.net/jobs/egypt"
driver = webdriver.Chrome(PATH)
driver.get(url)

#define the jobs we want to scrap
job_names =["Full stack developer","Frontend Developer","backend developer","customer service","data scientist","data analyst","sales agent","chef"]

#initialize a data frame and creating the header names
fields=["job_title","skills","experience","job_requirement"]
df =pd.DataFrame()

try:
    #main loop for searching and scraping
    for job_t in job_names:

        #getting the search bar element and typing the desired job
        search_title = driver.find_element_by_class_name("search-bar-input")
        search_title.send_keys(job_t)
        search_title.send_keys(Keys.RETURN)

        #wait statment untill the element is loaded inpage
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "div"))
        )

        #searching for job titles and storing it into an array
        titles = element.find_elements_by_tag_name("h2")
        #initializing counter and job title array to store job names 
        #and to loop on the count of the page titles
        counter =0
        jobs =[]
        for title in titles:
            if counter < 15:
                job_title = title.text
                jobs.append(job_title)
                print(job_title)
            counter=counter+1
        time.sleep(100)
        for i in range(15):
            #secondry loop for storing the job_title,skills,experience,job_requirement in a csv file
            exps=[]
            skls=[]
            reqs=[]
            counter =1
            time.sleep(2)
            search_jobs = driver.find_element_by_css_selector("#app > div > div.css-1omce3u > div > div > div:nth-child(2) > div:nth-child("+str(i+1)+") > div > div.css-laomuu > h2 > a")
            search_jobs.send_keys(Keys.RETURN)
            #get current window handle
            p = driver.current_window_handle
            #get first child window
            chwd = driver.window_handles
            for w in chwd:
            #switch focus to child window
                if(w!=p):
                    driver.switch_to.window(w)
            print(driver.title)
            skills = driver.find_elements_by_class_name("css-158icaa")
            for skill in skills:
                if counter > 2:
                    skls.append(skill.text)
                    print(skill.text)
                counter=counter+1
            if driver.find_element_by_class_name("css-4xky9y") != None:
                experience = driver.find_element_by_class_name("css-4xky9y")
                exps = experience.text
                print(experience.text)
            job_requirment = driver.find_element_by_class_name("css-1t5f0fr")
            reqs = job_requirment.text
            reqs=reqs.replace(",",".")
            reqs=reqs.replace("\n"," ")
            print(job_requirment.text)
            driver.close()
            driver.switch_to.window(p)
            df = df.append({"job_title":jobs[i],"skills":skls,"experience":exps,"job_requirement":reqs}, ignore_index=True)
            df.to_csv("jobs.csv")
            print(jobs[i])

        #return one page to the search page and clearing the search bar
        driver.execute_script("window.history.go(-1)")
        driver.find_element_by_class_name("search-bar-input").clear()
    time.sleep(10)
finally:
    driver.quit()




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 16:37:04 2021

@author: adi
"""
#Note: PHASTER does not allow more than 40MB file size so we need to
#create multiple windows that run each file separately
#so that we can combine the results later

#https://phaster.ca/
import os

#!pip install selenium

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options

#To automatically download to designated folder
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.helperApps.alwaysAsk.force", False)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", "/mnt/data/Data/Annotation_prokka/allFNAfiles/phaster_out/webDownloads") 
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/xml,text/plain,text/xml,image/jpeg,text/eml");        

#List of all FNA file names
files=open('/mnt/data/Data/Annotation_prokka/allFNAfiles/list_filenames.txt','r')

#List declaration and initialization
driver=['driver_space']*47

#Create a firefox driver with specific profile preferences
#Then go to PHASTER homepage
#Upload the FNA file
#Check the multiple contigs parameter (FNA files may have >1 contig)
#Submit and loop back for the next file

for fil in enumerate(files):
    print(fil[0],fil[1])
    driver[fil[0]]=webdriver.Firefox(executable_path="/mnt/data/Data/Annotation_prokka/allFNAfiles/phaster_out/geckodriver",firefox_profile = fp)
    driver[fil[0]].get("https://phaster.ca/")
    s = driver[fil[0]].find_element_by_xpath("//input[@type='file']")
    print((fil[1]))
    s.send_keys(fil[1].rstrip('\n'))
    driver[fil[0]].execute_script("arguments[0].click();", driver[fil[0]].find_element_by_id("contigs"))
    submit = driver[fil[0]].find_element_by_id('file-submit')
    submit.click()

#Wait 2 hours before fetching URLs to download
driver[fil[0]].implicitly_wait(7200)

#By now the results should have loaded and all windows will have new URLs

#Create a backup of all 47 driver sessions
print(driver)
driver_backup=driver

#Save list of all zip files here (list acts as backup as well)
ref_driver_zips=[]
for f in range(0,47):
    print(f,driver[f].current_url )
    if(driver[f].current_url is not None):
        url = driver[f].current_url+'.zip'
        print(url)
        ref_driver_zips.append(url)
    else:
        print('Not Done!!!!!!!!!!!')
        
#get all zips, verify you don't have to check the download popup box everytime
#if you have to do it manually, I suggest:
    #1. fixing the firefox profile variable above since it may be out of date
    #2. creating another agorithm to fetch the zip files from the URLs listed in ref_driver_zips variable
try:  
    for fil in range(0,47):
        url = driver[fil].current_url+'.zip'
        print('Getting: ',url)
        try:
            driver[fil].get(url)
        except:
            print(fil,' not done yet, download manually')
finally:
    print('JOB DONE ACCORDING TO SELENIUM, CHECK OUTPUT DIRECTORY')

'''
For a single PHASTER run:
    
#driver = webdriver.Firefox(executable_path="/mnt/data/Data/Annotation_prokka/allFNAfiles/phaster_out/geckodriver",firefox_profile = fp)
#driver.get("https://phaster.ca/")

#s = driver.find_element_by_xpath("//input[@type='file']")
#s.send_keys("/mnt/data/Data/Annotation_prokka/allFNAfiles/annot_PaLo1.unicycler_normal.fna")
#driver.execute_script("arguments[0].click();", driver.find_element_by_id("contigs"))


#submit = driver.find_element_by_id('file-submit')
#submit.click()

#wait until page is processing
#try:
#    WebDriverWait(driver, 1200).until(expected_conditions.presence_of_element_located((By.XPATH, "//[span@class='wishart wishart-not-available'][0]")))
#    print('Results are loaded')
#finally:  
#    url = driver.current_url+'.zip'
#    driver.get(url)

'''
#!/usr/bin/env/webcrawl python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 11:31:44 2022

Web Scrape of Beige Book html files years 1996-2022:
Main Archive page: https://www.federalreserve.gov/monetarypolicy/beige-book-archive.htm

This program usese Urllib combined with BeautifulSoup to find the links to each
of the beige book hmtl files. Then a headless browser is used to grab each of 
the beige books. The headless browser is used because some of the beigebook
pages dont store the text on the page and pull the text from a diffrent server. 
The headless browser is much slower but its able to get information that urllib 
cannot. Then the beige book html files are saved locally in a user specified path. 


@author: averydavis
"""

# ------------------ prepare work space 
from bs4 import BeautifulSoup 
import urllib.request
import time
from selenium import webdriver
import io


# Grab Currrent Time Before Running the Code
start = time.time()

##  create functions that will be called in this program 

#grab raw fed pages 
def lib_request(url):
    #header informaion (needed to access fed website)
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    request=urllib.request.Request(url,None,headers) #The assembled request
    response = urllib.request.urlopen(request) # open website
    raw = response.read() # The grab the website
    return raw 

#parse beige book raw HTML page 
def soup_tree(raw_page):
    soup_page = BeautifulSoup(raw_page,"html.parser")
    return soup_page

#grab beige books with text
def headless_browser(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome("driver/chromedriver.exe", options=options) #Change chromedriver path accordingly
    driver.get(url)
    driver.implicitly_wait(10)
    html = driver.page_source
    driver.close()
    return(html)


## ----------------- Step 1.
# vist and grab main archive page containing 1996-2021 beige books 
# then parse page tree with beautifulsoup
# find and store links to each years beige books page

# use function to grab archive main page 
main_page = lib_request("https://www.federalreserve.gov/monetarypolicy/beige-book-archive.htm")
    
# create soup tree
main_soup = soup_tree(main_page)

# find all the links on main page 
links = main_soup.findAll("a",href=True)

## from the main page assemble the year links 
pub_links = []   
for link in links:
    pub_links.append("http://www.federalreserve.gov" + link.attrs["href"])
# filter out the uneeded links 
years = pub_links[189:215]



## ----------------- Step 2.
## visit each of the year links and grab the page and store it 
#  turn each page into a soup tree
#  lastly pull all of the month page links out of the soup

year_pages = [] 
for years in years: 
    year_pages.append(lib_request(years)) # The data u need

year_soup = []  
for year_pages in year_pages: 
    year_soup.append(soup_tree(year_pages))
    
month_links = []
for year_soup in year_soup:
    month_links.append(year_soup.find_all('a', href=True, text=('HTML')))

# month_links is a nested  
# outter list is years 
# inner list is months 



### ----------------- Step 3.
## A.)
# we have collected the links for each beige book but some of them are broken 
# we must assemble the broken links so we can acess the beige books 
## B.)
# upon futher inspection of the websites the links we have gathered that come 
# from 1995-2010 are the summarys. to get the full report we must 
# change those link sightly 

#----- A.)
# Flatten nested list so its eaier to work with 
regular_list = month_links
flat_list = [item for sublist in regular_list for item in sublist]

# slice the list because some of the links are not complete 
broken_link = flat_list[0:39] #2011-2021
complete_link = flat_list[40:201] #1996-2010

# pull out the complete links
reg_link = []
for complete_link in complete_link:
    reg_link.append(complete_link["href"])

# assemble working links then pull them out
fixed_link = []
for broken_link in broken_link:
    fixed_link.append("http://www.federalreserve.gov" + broken_link.attrs["href"])
    
# add the two lists togther 
bblinks = fixed_link + reg_link
# so now we have the links to each of the beige books locations and we only need to download the websites. 
 
# ----- B.)
bbsummary= bblinks[86:199]  
newfull= bblinks[0:85] 

# cut off the end of each link 
prefix = []
for bbsummary in bbsummary:
    prefix.append(bbsummary.removesuffix('default.htm'))
# replace with correct ending 
oldfull = []    
for prefix in prefix: 
    oldfull.append((prefix + 'FullReport.htm'))


bb_reports = newfull + oldfull 
# location of all of the full beige book reports 



## ----------------- Step 4.
# go to the 2022 page to grab beige books then create tree 
#  lastly grab links to beige books 

now_page = lib_request("https://www.federalreserve.gov/monetarypolicy/publications/beige-book-default.htm")

#parse main page 
soup_current = soup_tree(now_page)

## pull links of intrest from each of the 2022 page 
nowlinks =soup_current.find_all('a', href=True, text=('HTML'))
# links for each beige book page 

readynow = []
for nowlinks in nowlinks:
    readynow.append("http://www.federalreserve.gov" + nowlinks["href"])
    
# This part of the code is important 
# its redundent but important for naming the files later
locnames = readynow + bb_reports
#create two lists of the file urls 
bblinksfull = locnames



## ----------------- Step 5.
## visit each of the year links and grab the page and store it in a list 


beige_books_raw = [] 
for bblinksfull in bblinksfull: 
    beige_books_raw.append(headless_browser(bblinksfull)) 


## ----------------- Step 6.
# the file will be named by publication date and the easiset way to get that 
# is from the link to each beige book 
 

firstn = locnames[0:44]   #sclice of list

lfirst = []
for firstn in firstn:
    lfirst.append(firstn[54:60]) #sclice of strings 
    
#grab file names
secondn = locnames[45:90]   #sclice of list

lsecond = []
for secondn in secondn:
    lsecond.append(secondn[65:71]) #sclice of strings 
    
#grab file names 
thirdn = locnames[91:203]  #sclice of list

lthird = []
for thirdn in thirdn:
    lthird.append(thirdn[51:57]) #sclice of strings 
    
#reassemble file names 
FileName = lfirst + lsecond + lthird


# assemble a file path using file names we created 
FileLocation = []
for FileName in FileName:
    FileLocation.append("/Users/averydavis/Desktop/beigebook_nlp/html_data/" + FileName+".html")
    


## ----------------- Step 7.
# save the beige books locally 
#using the zip funtion to combine the file path with the contents 
# ONLY RUN THIS ONE TIME BECAUSE IT SAVES ALL BEIGE BOOKS lOCALLY 

moniker = FileLocation
contents = beige_books_raw

for (a,b) in zip(moniker,contents):
    with io.open(a, "w", encoding="utf-8") as f:
        f.write(b)
        f.close()
      


# Grab Currrent Time After Running the Code
end = time.time()
#Subtract Start Time from The End Time
total_time = end - start
run_t= round(total_time,2)

print('...File Download completed! (Runtime:'+ str(run_t)+" Seconds)"+" (Downloaded: "+str(len(contents))+" files)")
        

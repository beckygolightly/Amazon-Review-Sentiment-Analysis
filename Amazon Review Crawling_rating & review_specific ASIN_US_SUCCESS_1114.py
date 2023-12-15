import driver as driver
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import random
import time
import re
import pandas as pd
import requests
import math
from selenium.webdriver.common.by import By

# ## entering specific ASIN for result
# print("Please enter review page url that you want to crawl")
# url=input()
# # https://www.amazon.com/BIOLIGHT-KM-Headlight-Halogen-Replacement/product-reviews/B08B3PVF6Y
# cookie={url}

# ## Adjust chrome driver ##
# driver = webdriver.Chrome(executable_path="C:/Users/User-Pc/chromedriver_win32/chromedriver.exe")
# firts_page = "https://www.amazon.com/BIOLIGHT-KM-Headlight-Halogen-Replacement/product-reviews/B08B3PVF6Y/ref=cm_cr_arp_d_paging_btm_next_2?pageNumber=1"
# driver.get(firts_page)
500

def Requestpage(page):

    print("Parsing request is proceed right now, wait for a sec :)")
    base_url = "https://www.amazon.com/Real-Barrier-Extreme-Cream-Moisturising/product-reviews/B094VF71QC/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews"
    url = base_url + '&pageNumber=' + page
    print(url)
    # driver = webdriver.Chrome(executable_path="C:/Users/User-Pc/chromedriver_win32/chromedriver.exe")

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36', 'referer': url}
    cookie = {}

    response = requests.get(url, cookies=cookie, headers=header)
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup)

    time.sleep(5)
    if response.status_code == 200:
        print()
        return response
    else:
        return "Error"

## Review date ##
dates = []
titles = []
ratings=[]
reviews=[]

## Adjust how manu reviews would be crawled ##
print("please enter the total review count of the product")
review_count_xpath = driver.find_element(BY.XPATH,"//*[@id='filter-info-section']/div")
review_count_replace = review_count_xpath.text
review_count = review_count.replace(" total ratings, 43 with reviews","")

how_many_page = math.ceil(total_review_count_raw/10.0)
print(how_many_page, "page will be crawled")

for a in range(how_many_page):
    Requestpage(str(a+1))
    # response = Requestpage('&pageNumber=' + str(a+1))
    # soup = BeautifulSoup(response.content, "html.parser")

    date_xpath = dirver.find_element(BY.XPATH,"//*[@id='customer_review-R1WMVXZT6EQ8JZ']/span")
    for t in date_xpath:
        dates.append(t.text)
    print("total counts of [dates]: ", len(dates))

    title_xpath = driver.find_element(BY.XPATH, "//*[@id='customer_review-R1WMVXZT6EQ8JZ']/div[j]/a/span[j]")
    for j in title_xpath:
        titles.append(j.text)
    print("total counts of [titles]: ", len(titles))

    reviewrating_xpath = driver.find_element(BY.XPATH,"//*[@id='customer_review-R3ECYT2982OAOW']/div[m]/a/i")
    for m in reviewrating_xpath:
        ratings.append(m.text)
        m.text.replace("", ".0 out of 5 stars")
    print("total counts of [ratings]: ", len(ratings))

    reviewbody_xpath = driver.find_element(BY.XPATH,"//*[@id='customer_review-R2X3TJ10W992SI']/div[s]/span/span")
    for s in reviewbody_xpath:
        reviews.append(s.text)
    print("total counts of [reviews]: ", len(reviews))

    # soup version
    # for t in soup.find_all("span", {'data-hook': "review-date"}):
    #     dates.append(t.text)
    # print("total counts of [dates]: ", len(dates))
    #
    # for j in soup.findAll("a", {'data-hook': "review-title"}):
    #     titles.append(j.text)
    # print("total counts of [titles]: ", len(titles))
    #
    # for m in soup.findAll('i', class_='review-rating'):
    #     ratings.append(m.text)
    #     m.text.replace("", ".0 out of 5 stars")
    # print("total counts of [ratings]: ", len(ratings))
    #
    # for s in soup.findAll("span", {'data-hook': "review-body"}):
    #     reviews.append(s.text)
    # print("total counts of [reviews]: ", len(reviews))

print(dates)
print(titles)
print(ratings)
print(reviews)

## save data into excel file
# making a data frame with a dictionary form
rev={
    'Date':dates,
    'Title':titles,
     'Rating':ratings,
     'Review':reviews,
    }

# matching the count of columns and rows
review_data=pd.DataFrame.from_dict(rev, orient='index')
review_data=review_data.transpose()

review_data.head(5)

review_data.shape

# converting the dataframe to a csv file so as to use it later for further analysis
review_data.to_csv('Scraping reviews_rating & review_RB_Extreme Cream.csv')
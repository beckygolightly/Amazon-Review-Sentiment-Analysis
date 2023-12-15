import os
import driver as driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import random
import time
from time import sleep
import re
import pandas as pd
import math
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
# from fake_useragent import UserAgent
from urllib.request import Request, urlopen
# from random_user_agent.user_agent import UserAgent
# from seleniumwire import webdriver
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from zenrows import ZenRowsClient

## 메커니즘 정리 ##
# 1. 원하는 ASIN 입력
# 2. ASIN사이트로 오픈
# 3. fake proxy & user agent로 session 접속
# 4. HTML 파싱
# 5. Review 모두보기 링크 따오기

# ## Acess to product page ##
# # Here I provide some proxies for not getting caught while scraping
# ua = UserAgent() # From here we generate a random user agent
# proxies = [] # Will contain proxies [ip, port]

# def MakingRandomProxy(page):
#     # Retrieve latest proxies
#     proxies_req = Request(page)
#     proxies_req.add_header('User-Agent', ua)
#     proxies_doc = urlopen(proxies_req).read().decode('utf8')
#
#     soup = BeautifulSoup(proxies_doc, 'html.parser')
#     proxies_table = soup.find(id='proxylisttable')
#
#     # Save proxies in the array
#     for row in proxies_table.tbody.find_all('tr'):
#         proxies.append({
#             'ip': row.find_all('td')[0].string,
#             'port': row.find_all('td')[1].string
#         })
#
#     # Choose a random proxy
#     proxy_index = random_proxy()
#     proxy = proxies[proxy_index]
#
#     for n in range(1, 20):
#         req = Request(page)
#         req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')
#
#         # Every 10 requests, generate a new proxy
#         if n % 10 == 0:
#             proxy_index = random_proxy()
#             proxy = proxies[proxy_index]
#
#         # Make the call
#         try:
#             my_ip = urlopen(req).read().decode('utf8')
#             print('#' + str(n) + ': ' + my_ip)
#             clear_output(wait=True)
#         except:  # If error, delete this proxy and find another one
#             del proxies[proxy_index]
#             print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
#             proxy_index = random_proxy()
#             proxy = proxies[proxy_index]
#
# ## Retrieve a random index proxy (we need the index to delete it if not working)
# def random_proxy():
#     return random.randint(0, len(proxies) - 1)
#
# if __name__ == '__MakingRandomProxy__':
#     MakingRandomProxy()

def RequestPage(page):
    ## Chrome profile control
    # options = webdriver.ChromeOptions()
    # options.headless = True
    # options.add_argument(
    #     "user-data-dir=C:/Users\juntaehwang\AppData\Local\Google\Chrome/User Data")  # Path to your chrome profile
    # options.add_argument("--profile-directory=Profile 2")

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    # premium proxy server
    proxy = "http://<YOUR_ZENROWS_API_KEY>:js_render=true&premium_proxy=true@proxy.zenrows.com:8001"
    proxies = {"http": proxy, "https": proxy}

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        # 'User-Agnet': user_agent, "Accept-Language": "en-US, en;q=0.5",
        'referer': page}
    cookie = {}

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    try:
        client = ZenRowsClient("e79e20e701434096975778dc263e82583c5be1bc")
        params = {"js_render": "true", "antibot": "true", "premium_proxy": "true"}
        response = client.get(page, params=params)
        print(response.text)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup)

    except requests.exceptions.ConnectionError:
        print("Connection error occurred")

    # try:
    #     response = requests.get(page, cookies=cookie, headers=header, proxies=proxies, verify=False)
    #     time.sleep(random.randint(1, 5))
    #     print(response.status_code)
    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     print(soup)
    #
    # except requests.exceptions.ConnectionError:
    #     print("Connection error occurred")


    # if response.status_code == 200:
    #     print("requested page is connected")
    #     return response
    #
    # else:
    #     return "Error"

## old version
# def Requestpage(page):
#
#     print("Parsing request is proceed right now, wait for a sec :)")
#     base_url = "https://www.amazon.com/Real-Barrier-Extreme-Cream-Moisturising/product-reviews/B094VF71QC/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
#
#     url = base_url + page
#     # driver = webdriver.Chrome(executable_path="C:/Users/User-Pc/chromedriver_win32/chromedriver.exe")
#
#     header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36', 'referer': url}
#     cookie = {}
#     requested_page = requests.get(url,cookies=cookie,headers=header)
#     # page.driver.get(url)
#     print(url)
#
#     time.sleep(5)
#     if requested_page.status_code == 200:
#         print()
#         return requested_page
#     else:
#         return "Error"

## new version
## 1. Enter ASIN info
print("Please enter the ASIN for access to review page")
ASIN = str(input())

## Opening Page & Roading HTML of product page
print("We're accessing to product page now :)")
Amazon_base_url = "https://www.amazon.com/dp/"
product_page = Amazon_base_url + ASIN
print(product_page)

# create the ChromeDriver instance with custom options
service = ChromeService(excecutable_path="C:/Users\juntaehwang\Desktop\새 폴더\Programs\chromedriver_win32\chromedriver.exe")
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)
driver.get(product_page)
time.sleep(random.randint(1, 5))
# MakingRandomProxy(product_page)
RequestPage(product_page)
product_page_html = driver.page_source
print("product_page_html: ",product_page_html)

## Get Reveiw page and access to it ##
# review_page = soup.find_all('a', {'data-hook': "see-all-reviews-link-foot"},href=True)
review_page = "https://www.amazon.com/Real-Barrier-Extreme-Cream-Moisturising/product-reviews/B094VF71QC/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews"
# review_page.send_keys('\n')
print("review_page_html: ",review_page)

# create the ChromeDriver instance with custom options
service = ChromeService(
    excecutable_path="C:/Users\juntaehwang\Desktop\새 폴더\Programs\chromedriver_win32\chromedriver.exe")
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

driver.get(review_page)
time.sleep(random.randint(1, 5))
# MakingRandomProxy(product_page)
RequestPage(review_page)
review_page_html = driver.page_source
print("review_page_html: ", product_page_html)

## Crawling Review data into data frame ##
dates = []
titles = []
ratings = []
reviews = []

## Adjust how manu reviews would be crawled ##
print("plase enter the total review count of the product")
total_review_count_raw = int(140)
how_many_page = math.ceil(total_review_count_raw / 10.0)
print(how_many_page, "page will be crawled")

for a in range(how_many_page):
    response = RequestPage(review_page+'&pageNumber=' + str(a + 1))
    soup = BeautifulSoup(response.content, "html.parser")
    time.sleep(random.randint(1, 10))

    for t in soup.find_all("span", {'data-hook': "review-date"}):
        dates.append(t.text)
    print("total counts of [dates]: ", len(dates))

    for j in soup.findAll("a", {'data-hook': "review-title"}):
        titles.append(j.text)
    print("total counts of [titles]: ", len(titles))

    for m in soup.findAll('i', class_='review-rating'):
        ratings.append(m.text)
        m.text.replace("", ".0 out of 5 stars")
    print("total counts of [ratings]: ", len(ratings))

    for s in soup.findAll("span", {'data-hook': "review-body"}):
        reviews.append(s.text)
    print("total counts of [reviews]: ", len(reviews))

print(dates)
print(titles)
print(ratings)
print(reviews)

## save data into excel file ##
# making a data frame with a dictionary form
rev = {
    'Date': dates,
    'Title': titles,
    'Rating': ratings,
    'Review': reviews,
}

# matching the count of columns and rows
review_data = pd.DataFrame.from_dict(rev, orient='index')
review_data = review_data.transpose()

review_data.head(5)

review_data.shape

# converting the dataframe to a csv file so as to use it later for further analysis
review_data.to_csv('NeoPharm_RB_Extreme Cream_Reviews_2311.csv')

# except:
#     print("I cannot find the link of review page")
#

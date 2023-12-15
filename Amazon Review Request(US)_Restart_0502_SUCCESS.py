import driver as driver
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
from selenium.webdriver.chrome.options import Options

## Loading default browser witn login info ##
# https://stackoverflow.com/questions/35641019/how-do-you-use-credentials-saved-by-the-browser-in-auto-login-script-in-python-2
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("user-data-dir=C:/Users/Becky/AppData/Local/Google/Chrome/User Data/Profile 1") #Path to your chrome profile
driver = webdriver.Chrome(executable_path="C:/Users/Becky/chromedriver_win32/chromedriver.exe", options=options)

## Opening url ##
driver.get("https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page=1")

## Adjusting date ##
baseUrl = "https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page=1"
html_text = requests.get(baseUrl).text
soup = BeautifulSoup(html_text, 'html.parser')

start_date = driver.find_element_by_xpath("//*[@id='myo-date-range-from-cal']/div[2]/div/div/div/input")
start_date.click()
start_date.clear();
start_date.send_keys("21.11.23");
end_date = driver.find_element_by_xpath("//*[@id='myo-date-range-to-cal']/div[2]/div/div/div/input")
end_date.click()
end_date.clear();
end_date.send_keys("21.12.6");

# selenium ver
## Order number ##
# Control how many order number
time.sleep(5)
timeout = 5
howmany = driver.find_element_by_xpath("//*[@id='myo-layout']/div[2]/div[1]/div[1]/div/span[1]").text
num1 = howmany.replace("건","")
num2 = num1.replace("주문","")
print(num2)

# order_links = []
#
# for i in range(int(num2)):
#     time.sleep(5)
#     timeout = 5
#     # timeout = 5
#     xpath = driver.find_elements_by_xpath("//*[@id='orders-table']/tbody/tr[" + str(i+15) + "]/td[3]/div/div[1]/a")
#     for i in xpath:
#         print(i.get_attribute("href"))
#         order_links.append(i.get_attribute("href"))
#
#     time.sleep(2)
#     timeout = 2

# ## request reveiew_v1 ## - 순차적으로 할때 한두개씩 생겨서 동일 링크로밖에 못들어가는 오류 발생
#     for j in range(len(order_links)):
#
#         driver.get(order_links[j])
#
#         # request review
#         time.sleep(2)
#         timeout = 2
#         request_review = driver.find_element_by_css_selector("#MYO-app > div > div.a-row.a-spacing-medium > div.a-column.a-span10 > div > div:nth-child(1) > div:nth-child(2) > div.a-column.a-span6.a-text-right.a-span-last > span:nth-child(2) > span > a")
#         request_review.send_keys('\n')
#
#         # click yes
#         time.sleep(2)
#         timeout = 2
#         yes = driver.find_element_by_css_selector("#ayb-reviews > div > kat-button")
#         yes.send_keys('\n')
#
#         j = j + 1

## request reveiew_v2 ## - 리뷰요청하고 리뷰리퀘스트 밖으로 나가기

print("Please enter #number you wanna start from")
restart = int(input())
# howmany = range(int(num2)-int(restart))
howmany = range(int(123))
print(howmany)

for j in howmany:
        order_links = []
        # order_links_text = []

        time.sleep(5)
        timeout = 5

        if int(restart) <= 100:
            driver.get("https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page=1")

        if int(restart) > 100 and int(restart) <= 200:
            driver.get("https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page=1")

        if int(restart) > 300:
            driver.get("https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page=1")

        time.sleep(5)
        timeout = 5

        xpath = driver.find_elements_by_xpath("//*[@id='orders-table']/tbody/tr[" + str(restart+j) + "]/td[3]/div/div[1]/a")

        time.sleep(2)
        timeout = 2

        for i in xpath:
            print(i.get_attribute("href"))
            # print(i.text)
            order_links.append(i.get_attribute("href"))
            # order_links_text.append(i.text)

            time.sleep(5)
            timeout = 5

        for z in range(len(order_links)):
            driver.get(order_links[z])
            # print(len(order_links))

            try:
                # request review
                time.sleep(5)
                timeout = 5
                request_review = driver.find_element_by_css_selector("#MYO-app > div > div.a-row.a-spacing-medium > div.a-column.a-span10 > div > div:nth-child(2) > div:nth-child(2) > div.a-column.a-span6.a-text-right.a-span-last > span:nth-child(2) > span > a")
                try:
                        request_review.send_keys('\n')

                        # click yes
                        time.sleep(3)
                        timeout = 3
                        yes = driver.find_element_by_css_selector("#ayb-reviews > div > kat-button")
                        yes.send_keys('\n')

                except:
                        print("There's no button written review request")
                        if restart <= 100:
                            driver.get("https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page=1")

                        if restart > 100 and restart <= 200:
                            driver.get("https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page=1")

                        if restart > 300:
                            driver.get("https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page=1")

            except:
                print("Review Request on this order has already been reqeusted")

                # turing page
                # if int(restart) <= 100:
                driver.get("https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page=1")
                #
                # if int(restart) > 100 and int(restart) <= 200:
                #     driver.get("https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page=2")
                #
                # if int(restart) > 300:
                #     driver.get("https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page=3")

        # turing page
        # if int(restart) <= 100:
        # driver.get("https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page=2")

        # if int(restart) > 100 and int(restart) <= 200:
        #     driver.get("https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page=2")
        #
        # if int(restart) >300:
        #     driver.get("https://sellercentral.amazon.com/orders-v3/ref=xx_myo_dnav_xx?page=3")

# ## request reveiew_v2 ## - 링크 수집하는 loop 안에서 바로 다음 링크로 넘어가도록 설정
# 
# #xpath = driver.find_elements_by_xpath("//*[@id='orders-table']/tbody/tr[" + str(i+11) + "]/td[3]/div/div[1]/a")
# 
#         # request review
#         time.sleep(2)
#         timeout = 2
#         request_review = driver.find_element_by_css_selector("#MYO-app > div > div.a-row.a-spacing-medium > div.a-column.a-span10 > div > div:nth-child(1) > div:nth-child(2) > div.a-column.a-span6.a-text-right.a-span-last > span:nth-child(2) > span > a")
#         request_review.send_keys('\n')
# 
#         # click yes
#         time.sleep(2)
#         timeout = 2
#         yes = driver.find_element_by_css_selector("#ayb-reviews > div > kat-button")
#         yes.send_keys('\n')
# 
#         for i in xpath[i]:
#             i = i + 1
#             xpath.append(xpath[i])
#         print(xpath)
# 
# print("SUCCESS")
# ## manually clicking each link ##
# # eachLink = driver.find_element_by_xpath("//*[@id='orders-table']/tbody/tr[1]/td[3]/div/div[1]/a")
# # eachLink.click()
# time.sleep(10)
# timeout = 10
# eachLink = driver.find_element_by_css_selector("#orders-table > tbody > tr:nth-child(1) > td:nth-child(3) > div > div.cell-body-title > a")
# eachLink.send_keys('\n')
#
# ## submitting review requests by oreder link ##
# # request review
# time.sleep(10)
# timeout = 10
# request_review = driver.find_element_by_css_selector("#MYO-app > div > div.a-row.a-spacing-medium > div.a-column.a-span10 > div > div:nth-child(1) > div:nth-child(2) > div.a-column.a-span6.a-text-right.a-span-last > span > span > a")
# request_review.send_keys('\n')
#
# # yes
# time.sleep(10)
# timeout = 10
# yes = driver.find_element_by_css_selector("#ayb-reviews > div > kat-button")
# yes.send_keys('\n')
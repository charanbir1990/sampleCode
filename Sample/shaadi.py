from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
import time, string
from pprint import pprint
from datetime import datetime
import re
import random

driver = webdriver.Chrome()
driver.get('https://www.shaadi.com/registration/user/login')
driver.find_element_by_xpath('//input[@name="email"]').send_keys("charanbir1990@yahoo.com")
driver.find_element_by_xpath('//input[@name="password"]').send_keys("manisha@123")
driver.find_element_by_xpath('//input[@name="sign_in"]').click()
driver.get('https://my.shaadi.com/search/smart_search?pg_searchresults_id=search%3A783d0530245f9292e3f9636ac97a458f&vtype=list&spn=list')
time.sleep(10)
name = driver.find_element_by_xpath("//a[@class='ListItemStyles__ProNameLink-fbfFey hmDPJj']")
link = name.get_attribute('href')
driver.get(link)
while 1==1:
    try:
        time.sleep(2)
        driver.find_element_by_xpath('//button[text()="Connect Now"]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//button[text()="Connect"]').click()
        time.sleep(1)
    except:
        pass
    driver.find_element_by_xpath('//div[@class="styles__paginationText-gWhFMF cWITwO"]').click()


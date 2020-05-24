from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
import time, string, requests
from pprint import pprint
from datetime import datetime
import pandas as pd
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from lxml import etree
import lxml.html, lxml.etree
from xml.etree import ElementTree as etree
import random

# //button[@tabindex='0']



driver = webdriver.Chrome()
def clickOnButton():
    try:
        driver.find_element_by_xpath("//span[text()='Connect']/../..").click()
        ran = random.randint(1,4)
        print ran
        time.sleep(ran)
        clickOnButton()
    except:
        print "crash"
        driver.get('https://www.linkedin.com/mynetwork/')
        clickOnButton()

driver.get('https://www.linkedin.com/')
driver.find_element_by_xpath("//input[@class='login-email']").send_keys("*****@***.***") #email
driver.find_element_by_xpath("//input[@class='login-password']").send_keys("******") # password
driver.find_element_by_xpath("//button[text()='Log in']").click()
driver.get('https://www.google.com/')
driver.get('https://www.linkedin.com/mynetwork/')
clickOnButton()

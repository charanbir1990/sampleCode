from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
import time, string
from pprint import pprint
from datetime import datetime
import re
import random

#Amanneet
driver = webdriver.Firefox()
driver.get('https://web.whatsapp.com/')
raw_input("Press Enter to continue to enter in whatsapp")
driver.find_element_by_xpath('//span[@title="Sali"]').click()

file = open("whatsappText.txt", "r")
fileContext = file.read()
arratContextOfWords = re.findall(r'\S+', fileContext)
for word in arratContextOfWords:
    searchBar = driver.find_element_by_xpath('//div[@data-tab="1"]')
    searchBar.send_keys(word)
    driver.find_element_by_xpath('//span[@data-icon="send"]').find_element_by_xpath('..').click()

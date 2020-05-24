import requests
import time, string
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
import _thread
from requests import Session
import re
from robobrowser import RoboBrowser
import random

#http://icanhazip.com
#https://whatsmyip.com/
#url = 'https://api.ipify.org/?format=text'

#=MOD(A2,2)
#http://spys.one/en/https-ssl-proxy/
#http://spys.one/en/free-proxy-list/
#//td[@colspan='1'][1]/font[@class='spy14']/text()
#https://free-proxy-list.net/
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies
    
def select500(driver):
    try:
        count = len(driver.find_elements_by_xpath("//select[1]/option"))
        driver.find_element_by_xpath("//select[1]/option[{0}][@selected='']".format(count))
    except:
        print("changing ip count to 500 again")
        driver.find_element_by_xpath("//select[1]").click()
        driver.find_elements_by_xpath("//select[1]/option")[-1].click()
        select500(driver)
    
def get_ip():
    arrIp = []
    driver = firefox('')
    driver.get("http://spys.one/en/https-ssl-proxy/")
    driver.find_element_by_xpath("//select[1]").click()
    driver.find_elements_by_xpath("//select[1]/option")[-1].click()
    select500(driver)
    elements = driver.find_elements_by_xpath("//td[@colspan='1'][1]/font[@class='spy14']")
    for element in elements:
        arrIp.append(element.text)
    driver.quit()
    return arrIp
    
    
#user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
#profile.set_preference("general.useragent.override", "[user-agent {0}]".format(user_agent))
def firefox(proxy):
    profile = webdriver.FirefoxProfile()
    if (proxy != ''):
        agent_IP, agent_Port = proxy.split(":")
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.share_proxy_settings", True)
        profile.set_preference("network.http.use-cache", False)
        profile.set_preference("network.proxy.http", agent_IP)
        profile.set_preference("network.proxy.http_port", int(agent_Port))
        profile.set_preference('network.proxy.ssl_port', int(agent_Port))
        profile.set_preference('network.proxy.ssl', agent_IP)
        profile.set_preference('network.proxy.socks', agent_IP)
        profile.set_preference('network.proxy.socks_port', int(agent_Port))
        profile.update_preferences()
#    driver = webdriver.Firefox(firefox_profile=profile)
#    for hide browser
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, firefox_profile=profile)
    return driver
    
    
def requestPython(proxy, url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    headers = {'Content-Type': 'application/json; charset=utf-8', 'User-Agent': user_agent}
    proxies = {
      "http": "http://" + proxy,
      "https": "https://" + proxy,
    }
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
        return response
    except: pass
    
def roboBrowserInit(proxy):
    session = Session()
    session.proxies = {
      "http": "http://" + proxy,
      "https": "https://" + proxy,
    }
    browser = RoboBrowser(session=session)
#    browser.open("https://charanbir.com/covid19/")
#    print(browser.parsed)
    return browser

#    driver.find_element_by_xpath("//button[contains(@title,'Play')]").click()


        
        
def closeBrowser(driver, num):
    time.sleep(num)
    driver.quit()
    print("Quit after {0}".format(num))
    

url = "https://charanbir.com/blog/2"
count = 0


arrIp = get_ip()

for ip in arrIp:
    count += 1
    print(count)
    print(ip)
    driver = firefox(ip)
    agent = driver.execute_script("return navigator.userAgent")
    print(agent)
    driver.set_page_load_timeout(30)
    try:
        driver.get(url)
        ran = random.randint(1,60)
        _thread.start_new_thread( closeBrowser, (driver, ran, ) )
    except:
        driver.quit()
        print("Error: Quit immidatily")


    
    
time.sleep(60)


    




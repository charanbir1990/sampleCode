import time
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options

    
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
    options = Options()
    options.headless = False
    driver = webdriver.Firefox(options=options, firefox_profile=profile)
    return driver
    
    
    
driver = firefox("86.123.166.109:8080")
driver.get("https://charanbir.com/")
time.sleep(5)
driver.quit()

    




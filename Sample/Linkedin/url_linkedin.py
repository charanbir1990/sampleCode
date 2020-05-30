import threading
import asyncio
from pyppeteer import launch
import time
import random
import pymongo
from pprint import pprint
#https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/
#https://docs.python.org/3/library/tracemalloc.html

concrentNumberOfThreads = 4
arrThreads = []
arrOfIp = []
pending = 'pending'
running = 'running'
isIpApiHitting = True
count = 0
fileRead = open("names.txt", "r")
arrNames = []
for name in fileRead: arrNames.append(name.replace('\n',''))
fileRead.close()
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["LinkedIn"]
mycol = mydb["UserWithStatus"]


class NewThread (threading.Thread):
    def __init__(self, name, ip, count):
      threading.Thread.__init__(self)
      self.name = name
      self.ip = ip
      self.count = count
      self.status = pending
      
    def run(self):
        try:
            self.status = running
            asyncio.run(self.handelRequest())
            if (self in arrThreads):
                for i in range(0, len(arrThreads)):
                    if (self is arrThreads[i]):
                        if (arrThreads[i].status == running):
                            del arrThreads[i]
                            break
            for i in range(0,concrentNumberOfThreads):
                if (i < len(arrThreads)):
                    if (arrThreads[i].status == pending):
                        arrThreads[i].start()
                        print("count before finish: {0}".format(arrThreads[i].count))
            if (concrentNumberOfThreads > len(arrThreads)):
                if (isIpApiHitting == False):
                    if (len(arrNames) > 0):
                        getIps()
        except:
            pass
        self.printCurrentThreadsCount('Finished')
        
    def printCurrentThreadsCount(self,status):
        try:
            count = 0
            for i in range(0,len(arrThreads)):
                if (arrThreads[i].status == running):
                    count += 1
            print("{0}, running threads: {1}, pending threads: {2}".format(status, count, len(arrThreads)))
        except:pass

    async def handelRequest(self):
        try:
            self.browser = await launch({'headless': True,
#            'ignoreHTTPSErrors': True,
            'handleSIGINT': False,
            'handleSIGTERM': False,
            'handleSIGHUP': False,
            'args': [
                     '--proxy-server=' + self.ip,
                     '--no-sandbox',
#                     '--disable-setuid-sandbox',
#                     '--disable-dev-shm-usage',
#                     '--disable-accelerated-2d-canvas',
#                     '--disable-gpu',
#                     '--window-size=1440x900',
                     '--disable-infobars',
#                     '--lang=en',
                     ]
            })
            page = await self.browser.newPage()
#            await page.setExtraHTTPHeaders({ 'DNT': '1' })
            await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15')
            await page.setViewport({'width': 1440, 'height': 900})
            self.printCurrentThreadsCount('Started')
#            await page.goto('https://www.linkedin.com/', { 'waitUntil': 'networkidle2', 'timeout': 40*1000  })
            await page.goto('https://www.linkedin.com/')
            await page.waitForSelector('.intent-module')
            await page.waitFor(1000)
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            await page.click('ul[class=intent-module__list] li:nth-child(2)')
            await page.waitForXPath("//main[@class='empty-pserp-page']")
            await page.waitFor(1000)
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            await page.type('body > div > header > nav > section.search-bar > section:nth-child(3) > form > section:nth-child(1) > input', self.name)
            await page.waitFor(1000)
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            await page.click('.sign-in-card__dismiss-btn')
            await page.waitFor(1000)
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            await page.click('body > div > header > nav > section.search-bar > section:nth-child(3) > form > button')
            await page.waitForSelector('#main-content')
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            profileLinks = await page.Jx("//section//ul/li/a")
            for element in profileLinks:
                text = await page.evaluate('(element) => element.href', element)
                link = str(text).split('?')[0]
                arrCol = mycol.find({ "link": link })
                if (arrCol.count() == 0):
                    mydict = { "link": link, 'status': pending }
                    mycol.insert_one(mydict)
                    print(link)
            if self.name in arrNames:
                arrNames.remove(self.name)
                file = open("names.txt", "w")
                for name in arrNames:
                    file.write(name+'\n')
                file.close()
                print("pending names count: {0}".format(len(arrNames)))
            await page.close()
            await self.browser.close()
        except :
            print('error')
            try:await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            except: pass
            try:await page.close()
            except: pass
            try:await self.browser.close()
            except: pass
            if self.ip in arrOfIp:
                arrOfIp.remove(self.ip)
        





class GetIPProxies:
    def __init__(self):
        pass
        
    async def select500(self, page):
        try:
            await page.waitForXPath("//select[1]/option")
            count = await page.Jx("//select[1]/option[2][@selected='']")
        except:
            print("changing ip count to get 50 ip again")
            await page.waitFor(1000)
            await page.select('.clssel', '1')
            await self.select500(page)
            
    async def click(self, page, xpath):
        await page.waitForXPath(xpath)
        btnArr = await page.Jx(xpath)
        if (len(btnArr) > 0):
          await btnArr[0].click()
        
    
    
    async def getIp(self):
        try:
            arrIp = []
            browser = await launch({'headless': True,
            'handleSIGINT': False,
            'handleSIGTERM': False,
            'handleSIGHUP': False
            })
            page = await browser.newPage()
            await page.setViewport({'width': 1200, 'height': 800})
            await page.goto("http://spys.one/en/https-ssl-proxy/")
    #        await self.select500(page)
            xpath = "//td[@colspan='1'][1]/font[@class='spy14']"
            await page.waitForXPath(xpath)
            await page.waitFor(1000)
            elements = await page.Jx(xpath)
            for element in elements:
                text = await element.getProperty('innerHTML')
                json = await text.jsonValue()
                ip = json.split("<")[0]
                port = json.split(">")[-1]
                arrIp.append(ip + ":" + port)
            await browser.close()
            return arrIp
        except:
            return []

def checkIfAlreadyExist(name):
    isEsist = False
    for th in arrThreads:
        if th.name == name:
            isEsist = True

    return isEsist

def getIps():
    global isIpApiHitting
    global arrOfIp
    isIpApiHitting = True
    
    while (len(arrOfIp) < concrentNumberOfThreads):
        print("requist for get ip")
        ips = asyncio.run(GetIPProxies().getIp())
        arrOfIp += ips
        print("current no of ip: {0}".format(len(arrOfIp)))
        
    for ip in arrOfIp:
        global count
        if (len(arrNames) > 0):
            index = random.randint(0,(len(arrNames)-1))
            name = arrNames[index]
            if checkIfAlreadyExist(name) == False:
                count += 1
                thread = NewThread(name, ip, count)
                arrThreads.append(thread)

    for i in range(0,concrentNumberOfThreads):
        if (i < len(arrThreads)):
            if (arrThreads[i].status == pending):
                arrThreads[i].start()
                print("count after start: {0}".format(arrThreads[i].count))
                
    isIpApiHitting = False

getIps()

#thread = NewThread('anwar', '', 1)
#thread.start()


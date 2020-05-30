import threading
import asyncio
from pyppeteer import launch
import time
import random
import pymongo
from pprint import pprint
#https://miyakogi.github.io/pyppeteer/_modules/pyppeteer/launcher.html

concrentNumberOfThreads = 20
arrThreads = []
arrOfIp = []
pending = 'pending'
running = 'running'
finished = 'finished'
waiting = 'waiting'
isIpApiHitting = True
count = 0
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["LinkedIn"]
mycol = mydb["UserWithStatus"]

async def gotoOverRide(page, url, time):
    return await page.goto(url, {
        'waitUntil': 'networkidle2',
        'timeout': time*1000
    })

class NewThread (threading.Thread):
    def __init__(self, name, ip, count):
      threading.Thread.__init__(self)
      self.name = name
      self.ip = ip
      self.count = count
      self.status = pending
      
    def run(self):
        print('Start')
        self.status = running
        self.printCurrentThreadsCount()
        asyncio.run(self.handelRequest())
        if (self in arrThreads):
            for i in range(0, len(arrThreads)):
                if (self is arrThreads[i]):
                    del arrThreads[i]
                    break
        for i in range(0,concrentNumberOfThreads):
            if (i < len(arrThreads)):
                if (arrThreads[i].status == pending):
                    arrThreads[i].start()
                    print(arrThreads[i].count)
        if (concrentNumberOfThreads > len(arrThreads)):
            if (isIpApiHitting == False):
                rec = mycol.find_one({ "status": pending })
                if rec != None:
                    getIps()
        print('Finish')
        
    def printCurrentThreadsCount(self):
        count = 0
        for i in range(0,len(arrThreads)):
            if (arrThreads[i].status == running):
                count += 1
        print("Current Number of Threads: {0}".format(count))
        
    async def browser(self,ip):
        head = True
        if (ip == ''):
            return await launch({'headless': head,
                'handleSIGINT': False,
                'handleSIGTERM': False,
                'handleSIGHUP': False,
                })
        else:
            return await launch({'headless': head,
                'handleSIGINT': False,
                'handleSIGTERM': False,
                'handleSIGHUP': False,
                'args': [
                '--proxy-server=' + ip,
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--window-size=1440x900',
                '--disable-infobars',
                '--lang=en'
                ]
                })

    async def initPage(self, browser):
        page = await browser.newPage()
        await page.setExtraHTTPHeaders({ 'DNT': '1' })
        await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15')
        await page.setViewport({'width': 1440, 'height': 900})
        return page

    async def handelRequest(self):
        self.browser = await self.browser(self.ip)
        page = await self.initPage(self.browser)
        rec = mycol.find_one({ "link": self.name })
        if rec != None:
            nv = { "$set": { 'status': running } }
            mycol.update_one(rec, nv)
        try:
#            await gotoOverRide(page, 'https://www.linkedin.com/', 60)
#            await page.waitForSelector('.intent-module')
#            await page.waitFor(1000)
#            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            await gotoOverRide(page, self.name, 60)
            await page.waitForSelector('.top-card-layout')
#            await page.waitFor(1000)
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            html = await page.content()
            rec = mycol.find_one({ "link": self.name })
            if rec != None:
                nv = { "$set": { 'status': finished, 'html': html } }
                mycol.update_one(rec, nv)
        except : #AssertionError as error:
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            if self.ip in arrOfIp:
                arrOfIp.remove(self.ip)
            rec = mycol.find_one({ "link": self.name })
            if rec != None:
                nv = { "$set": { 'status': pending } }
                mycol.update_one(rec, nv)
            print("timeout error after 5 min")
        await page.close()
        await self.browser.close()
        
    async def clickWithXpath(self, page, xpath):
        await page.waitForXPath(xpath)
        btnArr = await page.xpath(xpath)
        print(btnArr)
        if (len(btnArr) > 0):
          await btnArr[0].click()




class GetIPProxies:
    def __init__(self):
        pass
        
    async def select500(self, page):
        try:
            await page.waitForXPath("//select[1]/option")
            count = await page.Jx("//select[1]/option[2][@selected='']")
            print(count[0])
        except:
            print("changing ip count to 50 again")
            await page.waitFor(1000)
            await page.select('.clssel', '1')
            await self.select500(page)
            
    async def click(self, page, xpath):
        await page.waitForXPath(xpath)
        btnArr = await page.Jx(xpath)
        if (len(btnArr) > 0):
          await btnArr[0].click()
        
    
    
    async def getIp(self):
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

def getIps():
    global isIpApiHitting
    global arrOfIp
    isIpApiHitting = True
    if (len(arrOfIp) < concrentNumberOfThreads):
        print('requisting for new ips')
        ips = asyncio.run(GetIPProxies().getIp())
        arrOfIp += ips
    for ip in arrOfIp:
        global count
        rec = mycol.find_one({ "status": pending })
        if rec != None:
            name = rec['link']
            nv = { "$set": { 'status': waiting } }
            mycol.update_one(rec, nv)
            count += 1
            thread = NewThread(name, ip, count)
            arrThreads.append(thread)

    for i in range(0,concrentNumberOfThreads):
        if (i < len(arrThreads)):
            if (arrThreads[i].status == pending):
                arrThreads[i].start()
                print(arrThreads[i].count)
    print("{0} Ip".format(len(arrOfIp)))
    isIpApiHitting = False

getIps()

def changeBackStatusToPending(status):
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myclient["LinkedIn"]
    mycol = mydb["UserWithStatus"]
    total = mycol.find({ "status": status })
    for i in range(0,total.count()):
        old = mycol.find_one({ "status": status })
        new = { "$set": { 'status': 'pending' } }
        mycol.update_one(old, new)

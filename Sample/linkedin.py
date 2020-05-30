import threading
import asyncio
from pyppeteer import launch
import time
import random
import pymongo
from pprint import pprint
#https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/

concrentNumberOfThreads = 30
arrThreads = []
arrOfIp = []
pending = 'pending'
running = 'running'
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
                if (len(arrNames) > 0):
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
        try:
            await gotoOverRide(page, 'https://www.linkedin.com/', 30)
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
            await page.waitFor(1000)
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
            arrNames.remove(self.name)
            pprint(arrNames)
            print('pending names:->')
            print(len(arrNames))
        except : #AssertionError as error:
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            print("timeout error")
            if self.ip in arrOfIp:
                arrOfIp.remove(self.ip)
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
           
arrNames = [
'Abhinav',
'Adit',
'Adhyan',
'Adrith',
'Advik',
'Agastya',
'Akshant',
'Amey',
'Ankit',
'Ansh',
'Anshul',
'Arijit',
'Aruj',
'Aryan',
'Ashok',
'Atharv',
'Avaneesh',
'Aviraj',
'Avyan',
'Avyukt',
'Ayush',
'Bhargav',
'Chandan',
'Chirag',
'Daiwik',
'Dilip',
'Darsh',
'Deepak',
'Dev',
'Dipankar',
'Eklavya',
'Eshaanth',
'Gaurav',
'Gautam',
'Harish',
'Harshad',
'Hitansh',
'Hrithik',
'Ishaan',
'Jagan',
'Jatin',
'Jeet',
'Jyotiraditya',
'Kairav',
'Kamal',
'Kanishk',
'Karan',
'Karthik',
'Kapil',
'Kavyansh',
'Kiaan',
'Krish',
'Lakshit',
'Lalit',
'Madhavaditya',
'Malhar',
'Manoj',
'Mayank',
'Mehul',
'Mihir',
'Mohan',
'Nakul',
'Naitik',
'Naksh',
'Naman',
'Navin',
'Nikshith',
'Nikunj',
'Nirav',
'Nivan',
'Om',
'Omkar',
'Pankaj',
'Parag',
'Parikshit',
'Parthik',
'Parthiv',
'Prabhas',
'Pranav',
'Pranith',
'Prashant',
'Prateek',
'Pratham',
'Pratyush',
'Prem',
'Pritam',
'Priyom',
'Raghav',
'Rajesh',
'Rakesh',
'Ramesh',
'Rajat',
'Rishaan',
'Rishaank',
'Rishit',
'Rohan',
'Sabhya',
'Sachit',
'Samar',
'Samrat',
'Sanjay',
'Sarthak',
'Sathvik',
'Shakti',
'Shamit',
'Shivaay',
'Shreyansh',
'Siddharth',
'Soham',
'Spandan',
'Sujal',
'Sumedh',
'Tanay',
'Tanmay',
'Tarak',
'Tushar',
'Utkarsh',
'Veer',
'Vishesh',
'Vivek',
'Vyas',
'Yashvir',
'Yuvaan',
'Yuvraj']

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
    if (len(arrOfIp) < concrentNumberOfThreads):
        print('requisting for new ips')
        ips = asyncio.run(GetIPProxies().getIp())
        arrOfIp += ips
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
                print(arrThreads[i].count)
    print("{0} Ip".format(len(arrOfIp)))
    isIpApiHitting = False

getIps()


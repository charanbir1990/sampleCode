import threading
import asyncio
from pyppeteer import launch
import time
import random

concrentNumberOfThreads = 5
arrThreads = []
pending = 'pending'
running = 'running'
isIpApiHitting = True
count = 0
key = 'DubeyIhIZqTUZ2y4mRlPTXUXv8t2'
proxy = "https://proxybot.io/api/v1/{0}?url=".format(key)
#https://proxybot.io/api/v1/DubeyIhIZqTUZ2y4mRlPTXUXv8t2?url=https://charanbir.com/covid19/
#https://www.scrapehero.com/detect-and-block-bots/

async def gotoOverRide(page, url):
    return await page.goto(url, {
        'waitUntil': 'networkidle2',
        'timeout': 120000
    })

class NewThread (threading.Thread):
    def __init__(self, url, ip, count):
      threading.Thread.__init__(self)
      self.url = url
      self.ip = ip
      self.count = count
      self.status = pending
      
    def run(self):
        self.status = running
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
                getIps()
        print('thread finished')
        
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
                'args': ['--proxy-server='+ip, '--no-sandbox', '--disable-infobars']
                })
        
    async def initPage(self, browser):
        page = await browser.newPage()
        await page.setUserAgent('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36')
        await page.setViewport({'width': 1200, 'height': 800})
        return page

    async def handelRequest(self):
        print('Thread started')
        browser = await self.browser(self.ip)
        page = await self.initPage(browser)
        try:
#            pageUrl = proxy + self.url
            await gotoOverRide(page, self.url)
            if ('https://charanbir.com/covid19/' in self.url):
                await page.waitForSelector('#heading')
                element = await page.querySelectorAll('#heading')
                if (len(element) > 0):
                    text = await page.evaluate('(element) => element.textContent', element[0])
                    if (str(text[0:3]) != 'For'):
                        await page.waitForXPath('//table')
            else:
                await page.waitForXPath('//div[@class="header"]')
        except : #AssertionError as error:
            print("timeout error after 120 sec")
        await browser.close()




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
        
arrUrls = [ "https://charanbir.com/","https://charanbir.com/portfolio","https://charanbir.com/blog","https://charanbir.com/blog/2","https://charanbir.com/contact","https://charanbir.com/covid19/","https://charanbir.com/covid19/USA/","https://charanbir.com/covid19/Russia/","https://charanbir.com/covid19/Spain/","https://charanbir.com/covid19/Brazil/","https://charanbir.com/covid19/UK/","https://charanbir.com/covid19/Italy/","https://charanbir.com/covid19/France/","https://charanbir.com/covid19/Germany/","https://charanbir.com/covid19/Turkey/","https://charanbir.com/covid19/Iran/","https://charanbir.com/covid19/India/","https://charanbir.com/covid19/Peru/","https://charanbir.com/covid19/China/","https://charanbir.com/covid19/Canada/","https://charanbir.com/covid19/Saudi Arabia/","https://charanbir.com/covid19/Belgium/","https://charanbir.com/covid19/Mexico/","https://charanbir.com/covid19/Chile/","https://charanbir.com/covid19/Pakistan/","https://charanbir.com/covid19/Netherlands/","https://charanbir.com/covid19/Qatar/","https://charanbir.com/covid19/Ecuador/","https://charanbir.com/covid19/Belarus/","https://charanbir.com/covid19/Sweden/","https://charanbir.com/covid19/Switzerland/","https://charanbir.com/covid19/Portugal/","https://charanbir.com/covid19/Singapore/","https://charanbir.com/covid19/Bangladesh/","https://charanbir.com/covid19/UAE/","https://charanbir.com/covid19/Ireland/","https://charanbir.com/covid19/Poland/","https://charanbir.com/covid19/Ukraine/","https://charanbir.com/covid19/Indonesia/","https://charanbir.com/covid19/Kuwait/","https://charanbir.com/covid19/Romania/","https://charanbir.com/covid19/South Africa/","https://charanbir.com/covid19/Colombia/","https://charanbir.com/covid19/Israel/","https://charanbir.com/covid19/Japan/","https://charanbir.com/covid19/Austria/","https://charanbir.com/covid19/Egypt/","https://charanbir.com/covid19/Dominican Republic/","https://charanbir.com/covid19/Philippines/","https://charanbir.com/covid19/Denmark/","https://charanbir.com/covid19/S. Korea/","https://charanbir.com/covid19/Serbia/","https://charanbir.com/covid19/Panama/","https://charanbir.com/covid19/Argentina/","https://charanbir.com/covid19/Czechia/","https://charanbir.com/covid19/Norway/","https://charanbir.com/covid19/Afghanistan/","https://charanbir.com/covid19/Bahrain/","https://charanbir.com/covid19/Algeria/","https://charanbir.com/covid19/Australia/","https://charanbir.com/covid19/Morocco/","https://charanbir.com/covid19/Malaysia/","https://charanbir.com/covid19/Kazakhstan/","https://charanbir.com/covid19/Nigeria/","https://charanbir.com/covid19/Finland/","https://charanbir.com/covid19/Moldova/","https://charanbir.com/covid19/Ghana/","https://charanbir.com/covid19/Oman/","https://charanbir.com/covid19/Armenia/","https://charanbir.com/covid19/Bolivia/","https://charanbir.com/covid19/Luxembourg/","https://charanbir.com/covid19/Iraq/","https://charanbir.com/covid19/Hungary/","https://charanbir.com/covid19/Cameroon/","https://charanbir.com/covid19/Azerbaijan/","https://charanbir.com/covid19/Thailand/","https://charanbir.com/covid19/Honduras/","https://charanbir.com/covid19/Uzbekistan/","https://charanbir.com/covid19/Guinea/","https://charanbir.com/covid19/Greece/","https://charanbir.com/covid19/Sudan/","https://charanbir.com/covid19/Senegal/","https://charanbir.com/covid19/Bosnia/","https://charanbir.com/covid19/Bulgaria/","https://charanbir.com/covid19/Croatia/","https://charanbir.com/covid19/Côte d'Ivoire/","https://charanbir.com/covid19/Guatemala/","https://charanbir.com/covid19/Tajikistan/","https://charanbir.com/covid19/Cuba/","https://charanbir.com/covid19/Macedonia/","https://charanbir.com/covid19/Iceland/","https://charanbir.com/covid19/Estonia/","https://charanbir.com/covid19/DRC/","https://charanbir.com/covid19/Djibouti/","https://charanbir.com/covid19/Lithuania/","https://charanbir.com/covid19/El Salvador/","https://charanbir.com/covid19/New Zealand/","https://charanbir.com/covid19/Gabon/","https://charanbir.com/covid19/Somalia/","https://charanbir.com/covid19/Slovakia/","https://charanbir.com/covid19/Slovenia/","https://charanbir.com/covid19/Mayotte/","https://charanbir.com/covid19/Kyrgyzstan/","https://charanbir.com/covid19/Maldives/","https://charanbir.com/covid19/Hong Kong/","https://charanbir.com/covid19/Tunisia/","https://charanbir.com/covid19/Guinea-Bissau/","https://charanbir.com/covid19/Sri Lanka/","https://charanbir.com/covid19/Latvia/","https://charanbir.com/covid19/Albania/","https://charanbir.com/covid19/Kenya/","https://charanbir.com/covid19/Lebanon/","https://charanbir.com/covid19/Cyprus/","https://charanbir.com/covid19/Niger/","https://charanbir.com/covid19/Mali/","https://charanbir.com/covid19/Costa Rica/","https://charanbir.com/covid19/Zambia/","https://charanbir.com/covid19/Paraguay/","https://charanbir.com/covid19/Equatorial Guinea/","https://charanbir.com/covid19/Burkina Faso/","https://charanbir.com/covid19/Andorra/","https://charanbir.com/covid19/Venezuela/","https://charanbir.com/covid19/Uruguay/","https://charanbir.com/covid19/Georgia/","https://charanbir.com/covid19/Diamond Princess/","https://charanbir.com/covid19/San Marino/","https://charanbir.com/covid19/Jordan/","https://charanbir.com/covid19/Haiti/","https://charanbir.com/covid19/Malta/","https://charanbir.com/covid19/Channel Islands/","https://charanbir.com/covid19/Chad/","https://charanbir.com/covid19/Sierra Leone/","https://charanbir.com/covid19/Jamaica/","https://charanbir.com/covid19/Tanzania/","https://charanbir.com/covid19/Réunion/","https://charanbir.com/covid19/Taiwan/","https://charanbir.com/covid19/Nepal/","https://charanbir.com/covid19/Congo/","https://charanbir.com/covid19/Palestine/","https://charanbir.com/covid19/Ethiopia/","https://charanbir.com/covid19/Madagascar/","https://charanbir.com/covid19/Central African Republic/","https://charanbir.com/covid19/Togo/","https://charanbir.com/covid19/Cabo Verde/","https://charanbir.com/covid19/Isle of Man/","https://charanbir.com/covid19/Mauritius/","https://charanbir.com/covid19/Montenegro/","https://charanbir.com/covid19/Vietnam/","https://charanbir.com/covid19/Rwanda/","https://charanbir.com/covid19/South Sudan/","https://charanbir.com/covid19/Uganda/","https://charanbir.com/covid19/Nicaragua/","https://charanbir.com/covid19/Sao Tome and Principe/","https://charanbir.com/covid19/Liberia/","https://charanbir.com/covid19/French Guiana/","https://charanbir.com/covid19/Swaziland/","https://charanbir.com/covid19/Myanmar/","https://charanbir.com/covid19/Martinique/","https://charanbir.com/covid19/Faroe Islands/","https://charanbir.com/covid19/Yemen/","https://charanbir.com/covid19/Guadeloupe/","https://charanbir.com/covid19/Gibraltar/","https://charanbir.com/covid19/Mozambique/","https://charanbir.com/covid19/Brunei/","https://charanbir.com/covid19/Mongolia/","https://charanbir.com/covid19/Mauritania/","https://charanbir.com/covid19/Benin/","https://charanbir.com/covid19/Bermuda/","https://charanbir.com/covid19/Guyana/","https://charanbir.com/covid19/Cambodia/","https://charanbir.com/covid19/Trinidad and Tobago/","https://charanbir.com/covid19/Cayman Islands/","https://charanbir.com/covid19/Aruba/","https://charanbir.com/covid19/Monaco/","https://charanbir.com/covid19/Bahamas/","https://charanbir.com/covid19/Barbados/","https://charanbir.com/covid19/Liechtenstein/","https://charanbir.com/covid19/Sint Maarten/","https://charanbir.com/covid19/Malawi/","https://charanbir.com/covid19/Libyan Arab Jamahiriya/","https://charanbir.com/covid19/French Polynesia/","https://charanbir.com/covid19/Syrian Arab Republic/","https://charanbir.com/covid19/Angola/","https://charanbir.com/covid19/Zimbabwe/","https://charanbir.com/covid19/Macao/","https://charanbir.com/covid19/Burundi/","https://charanbir.com/covid19/Eritrea/","https://charanbir.com/covid19/Saint Martin/","https://charanbir.com/covid19/Comoros/","https://charanbir.com/covid19/Antigua and Barbuda/","https://charanbir.com/covid19/Botswana/","https://charanbir.com/covid19/Gambia/","https://charanbir.com/covid19/Timor-Leste/","https://charanbir.com/covid19/Grenada/","https://charanbir.com/covid19/Bhutan/","https://charanbir.com/covid19/Lao People's Democratic Republic/","https://charanbir.com/covid19/Belize/","https://charanbir.com/covid19/Fiji/","https://charanbir.com/covid19/New Caledonia/","https://charanbir.com/covid19/Saint Lucia/","https://charanbir.com/covid19/Saint Vincent and the Grenadines/","https://charanbir.com/covid19/Curaçao/","https://charanbir.com/covid19/Dominica/","https://charanbir.com/covid19/Namibia/","https://charanbir.com/covid19/Saint Kitts and Nevis/","https://charanbir.com/covid19/Falkland Islands (Malvinas)/","https://charanbir.com/covid19/Holy See (Vatican City State)/","https://charanbir.com/covid19/Turks and Caicos Islands/","https://charanbir.com/covid19/Greenland/","https://charanbir.com/covid19/Montserrat/","https://charanbir.com/covid19/Seychelles/","https://charanbir.com/covid19/Suriname/","https://charanbir.com/covid19/MS Zaandam/","https://charanbir.com/covid19/British Virgin Islands/","https://charanbir.com/covid19/Papua New Guinea/","https://charanbir.com/covid19/Caribbean Netherlands/","https://charanbir.com/covid19/St. Barth/","https://charanbir.com/covid19/Western Sahara/","https://charanbir.com/covid19/Anguilla/","https://charanbir.com/covid19/Lesotho/","https://charanbir.com/covid19/Saint Pierre Miquelon/","https://charanbir.com/covid19/India/Maharashtra/","https://charanbir.com/covid19/India/Tamil Nadu/","https://charanbir.com/covid19/India/Gujarat/","https://charanbir.com/covid19/India/Delhi/","https://charanbir.com/covid19/India/Rajasthan/","https://charanbir.com/covid19/India/Madhya Pradesh/","https://charanbir.com/covid19/India/Uttar Pradesh/","https://charanbir.com/covid19/India/West Bengal/","https://charanbir.com/covid19/India/Andhra Pradesh/","https://charanbir.com/covid19/India/Punjab/","https://charanbir.com/covid19/India/Telangana/","https://charanbir.com/covid19/India/Bihar/","https://charanbir.com/covid19/India/Karnataka/","https://charanbir.com/covid19/India/Jammu and Kashmir/","https://charanbir.com/covid19/India/State Unassigned/","https://charanbir.com/covid19/India/Odisha/","https://charanbir.com/covid19/India/Haryana/","https://charanbir.com/covid19/India/Kerala/","https://charanbir.com/covid19/India/Jharkhand/","https://charanbir.com/covid19/India/Chandigarh/","https://charanbir.com/covid19/India/Tripura/","https://charanbir.com/covid19/India/Assam/","https://charanbir.com/covid19/India/Uttarakhand/","https://charanbir.com/covid19/India/Chhattisgarh/","https://charanbir.com/covid19/India/Himachal Pradesh/","https://charanbir.com/covid19/India/Goa/","https://charanbir.com/covid19/India/Ladakh/","https://charanbir.com/covid19/India/Andaman and Nicobar Islands/","https://charanbir.com/covid19/India/Puducherry/","https://charanbir.com/covid19/India/Meghalaya/","https://charanbir.com/covid19/India/Manipur/","https://charanbir.com/covid19/India/Mizoram/","https://charanbir.com/covid19/India/Arunachal Pradesh/","https://charanbir.com/covid19/India/Dadra and Nagar Haveli and Daman and Diu/","https://charanbir.com/covid19/India/Nagaland/","https://charanbir.com/covid19/India/Lakshadweep/","https://charanbir.com/covid19/India/Sikkim/" ]
   
def getIps():
    global isIpApiHitting
    isIpApiHitting = True
    print('requisting for new ips')
    ips = asyncio.run(GetIPProxies().getIp())
    for ip in ips:
        global count
        count += 1
        index = random.randint(0,(len(arrUrls)-1))
        url = arrUrls[index]
        thread = NewThread(url, ip, count)
        arrThreads.append(thread)

    for i in range(0,concrentNumberOfThreads):
        if (i < len(arrThreads)):
            if (arrThreads[i].status == pending):
                arrThreads[i].start()
                print(arrThreads[i].count)
    print("{0} new Ip address added".format(len(ips)))
    isIpApiHitting = False

getIps()

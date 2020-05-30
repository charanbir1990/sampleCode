import asyncio
from pyppeteer import launch
import threading
import time

class NewThread (threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
      print('mop')
      
    def run(self):
        print('hit')
        asyncio.run(self.handelRequest())

    async def handelRequest(self):
        browser = await launch({'headless': False,
        'ignoreHTTPSErrors': True,
        'handleSIGINT': False,
        'handleSIGTERM': False,
        'handleSIGHUP': False,
        'args': [
#        '--proxy-server=' + "86.123.166.109:8080",
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--disable-gpu',
        '--window-size=1440x900',
        '--disable-infobars',
        '--lang=en',
        ]
        })
        page = await browser.newPage()
        await page.setViewport({'width': 1200, 'height': 800})
        await page.goto('https://www.linkedin.com/', {
            'waitUntil': 'networkidle2',
            'timeout': 60*1000
        })
    #    await page.goto("https://charanbir.com/")
        await page.waitForSelector('.intent-module')
        await page.waitFor(1000)
        await page.goto("https://google.com/")
        await page.waitForXPath("//input[@title='Search']")
        await page.click('ul[class=intent-module__list] li:nth-child(2)')
        await page.waitForXPath("//main[@class='empty-pserp-page']")
        await page.screenshot({'path': 'linkedin.png'})
        await browser.close()



thread = NewThread()
thread.start()
#asyncio.get_event_loop().run_until_complete(handelRequest())


const puppeteer = require('puppeteer')
var random_useragent = require('random-useragent')
const fs = require('fs')
const expect = require('chai').expect
const { click } = require('../helper')
//https://devdocs.io/puppeteer/
//puppeteer timeout is 40 sec default

describe('My First Puppeteer Test', () => {
         before(async function(){
                
                })
         after(async function(){
         
         })
         beforeEach(async function(){
         
         })
         afterEach(async function(){
         
         })
         it('should launch the browser', async function() {
            const browser = await puppeteer.launch({
                                                   headless: false,
                                                   slowMo: 10,
                                                   devtools: false
                                                   })
            const context = await browser.createIncognitoBrowserContext()
            const page = await browser.newPage()
            await page.setUserAgent(random_useragent.getRandom())
            const pageIncognitee = await browser.context()
            await page.setViewport({width: 1650, height: 1050})
            // for tablet
            const tablet = puppeteer.devices['ipad landscape']
            await page.emulater(tablet)
            //for tablet end
            
            // for mobile
            const phone = puppeteer.devices['iphone X']
            await page.emulater(phone)
            //for mobile end
            await page.setDefaultTimeout(9000)
            await page.setDefaultNavigationTimeout(7000)
            await page.goto('http://example.com')
            await page.waitFor(3000)
            await page.waitForSelector('h1') // simple element name
            await page.type('#someId', 'value', {delay: 0}) // deling with id
            await page.type('.someClass', 'value', {delay: 0}) // dealing with class
            await page.waitForXPath('//h1') // dealing with xpath
            await page.waitForXPath("//td[@colspan='1'][1]/font[@class='spy14']")
            let elements = await page.$x("//td[@colspan='1'][1]/font[@class='spy14']")
            await page.click('input[type="submit"]')
            await page.click('#someId', {clickCount: 3})
            const title = await page.title() // get page title
            await page.url() // get page url
            await page.$eval('h1', element => element.innerHTML) // get html from element
            await page.$eval('h1', element => element.textContent) // get text from element
            await page.$$eval('h1', element => element.length) // get h1 count
            await page.keyboard.press('Enter', {delay: 1}) // press enter from keyboard
            await page.select('#someId', 'select index value')
            await page.reload()
            await page.goto('http://example.com')
            await page.goBack()
            await page.goForward()
            await page.waitForSelector('button', {hidden: true, timeout: 3000})
            await page.waitFor(() => !document.querySelector('#someId'))
            expect(title).to.be.a('string', 'this is title')
            expect(title).to.include('this is title')
            
            //save data to file
            const logger  = fs.createWriteStream('log.txt', {flags: 'a'})
            logger.write("some text")
            logger.close()
            await browser.close()
            await page.screenshot({path: 'example.png'})

            })
         })





    await page.waitForXPath("//td[@colspan='1'][1]/font[@class='spy14']")
    let elements = await page.$x("//td[@colspan='1'][1]/font[@class='spy14']")
//    const srcHandlesArray = await Promise.all(elements.map(handle => handle.getProperty('innerHTML')))
//    const srcValuesArray = await Promise.all(srcHandlesArray.map(handle => handle.jsonValue()))
//    console.log(srcValuesArray)
//text = await page.evaluate(element => element.textContent, element)
//var xpathTextContent = await element.getProperty('textContent'), text = await xpathTextContent.jsonValue();
//let text = await element.getProperty('textContent')

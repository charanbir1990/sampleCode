const puppeteer = require('puppeteer')
const expect = require('chai').expect
const { getText } = require('../lib/helpers')

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
            const browser = await puppeteer.launch({headless: false})
            const page = await browser.newPage()
            await page.setDefaultTimeout(9000)
            await page.setDefaultNavigationTimeout(5000)
            await page.goto('https://charanbir.com/covid19')
            const text = await getText(page, 'buttonld')
            console.log(text)
            await browser.close()
            })
         })

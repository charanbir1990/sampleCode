

const fs = require('fs')
const puppeteer = require('puppeteer')
var MongoClient = require('mongodb').MongoClient
var url = "mongodb://localhost:27017/"

async function get_ip(){
    console.log('requesting ip')
    arrIp = []
    const browser = await puppeteer.launch({ headless: true })
    const page = await browser.newPage()
    await page.setViewport({width: 1440, height: 900})
    await page.goto("http://spys.one/en/https-ssl-proxy/")
    let xpath = "//td[@colspan='1'][1]/font[@class='spy14']"
    await page.waitForXPath(xpath)
    let elements = await page.$x(xpath)
    for (element of elements) {
        let text = await element.getProperty('innerHTML');
        var json = await text.jsonValue()
        var ip = json.split("<")[0]
        var arr = json.split(">")
        var port = arr[arr.length-1]
        arrIp.push(ip + ":" + port)
    }
    await browser.close()
    console.log('got ip: %d',arrIp.length)
    return await arrIp
}

async function click(page, xpath) {
    await page.waitForXPath(xpath)
    const btnArr = await page.$x(xpath)
    if (btnArr.length > 0) {
      await btnArr[0].click()
    }
}

arrNames = []
arrOpreations = []





class Opration {
    constructor(name, ip, count){
        this.name = name
        this.ip = ip
        this.count = count
    }
    
    async startOpration() {
        await this.runOnlyNames()
    }
    
    saveDataToDb(urlToSave) {
        MongoClient.connect(url, { useNewUrlParser: true, useUnifiedTopology: true }, function(err, db) {
        if (err == null) {
        var dbo = db.db("LinkedIn")
        const coll = 'UserWithStatus'
//        const coll = 'User'
        dbo.collection(coll).findOne({'link': urlToSave}, function(err, result) {
                                       if (err == null && result == null) {
                                       var myobj = { link: urlToSave, status: 'pending' }
                                       dbo.collection(coll).insertOne(myobj, function(err, res) {
                                                                        if (err == null) {
                                                                        console.log("saved: " + urlToSave)
                                                                      }else{
                                                                      console.log('error in save row')
                                                                      }
                                                                        db.close()
                                                                        })
                                       }else {
                                     console.log('already exsist')
                                       db.close()
                                       }
                                       })
                            }else{
                            console.log('error to link db')
                            }
        })
    }
    
    async runOnlyNames() {
        console.log('started: %d', this.count)
        try{
            this.browser = await puppeteer.launch({
                                                   headless: false,
                                                  ignoreDefaultArgs: ['--enable-automation'],
                                                   args: [
//                                                          '--proxy-server=' + this.ip,
                                                          '--no-sandbox',
                                                          '--disable-setuid-sandbox',
                                                          '--disable-infobars',
                                                          ]
                                                   })
            const page = await this.browser.newPage()
            await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15')
            await page.setViewport({'width': 1440, 'height': 900})
            await page.setDefaultTimeout(90000)
            await page.setDefaultNavigationTimeout(90000)
            await page.goto('https://www.linkedin.com/')
            await page.waitForSelector('.intent-module')
            await page.waitFor(1000)
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            await page.click('ul[class=intent-module__list] li:nth-child(2)')
            await page.waitForXPath("//main[@class='empty-pserp-page']")
            await page.waitFor(1000)
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            const nameA = arrNames
            console.log(nameA.length)
            for (const name of nameA) {
                this.name = name
                await page.click('body > div > header > nav > section.search-bar > section:nth-child(3) > form > section:nth-child(1) > input', { clickCount: 3 })
                await page.type('body > div > header > nav > section.search-bar > section:nth-child(3) > form > section:nth-child(1) > input', this.name)
                await page.waitFor(1000)
                await page.screenshot({'path': 'ScreenShots/linkedin.png'})
                await page.click('.sign-in-card__dismiss-btn')
                await page.waitFor(1000)
                await page.screenshot({'path': 'ScreenShots/linkedin.png'})
                await page.click('body > div > header > nav > section.search-bar > section:nth-child(3) > form > button')
                await page.waitForSelector('#main-content')
                await page.screenshot({'path': 'ScreenShots/linkedin.png'})
                const profileLinks = await page.$x("//section//ul/li/a")
                for (const element of profileLinks) {
                    const textRaw = await element.getProperty('href')
                    const text = await textRaw.jsonValue()
                    const link = text.split('?')[0]
                    this.saveDataToDb(link)
                }
                if (arrNames.includes(this.name)) {
                    const index = arrNames.indexOf(this.name)
                    arrNames.splice(index,1)
                    var names = ''
                    for (const element of arrNames) {
                        names += (element+"\n")
                    }
                    fs.writeFile('names.txt', names, function (err) {})
                }
            }
            await this.browser.close()
            console.log('finished')
        }catch{
            try{
                console.log('error')
                await this.browser.close()
            }catch{}
        }
    }
    
    async run() {
        console.log('started: %d', this.count)
        try{
            this.browser = await puppeteer.launch({
                                                   headless: true,
                                                  ignoreDefaultArgs: ['--enable-automation'],
                                                   args: [
                                                          '--proxy-server=' + this.ip,
                                                          '--no-sandbox',
                                                          '--disable-setuid-sandbox',
                                                          '--disable-infobars',
                                                          ]
                                                   })
            const page = await this.browser.newPage()
            await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15')
            await page.setViewport({'width': 1440, 'height': 900})
            await page.setDefaultTimeout(90000)
            await page.setDefaultNavigationTimeout(90000)
            await page.goto('https://www.linkedin.com/')
            await page.waitForSelector('.intent-module')
            await page.waitFor(1000)
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            await page.click('ul[class=intent-module__list] li:nth-child(2)')
            await page.waitForXPath("//main[@class='empty-pserp-page']")
            await page.waitFor(1000)
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            await page.type('body > div > header > nav > section.search-bar > section:nth-child(3) > form > section:nth-child(1) > input', this.name)
            await page.waitFor(1000)
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            await page.click('.sign-in-card__dismiss-btn')
            await page.waitFor(1000)
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            await page.click('body > div > header > nav > section.search-bar > section:nth-child(3) > form > button')
            await page.waitForSelector('#main-content')
            await page.screenshot({'path': 'ScreenShots/linkedin.png'})
            const profileLinks = await page.$x("//section//ul/li/a")
            console.log(profileLinks.length)
            for (const element of profileLinks) {
                const textRaw = await element.getProperty('href')
                const text = await textRaw.jsonValue()
                const link = text.split('?')[0]
                this.saveDataToDb(link)
            }
            if (arrNames.includes(this.name)) {
                const index = arrNames.indexOf(this.name)
                arrNames.splice(index,1)
                names = ''
                for (element of arrNames) {
                    names += (element+"\n")
                }
                fs.writeFile('names.txt', names, function (err) {})
            }
            await rhis.browser.close()
            console.log('finished')
        }catch{
            try{
                console.log('error')
                await this.browser.close()
            }catch{}
        }

    }
}

function getName(){
    index = Math.floor(Math.random() * arrNames.length)
    return arrNames[index]
}

function isNameExistAlready(name){
    isExist = false
    for (element of arrOpreations) {
        if (name == element.name) {
            isExist = true
            break
        }
    }
    return isExist
}

function getNextName() {
    name = getName()
    while (isNameExistAlready(name)){ name = getName() }
    return name
}

async function run() {
    
    arrNames = fs.readFileSync('names.txt', 'utf8').split('\n')
    arrNames = arrNames.filter(function (el) { return el != '' })
    const task = new Opration('', '', 1)
    await task.startOpration()
    return
    arrIp = await get_ip()
    count = 0
    for (ip of arrIp) {
        count += 1
        name = getNextName()
        task = new Opration(name, ip, count)
        arrOpreations.push(task)
        await task.startOpration()
    }
}
run()




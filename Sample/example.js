const puppeteer = require('puppeteer')


let browser
async function getChrome(proxy) {
    let headless = true
    
    if (proxy == '') {
        browser = await puppeteer.launch({
                                         headless: headless
                                         })
    } else {
        browser = await puppeteer.launch({
                                         headless: headless,
                                         args: [ '--proxy-server=' + proxy ]
                                         })
    }
    const page = await browser.newPage()
    await page.setViewport({width: 1200, height: 800})
    await page.setDefaultTimeout(90000)
    await page.setDefaultNavigationTimeout(90000)
    return page
}

async function get_ip(){
    arrIp = []
    const page = await getChrome('')
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
    return await arrIp
}


async function run() {
    const arrIp = await get_ip()
    for (ip of arrIp) {
        console.log(ip)
        try{
            const page = await getChrome(ip)
            await page.goto('https://charanbir.com/covid19')
            await page.waitForSelector('button')
            await page.waitFor(5000)
            await browser.close()
        }catch(error) {
            await browser.close()
            console.log(error)
        }
    }
}
run()
//dimensions = await page.evaluate('''() => {
//    return {
//        width: document.documentElement.clientWidth,
//        height: document.documentElement.clientHeight,
//        deviceScaleFactor: window.devicePixelRatio,
//    }
//}''')


//var linkTexts = await page.$$eval(".plan-features a", elements=> elements.map(item=>item.textContent))
//            await page.$eval('input[name=username]', el => el.value = 'charanbir1990@yahoo.com')
//            await page.$eval('input[name=password]', el => el.value = 'manisha@123')
//instaXpath = "//a[text()='Forgot password?']"
//const linkHandlers = await page.$x(instaXpath)
//if (linkHandlers.length > 0) {
//  await linkHandlers[0].click();
//}

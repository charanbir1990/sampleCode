const { Cluster } = require('puppeteer-cluster')
const maxConcurrent = 10
const headless = true

async function run() {
 let proxy = "202.147.207.253:38646"
 let browserArgs = [
                    '--disable-infobars',
                    '--window-position=0,0',
                    '--ignore-certifcate-errors',
                    '--ignore-certifcate-errors-spki-list',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--disable-gpu',
                    '--window-size=1920x1080',
                    '--hide-scrollbars',
                    ];
 
 // each new call to workerInstance() will
 // left pop() one element from this list
 // maxConcurrency should be equal to perBrowserOptions.length
 var perBrowserOptions = []
 for (var i = 0; i < maxConcurrent; i++) {
 perBrowserOptions.push(
                        {
                        headless: headless,
                        ignoreHTTPSErrors: true,
                        args: browserArgs.concat(['--proxy-server='+proxy])
                        }
                        )
 }
 
 const cluster = await Cluster.launch({
                                      monitor: false,
                                      concurrency: Cluster.CONCURRENCY_BROWSER,
                                      maxConcurrency: maxConcurrent,
                                      puppeteerOptions: {
                                      headless: true,
                                      args: browserArgs,
                                      ignoreHTTPSErrors: true,
                                      },
                                      perBrowserOptions: perBrowserOptions
                                      })
 
 // Event handler to be called in case of problems
 cluster.on('taskerror', (err, data) => {
            console.log(`Error crawling ${data}: ${err.message}`)
            })
 
 
 await cluster.task(async ({ page, data: url }) => {
                    await page.goto(url, {waitUntil: 'networkidle2', timeout: 90000})
                    const pageTitle = await page.evaluate(() => document.title)
                    console.log(`Page title of ${url} is ${pageTitle}`)
                    console.log(await page.content())
                    })
 for (var i = 0; i <= maxConcurrent; i++){
     await cluster.queue('http://ipinfo.io/json')
 }
 // many more pages
 
 await cluster.idle()
 await cluster.close()

 }

async function wait(){
    await run()
    console.log('print1')
    await run()
    console.log('print2')
}


wait()

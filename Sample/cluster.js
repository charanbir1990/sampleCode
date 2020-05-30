const { Cluster } = require('puppeteer-cluster');
//const maxParlelQueues = 4


(async () => {
  const cluster = await Cluster.launch({
    concurrency: Cluster.CONCURRENCY_CONTEXT,
    maxConcurrency: 5,
  })
count = 0
  await cluster.task(async ({ page, data: url }) => {
    await page.goto(url)
                     console.log('cluster')
                     count += 1
                     path = ("ScreenShots/" + String(count) + ".png")
                     console.log(path)
                     await page.screenshot({'path': path})
  });

    cluster.queue('http://www.google.com/')
    cluster.queue('http://www.wikipedia.org/')
    cluster.queue('http://www.linkedin.com/')
    cluster.queue('http://www.charanbir.com/')
 cluster.queue('https://api.ipify.org/?format=text')
  // many more pages

  await cluster.idle();
  await cluster.close();
})();

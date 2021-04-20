const { chromium } = require('playwright');
const { saveVideo } = require('playwright-video');

(async () => {
  var start = new Date();
  const browser = await chromium.launch();
  const context = await browser.newContext();
	var now = new Date();
	console.log('launched', now.getTime() - start.getTime());
  const page = await context.newPage();
  await page.setViewportSize({
    width: 1920,
    height: 1080,
  });

  await saveVideo(page, 'video.mp4');

	now = new Date();
	console.log('starting clicking', now.getTime() - start.getTime());
  await page.goto('https://usegalaxy.org');
  await page.waitForLoadState('networkidle');
	now = new Date();
	console.log('net idle', now.getTime() - start.getTime());
  //await page.waitForTimeout(5000);
  //await page.click('#tool-panel-upload-button');
  await page.waitForTimeout(5000);
  now = new Date();
  console.log('5s later, going to bwa-mem', now.getTime() - start.getTime());
  await page.goto('https://usegalaxy.org/?tool_id=bwa_mem');
	now = new Date();
	console.log('gone', now.getTime() - start.getTime());
  await page.waitForTimeout(3000);
	now = new Date();
	console.log('wait 3s', now.getTime() - start.getTime());
  //await page.mouse.move(0, 0);
  //await page.waitForTimeout(250);
  //await page.mouse.move(200, 200);
  //await page.waitForTimeout(250);
  //await page.mouse.move(400, 400);
  //await page.waitForTimeout(250);
	now = new Date();
	console.log('going to click', now.getTime() - start.getTime());
  await page.click('#s2id_field-uid-11_select');
	now = new Date();
	console.log('clicked', now.getTime() - start.getTime());
  await page.waitForTimeout(3000);
	now = new Date();
	console.log('wait 3s', now.getTime() - start.getTime());

  await browser.close();
})();

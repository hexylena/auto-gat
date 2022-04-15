const { chromium } = require('playwright-chromium');
const { saveVideo } = require('playwright-video');
const fs = require('fs');
var actions;
var syncReport = [];
fs.readFile(process.argv[2], 'utf8', (err, data) => {
	actions = JSON.parse(data);
});
var video_output_name = process.argv[3];
var videoSpeed = 1000;
if(process.argv.length > 4){
	videoSpeed = 10;
}


function logtime(now, start, msg){
	var timestamp = now.getTime() - start.getTime();
	syncReport.push({
		'time': timestamp,
		'msg': msg,
	})
	//console.log(timestamp/1000, msg);
}

(async () => {
	var start = new Date();
	// this seems to be ignored? no way to set zoom?
	const browser = await chromium.launch();
	const context = await browser.newContext({ignoreHTTPSErrors: true});
	const page = await context.newPage();
	await page.setViewportSize({
		width: 1920,
		height: 1080,
	});
	await saveVideo(page, video_output_name);

	for(var i = 0; i < actions.length; i++){
		var step = actions[i];
		//console.log(step);
		if(step.action == 'goto'){
			await page.goto(step.target);
			await page.evaluate(() => {
				document.body.style.zoom=1.4;
			});
			await page.waitForLoadState('networkidle');
			if(step.value !== undefined){
				//console.log('text=' + step.value)
				await page.locator(step.value).first().waitFor();
			}
			now = new Date();
			logtime(now, start, 'gone')
		} else if (step.action == 'scrollTo'){
			await page.evaluate((step) => document.getElementById(step.target.slice(1)).scrollIntoView({behavior: "smooth"}), step).catch((err) => console.log(err));
			now = new Date();
			logtime(now, start, 'scrolled')
		} else if (step.action == 'fill'){
			//await page.fill(step.target, step.value)

		  await page.locator(step.target).first().fill(step.value);

			now = new Date();
			logtime(now, start, 'filled')
		} else if (step.action == 'click'){
			//await page.locator(step.target).first().click();
			//await page.click(step.target)
			await page.evaluate((step) => {
				document.querySelector(step.target).click();
			}, step);

			await page.evaluate(() => {
				document.body.style.zoom=1.4;
			});
			now = new Date();
			logtime(now, start, 'clicked')
		} else if (step.action == 'loadTool'){
			await page.evaluate((step) => {
				Galaxy.router.push("/", { tool_id: step.target });
			}, step);
			await page.evaluate(() => {
				document.body.style.zoom=1.4;
			});

			if(step.value !== undefined){
				await page.locator(step.value).waitFor();
			}

			now = new Date();
			logtime(now, start, 'loadTool')
		} else if (step.action == 'custom'){
			await page.evaluate((step) => {
				eval(step.target)
			}, step);
			await page.evaluate(() => {
				document.body.style.zoom=1.4;
			});

			now = new Date();
			logtime(now, start, 'custom')
		} else if (step.action == 'waitForDataset'){
			var e = document.evaluate(`//span[text()='${step.target}']`, document, null, XPathResult.ANY_TYPE, null).iterateNext().parentElement.parentElement.parentElement.id;
			await this.page.waitForSelector(`#${e.id}.state-ok`);
			now = new Date();
			logtime(now, start, 'datasetState')
		} else {
			console.log("Unknown step type!", step)
		}

		if(step.sleep){
			await page.waitForTimeout(step.sleep * videoSpeed);
		}
	}
	// Sleep an extra 1.5s at the end.
	await page.waitForTimeout(1500);
	await browser.close();
	process.stdout.write(JSON.stringify(syncReport));
})();

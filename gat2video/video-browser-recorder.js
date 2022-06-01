const { chromium } = require('playwright-chromium');
const { program } = require('commander');

const fs = require('fs');
var actions;
var syncReport = [];

program
  .name('video-browser-recorder')
  .description('Given a GTN JSON Script, trigger specific browser recording actions with a simplified syntax')
  .version('0.0.0');

program
  .argument('<jsonpath>', 'Path to the JSON script')
  .option('--fast')
  .option('--log <output-log-path>')
  .option('--cookiejar <cookie-jar-path>')
  .option('--sessionstate <session-state-path>')
  .option('--mp4 <output-mp4-path>');

program.parse(process.argv);
const options = program.opts();

fs.readFile(program.args[0], 'utf8', (err, data) => {
	actions = JSON.parse(data);
});

function easeInOut(x) {
	return x < 0.5 ? 16 * x * x * x * x * x : 1 - Math.pow(-2 * x + 2, 5) / 2;
}

async function tweenMouse(page, origPos, newTarget){
	let [x2, y2] = newTarget,
		y0 = origPos[1],
		x0 = origPos[0];

	const totalTimeMs = 800;
	const tweenSteps = 50;
	for(var i = 0; i < tweenSteps; i++){
		let x1 = parseInt(x0 + (x2 - x0) * easeInOut(i / tweenSteps)),
			y1 = parseInt(y0 + (y2 - y0) * easeInOut(i / tweenSteps));
		await page.mouse.move(x1, y1);
		await page.waitForTimeout(totalTimeMs / tweenSteps);
	}
}


// https://github.com/hdorgeval/playwright-fluent/blob/master/src/actions/dom-actions/show-mouse-position/show-mouse-position.ts
//
async function showMousePosition(page) {
  if (!page) {
    throw new Error('Cannot show mouse position because no browser has been launched');
  }
  // code from https://gist.github.com/aslushnikov/94108a4094532c7752135c42e12a00eb
  await page.addInitScript(() => {
    // Install mouse helper only for top-level frame.
    if (window !== window.parent) return;
    window.addEventListener(
      'DOMContentLoaded',
      () => {
        const box = document.createElement('playwright-mouse-pointer');
        const styleElement = document.createElement('style');
        styleElement.innerHTML = `
        playwright-mouse-pointer {
          pointer-events: none;
          position: absolute;
          top: 0;
          z-index: 10000;
          left: 0;
          width: 20px;
          height: 20px;
          background: rgba(0,0,0,.4);
          border: 1px solid white;
          border-radius: 10px;
          margin: -10px 0 0 -10px;
          padding: 0;
          transition: background .2s, border-radius .2s, border-color .2s;
        }
        playwright-mouse-pointer.button-1 {
          transition: none;
          background: rgba(0,0,0,0.9);
        }
        playwright-mouse-pointer.button-2 {
          transition: none;
          border-color: rgba(0,0,255,0.9);
        }
        playwright-mouse-pointer.button-3 {
          transition: none;
          border-radius: 4px;
        }
        playwright-mouse-pointer.button-4 {
          transition: none;
          border-color: rgba(255,0,0,0.9);
        }
        playwright-mouse-pointer.button-5 {
          transition: none;
          border-color: rgba(0,255,0,0.9);
        }
      `;
        document.head.appendChild(styleElement);
        document.body.appendChild(box);
        document.addEventListener(
          'mousemove',
          (event) => {
            box.style.left = event.pageX + 'px';
            box.style.top = event.pageY + 'px';
          },
          true,
        );
        document.addEventListener(
          'mousedown',
          (event) => {
            box.classList.add('button-' + event.which);
          },
          true,
        );
        document.addEventListener(
          'mouseup',
          (event) => {
            box.classList.remove('button-' + event.which);
          },
          true,
        );
      },
      false,
    );
  });
}





var videoSpeed = 1000;
var lastMousePos;
if(options.fast){
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
	var contextOptions = {
		ignoreHTTPSErrors: true
	}
	if(options.mp4){
		contextOptions['recordVideo'] = {
			dir: '/tmp/',
			size: { width: 1920, height: 1080 },
		}
	}
	if(options.cookiejar){
		contextOptions['storageState'] = options.cookiejar
	}

	const context = await browser.newContext(contextOptions);


	if(options.cookiejar){
		const cookies = JSON.parse(fs.readFileSync(options.cookiejar).toString("utf-8"))
		await context.addCookies(cookies.cookies);
	}
	if(options.sessionstate){
		const sessionStorage = fs.readFileSync(options.sessionstate).toString("utf-8")
		context.addInitScript(storage => {
		  if (true) {
			const entries = JSON.parse(storage);
			for (const [key, value] of Object.entries(entries)) {
			  window.sessionStorage.setItem(key, value);
			}
		  }
		}, sessionStorage);
	}

	const page = await context.newPage();
	await page.setViewportSize({
		width: 1920,
		height: 1080,
	});

	// Setup the mouseHandler
	await showMousePosition(page);
	// Save that.
	lastMousePos = [
		400,
		400,
	];

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

			await page.evaluate(() => {
				lastMousePos = [
					document.documentElement.clientWidth / 2,
					document.documentElement.clientHeight / 2,
				];
			})
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
			var newMousePos = await page.evaluate((target) => {
				console.log(target)
				e2 = document.querySelector(target)
				p2 = e2.getBoundingClientRect()
				console.log(e2)
				y2 = p2.top + (p2.height / 2)
				x2 = p2.left + (p2.width / 2)
				return [x2, y2, target]
			}, step.target);
			console.log(lastMousePos, newMousePos)

			await tweenMouse(page, lastMousePos, newMousePos);
			lastMousePos = newMousePos;


			//await page.locator(step.target).first().click();
			//await page.click(step.target)
			//
			await page.evaluate(() => {
				document.getElementsByTagName("playwright-mouse-pointer")[0].classList.add('button-1');
			})
			await page.waitForTimeout(0.5 * videoSpeed);

			await page.evaluate((step) => {
				document.querySelector(step.target).click();
			}, step);

			await page.waitForLoadState('domcontentloaded');
			await page.mouse.move(...lastMousePos);
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
			// Sleep an extra couple seconds than requested, just to give the audio a bit more breathing room.
			await page.waitForTimeout((step.sleep + 2) * videoSpeed);
		}
	}
	// Sleep an extra 5s at the end.
	await page.waitForTimeout(5 * videoSpeed);
	await browser.close();

	if(options.log){
		fs.writeFile(options.log, JSON.stringify(syncReport), 'utf8', () => {})
	}

	// Make sure to await close, so that videos are saved.
	await context.close();

	if(options.mp4){
		const path = await page.video().path();
		//cnosole.log(path, options.mp4)
		fs.rename(path, options.mp4, () => {});
	}

})();

const { chromium } = require('playwright');
const path = require('path');
const V = __dirname;   // run from the repository: node docs/video/record.js (the demo must be running: python app.py)
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 720 }, recordVideo: { dir: V, size: { width: 1280, height: 720 } } });
  const p = await ctx.newPage();
  const t0 = Date.now(); const mark = (s) => console.log(((Date.now() - t0) / 1000).toFixed(1), s);
  const overlay = async () => p.evaluate(() => {
    if (document.getElementById('cap')) return;
    const c = document.createElement('div'); c.id = 'cap';
    c.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:99999;background:#0b0b0b;color:#fff;font:600 23px/1.35 Inter,Arial,sans-serif;padding:14px 34px;min-height:62px;display:flex;align-items:center';
    document.body.appendChild(c);
    const m = document.createElement('div'); m.id = 'mouse';
    m.style.cssText = 'position:fixed;z-index:100000;width:22px;height:22px;border-radius:50%;background:rgba(235,104,52,.75);border:2px solid #fff;pointer-events:none;left:-50px;top:-50px;transform:translate(-50%,-50%)';
    document.body.appendChild(m);
    document.addEventListener('mousemove', e => { m.style.left = e.clientX + 'px'; m.style.top = e.clientY + 'px'; });
  });
  const cap = async (text) => { await overlay(); await p.evaluate(t => { document.getElementById('cap').innerHTML = t; }, text); };
  const clickOn = async (locator) => {
    const box = await locator.boundingBox();
    await p.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 25 });
    await sleep(500); await locator.click();
  };

  // 1. the problem
  await p.goto('file://' + V + '/title.html'); mark('title'); await sleep(10000);

  // 2. live: real input -> real output
  await p.goto('http://127.0.0.1:7860/', { waitUntil: 'networkidle' }); mark('live');
  await cap('The demo. <b>Input:</b>&nbsp;today\'s weather reports from Almaty airport, downloaded now. No PM2.5 sensor is needed.');
  await sleep(5000);
  await clickOn(p.getByRole('button', { name: 'Forecast the real tomorrow' }));
  await p.waitForFunction(() => document.body.innerText.includes('Expected daytime PM2.5'), null, { timeout: 60000 });
  await cap('<b>Output:</b>&nbsp;tomorrow\'s school-hours PM2.5, about 57 µg/m³, a likely range, and a decision: PE indoors.');
  await sleep(7500);
  await cap('It also says why: high pressure, a cold night and weak wind keep smoke over the city.');
  await sleep(6000);
  await cap('This is the real tomorrow, 16 November 2026. The answer is not known yet.');
  await sleep(5000);

  // 3. replay: forecast next to the truth
  await clickOn(p.getByRole('tab', { name: /Replay/ })); mark('replay');
  await cap('So we replay evenings the model never saw in training. 16 December 2024: the air today was clean, 23 µg/m³.');
  await sleep(6000);
  await clickOn(p.getByRole('button', { name: 'Forecast tomorrow', exact: true }));
  await p.waitForFunction(() => document.body.innerText.includes('What actually happened'), null, { timeout: 60000 });
  await cap('The main model also uses today\'s PM2.5. Its forecast: 63 µg/m³, a smog warning.');
  await sleep(6000);
  await p.mouse.wheel(0, 420); await sleep(600);
  await cap('Measured the next day: 67 µg/m³. The simple rule "tomorrow = today" would have said 23.');
  await sleep(7500);

  // 4. a failure
  await p.mouse.wheel(0, -420); await sleep(500);
  await clickOn(p.getByRole('button', { name: '2025-10-27' })); await sleep(700);
  await clickOn(p.getByRole('button', { name: 'Forecast tomorrow', exact: true }));
  await p.waitForFunction(() => document.body.innerText.includes('28 October 2025') && document.body.innerText.includes('What actually happened'), null, { timeout: 60000 });
  mark('failure');
  await cap('A day it got wrong, 27 October 2025: forecast 28 µg/m³, no warning.');
  await sleep(5000);
  await p.mouse.wheel(0, 420); await sleep(600);
  await cap('Measured: 69 µg/m³, a missed smog day. The model cannot see tomorrow\'s weather.');
  await sleep(6500);

  // 5. how it works and the comparison
  await p.goto('file://' + V + '/results.html'); mark('results');
  await cap('Data: 5 years of hourly PM2.5 and airport weather. Model: gradient-boosted trees. Test: 398 later days, never shuffled.');
  await sleep(6500);
  await cap('Average miss: "tomorrow = today" 15.3, our main model 12.3, our sensor-free model 13.2 µg/m³.');
  await sleep(7000);
  await p.evaluate(() => { document.getElementById('a').classList.remove('on'); document.getElementById('b').classList.add('on'); });
  await cap('Honest result: far fewer false alarms, 52 and 40 against 76, but more missed smog days, 16 and 19 against 11.');
  await sleep(8000);

  // 6. limits and next steps
  await p.goto('file://' + V + '/end.html'); mark('end'); await sleep(9000);
  mark('stop');
  await ctx.close(); await b.close();
})();

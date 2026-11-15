// Records the demo video: node krecord.js <folder with demo.html> <folder with title.html and end.html>
const { chromium } = require('playwright');
const DEMO = process.argv[2], V = process.argv[3];
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 720 }, recordVideo: { dir: V, size: { width: 1280, height: 720 } } });
  const p = await ctx.newPage();
  const t0 = Date.now(); const mark = (s) => console.log(((Date.now() - t0) / 1000).toFixed(1), s);
  const overlay = async () => p.evaluate(() => {
    if (document.getElementById('cap')) return;
    const c = document.createElement('div'); c.id = 'cap';
    c.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:99999;background:#0b0b0b;color:#fff;font:600 22px/1.35 Inter,Arial,sans-serif;padding:12px 34px;min-height:64px;display:flex;align-items:center;box-sizing:border-box';
    document.body.appendChild(c);
    const m = document.createElement('div'); m.id = 'mouse';
    m.style.cssText = 'position:fixed;z-index:100000;width:22px;height:22px;border-radius:50%;background:rgba(235,104,52,.75);border:2px solid #fff;pointer-events:none;left:-50px;top:-50px;transform:translate(-50%,-50%)';
    document.body.appendChild(m);
    document.addEventListener('mousemove', e => { m.style.left = e.clientX + 'px'; m.style.top = e.clientY + 'px'; });
  });
  const cap = async (text) => { await overlay(); await p.evaluate(t => { document.getElementById('cap').innerHTML = t; }, text); };
  const scrollToHeading = async (text, offset = 18) => {
    await p.evaluate(([text, offset]) => {
      const h = [...document.querySelectorAll('h1, h2')].find(e => e.innerText.includes(text));
      const card = h.closest('section') || h;
      window.scrollTo({ top: Math.max(0, card.getBoundingClientRect().top + window.scrollY - offset), behavior: 'smooth' });
    }, [text, offset]);
    await sleep(1100);
  };
  const clickOn = async (locator) => {
    await locator.scrollIntoViewIfNeeded();
    const box = await locator.boundingBox();
    await p.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 25 });
    await sleep(450); await locator.click(); await sleep(350);
  };

  // 1. the problem
  await p.goto('file://' + V + '/title.html'); mark('title'); await sleep(9500);

  // 2. the demo: a real held-out evening goes in, a message comes out
  await p.goto('file://' + DEMO + '/demo.html'); await sleep(700); mark('demo');
  await cap('The demo is one file: the model runs in the browser. It replays evenings the model never saw in training.');
  await sleep(6500);
  await clickOn(p.getByRole('button', { name: /Smog starts — caught/ }));
  await scrollToHeading('At 18:00 the tool knows');
  await cap('<span><b>Input</b>, 14 November 2024 at 18:00: the air today is clean, 15 µg/m³. Tomorrow\'s weather forecast: cold and calm.</span>');
  await sleep(8000);
  await cap('<span><b>Output:</b> tomorrow about 41 µg/m³, likely 21 to 57. Plan the lesson indoors. The simple rule says 15: no warning.</span>');
  await sleep(8500);
  await scrollToHeading('The next day: what was measured');
  await clickOn(p.locator('#reveal'));
  await scrollToHeading('The next day: what was measured');
  await cap('The next day measured 54 µg/m³. The model\'s advice was right. "Tomorrow = today" missed the start of the smog.');
  await sleep(8500);
  await scrollToHeading('The week plan');
  await cap('A second step plans the week: the two outdoor lessons go to the days forecast to be cleanest.');
  await sleep(7500);

  // 3. a failure
  await cap('Now the model\'s worst day in the whole test period.');
  await p.evaluate(() => window.scrollTo({ top: 0, behavior: 'smooth' })); await sleep(1000);
  await clickOn(p.getByRole('button', { name: /Largest error/ }));
  await scrollToHeading('The next day: what was measured', 330);
  await clickOn(p.locator('#reveal'));
  await scrollToHeading('The next day: what was measured', 330);
  mark('failure');
  await cap('The model\'s largest error, 1 February 2025: forecast 41, measured 98. The warning was right, but the number was far too low.');
  await sleep(9000);

  // 4. how it works and how it compares with the baseline
  await scrollToHeading('Not just this evening'); mark('results');
  await cap('How it works: five years of hourly PM2.5 from one monitor plus the weather forecast. A linear model, tested once on 216 later winter days.');
  await sleep(8500);
  await cap('Average error 12.2 µg/m³ against 17.0 for "tomorrow = today". 22 false alarms instead of 40, and 16 missed bad days instead of 19.');
  await sleep(9000);

  // 5. limits and next steps
  await p.goto('file://' + V + '/end.html'); mark('end'); await sleep(11000);
  mark('stop');
  await ctx.close(); await b.close();
})();

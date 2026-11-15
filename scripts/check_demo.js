// Check that demo.html really runs the notebook's model.
//
//     node scripts/check_demo.js            (needs Node.js and Playwright with Chromium)
//
// It opens the page in a headless browser and
//   1. recomputes the forecast for every held-out evening with the page's own code and compares it with the
//      forecast the notebook saved in results/predictions_test.csv (they must agree within 0.05 µg/m³,
//      and the warn / no-warn decision must be the same on every day);
//   2. clicks through the page (examples, reveal, language, what-if) and fails on any browser error.
// Optional: pass a folder as the first argument to save screenshots there.
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

(async () => {
  const page_path = path.resolve(__dirname, "..", "demo.html");
  const shots = process.argv[2];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
  const errors = [];
  page.on("pageerror", e => errors.push(String(e)));
  page.on("console", m => { if (m.type() === "error") errors.push(m.text()); });
  await page.goto("file://" + page_path + "#d=2025-02-01");

  // 1. the page's forecasts against the notebook's
  const result = await page.evaluate(() => {
    const { DATA, predictAll } = window.SmogDemo;
    const mine = predictAll();
    let worst = 0, flips = 0;
    DATA.rows.forEach((row, i) => {
      worst = Math.max(worst, Math.abs(mine[i] - row.nb));
      if ((mine[i] >= DATA.model.cutoff) !== (row.nb >= DATA.model.cutoff)) flips += 1;
    });
    return { days: mine.length, worst, flips };
  });
  console.log(`forecasts recomputed in the browser: ${result.days} evenings, largest difference from the notebook ` +
              `${result.worst.toFixed(4)} µg/m³, different warn decisions: ${result.flips}`);
  if (result.days !== 396 || result.worst > 0.05 || result.flips !== 0) throw new Error("the page does not reproduce the notebook");

  // 2. the saved CSV itself (so the comparison does not rest only on numbers stored inside the page)
  const csv = fs.readFileSync(path.resolve(__dirname, "..", "results", "predictions_test.csv"), "utf8").trim().split("\n");
  const header = csv[0].split(",");
  const col = name => header.indexOf(name);
  const fromCsv = Object.fromEntries(csv.slice(1).map(line => { const c = line.split(","); return [c[col("issue_day")], +c[col("model")]]; }));
  const fromPage = await page.evaluate(() => Object.fromEntries(window.SmogDemo.DATA.rows.map((r, i) => [r.d, window.SmogDemo.predict(r.x)])));
  let worstCsv = 0;
  for (const day of Object.keys(fromCsv)) worstCsv = Math.max(worstCsv, Math.abs(fromCsv[day] - fromPage[day]));
  console.log(`against results/predictions_test.csv: largest difference ${worstCsv.toFixed(4)} µg/m³ over ${Object.keys(fromCsv).length} evenings`);
  if (!(worstCsv <= 0.05)) throw new Error("the page does not match results/predictions_test.csv");

  // 3. click through the page
  const text = async sel => (await page.textContent(sel)).trim();
  if (await text("#fc-value") !== "41") throw new Error("1 Feb 2025 should show a forecast of 41, got " + await text("#fc-value"));
  if (shots) await page.screenshot({ path: path.join(shots, "demo_1_forecast.png"), fullPage: true });
  await page.click("#reveal");
  if (await text("#measured") !== "98") throw new Error("1 Feb 2025 should reveal 98, got " + await text("#measured"));
  if (shots) await page.screenshot({ path: path.join(shots, "demo_2_revealed.png"), fullPage: true });
  for (const button of await page.$$("#examples button")) {
    await button.click();
    await page.click("#reveal");
  }
  await page.click("#lang-ru");
  if (!(await text("h1")).includes("Смог")) throw new Error("the Russian version did not load");
  if (shots) await page.screenshot({ path: path.join(shots, "demo_3_russian.png"), fullPage: true });
  await page.click("#lang-en");
  await page.fill("#s-temp", "-8");
  await page.dispatchEvent("#s-temp", "input");
  const colder = +(await text("#whatif-value"));
  await page.fill("#s-temp", "8");
  await page.dispatchEvent("#s-temp", "input");
  const warmer = +(await text("#whatif-value"));
  if (!(colder > warmer)) throw new Error("what-if: a colder day should give a higher forecast");
  await page.click("#next"); await page.click("#prev");
  if (shots) {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: path.join(shots, "demo_4_phone.png"), fullPage: true });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    console.log("horizontal overflow at phone width (px):", overflow);
    await page.emulateMedia({ colorScheme: "dark" });
    await page.setViewportSize({ width: 1200, height: 900 });
    await page.screenshot({ path: path.join(shots, "demo_5_dark.png"), fullPage: true });
  }
  await browser.close();
  if (errors.length) throw new Error("browser errors:\n" + errors.join("\n"));
  console.log("demo.html: all checks passed");
})().catch(e => { console.error("FAILED:", e.message); process.exit(1); });

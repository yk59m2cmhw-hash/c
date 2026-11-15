// Screenshots of demo.html for the write-up:  node scripts/make_screenshots.js
const path = require("path");
const { chromium } = require("playwright");
(async () => {
  const url = "file://" + path.resolve(__dirname, "..", "demo.html");
  const out = path.resolve(__dirname, "..", "results", "figures");
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1100, height: 900 }, deviceScaleFactor: 2, colorScheme: "light" });
  // the message for one evening, with the measurement of the next day revealed
  await page.goto(url + "#d=" + (process.argv[2] || "2024-11-14") + "&r=1");
  await page.locator(".grid2").screenshot({ path: path.join(out, "06_demo_message.png") });
  // the week plan of the dirtiest school week of the test period, revealed
  await page.goto(url + "#d=" + (process.argv[3] || "2025-02-02") + "&r=1");
  await page.reload();
  await page.locator("section.card", { has: page.locator("#week") }).screenshot({ path: path.join(out, "07_demo_week.png") });
  await browser.close();
  console.log("saved results/figures/06_demo_message.png and 07_demo_week.png");
})();

// Rend chaque <section id="…"> de kit.html en image : marketing/out/<id>.png
// Usage : node marketing/render.js   (Playwright doit être installé)
const path = require('path');
const fs = require('fs');

function loadPlaywright() {
  for (const name of ['playwright', '/opt/node22/lib/node_modules/playwright']) {
    try { return require(name); } catch (e) { /* essaie le suivant */ }
  }
  throw new Error('Playwright introuvable : npm install playwright');
}

(async () => {
  const { chromium } = loadPlaywright();
  const out = path.join(__dirname, 'out');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const url = 'file://' + path.join(__dirname, 'kit.html');

  // Les sections qui demandent une meilleure définition portent data-scale
  const probe = await browser.newPage();
  await probe.goto(url);
  const sections = await probe.evaluate(() =>
    [...document.querySelectorAll('section[id]')].map((s) => ({ id: s.id, scale: Number(s.dataset.scale || 1) })));
  await probe.close();

  for (const { id, scale } of sections) {
    const page = await browser.newPage({ viewport: { width: 1200, height: 2000 }, deviceScaleFactor: scale });
    await page.goto(url);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    await page.locator('#' + id).screenshot({ path: path.join(out, id + '.png') });
    await page.close();
    console.log('rendu', id);
  }
  await browser.close();
})();

const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.goto('http://localhost:3000/login', { waitUntil: 'domcontentloaded' });
  await page.screenshot({ path: 'evidence/ui_demo/screenshots/smoke_login.png', fullPage: true });
  await browser.close();
  console.log('OK');
})();

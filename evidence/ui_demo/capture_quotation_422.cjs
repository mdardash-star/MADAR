const { chromium } = require('playwright');
const fs = require('node:fs/promises');

(async () => {
  const uniq = Date.now().toString().slice(-6);
  const payloadCapture = {
    request: null,
    responseStatus: null,
    responseBody: null,
    url: null
  };

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });

  page.on('response', async (resp) => {
    const url = resp.url();
    if (url.includes('/api/v1/sales/quotations') && resp.request().method() === 'POST') {
      payloadCapture.url = url;
      payloadCapture.request = resp.request().postData();
      payloadCapture.responseStatus = resp.status();
      try {
        payloadCapture.responseBody = await resp.text();
      } catch {
        payloadCapture.responseBody = '';
      }
    }
  });

  try {
    await page.goto('http://localhost:3000/login', { waitUntil: 'domcontentloaded' });
    await page.getByLabel('البريد الإلكتروني').fill('admin@gulf-trading.demo');
    await page.getByLabel('كلمة المرور').fill('BetaAdmin2026!');
    await page.getByRole('button', { name: 'تسجيل الدخول' }).click();
    await page.waitForURL('**/dashboard', { timeout: 30000 });

    await page.goto('http://localhost:3000/quotations', { waitUntil: 'domcontentloaded' });
    await page.getByRole('button', { name: 'إضافة عرض' }).click();

    const customerSelect = page.getByLabel('العميل *');
    await customerSelect.selectOption({ index: 1 });
    await page.getByLabel('رقم العرض').fill(`UIQ-${uniq}`);
    await page.getByLabel('المبلغ الإجمالي').fill('1500');
    await page.getByLabel('الحالة').selectOption('accepted');

    await page.evaluate(() => document.getElementById('quotation-form').requestSubmit());
    await page.waitForTimeout(2500);
  } finally {
    await browser.close();
  }

  await fs.writeFile('/workspaces/MADAR/evidence/ui_demo/quotation_422_capture.json', JSON.stringify(payloadCapture, null, 2), 'utf8');
  console.log('captured');
})();

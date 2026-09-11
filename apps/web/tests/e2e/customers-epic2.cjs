const { chromium } = require('playwright');
const assert = require('node:assert/strict');

const baseUrl = process.env.PLAYWRIGHT_BASE_URL || 'http://127.0.0.1:3000';

async function registerAndLogin(page, suffix) {
  const email = `e2e-admin-${suffix}@example.com`;
  await page.goto(`${baseUrl}/register`, { waitUntil: 'domcontentloaded' });
  await page.getByLabel('اسم الشركة *').fill(`E2E Company ${suffix}`);
  await page.getByLabel('الاسم المختصر (slug) *').fill(`e2e-company-${suffix}`);
  await page.getByLabel('اسم المدير *').fill('E2E Admin');
  await page.getByLabel('بريد المدير *').fill(email);
  await page.getByLabel('كلمة مرور المدير *').fill('E2eCustomers2026!');
  await page.getByRole('button', { name: 'إنشاء الشركة' }).click();
  await page.waitForURL('**/dashboard', { timeout: 30000 });
}

async function verifyCustomersFlow(browser, viewport) {
  const suffix = `${Date.now()}-${viewport.width}`;
  const context = await browser.newContext({ viewport });
  const page = await context.newPage();
  const browserErrors = [];
  page.on('pageerror', (error) => browserErrors.push(String(error)));

  await registerAndLogin(page, suffix);
  await page.goto(`${baseUrl}/customers`, { waitUntil: 'domcontentloaded' });
  await page.getByRole('heading', { name: 'العملاء' }).waitFor({ timeout: 20000 });

  // Regression gate: the long customer modal must keep its actions reachable.
  await page.getByRole('button', { name: 'إضافة عميل' }).click();
  const cancel = page.getByRole('button', { name: 'إلغاء' });
  await cancel.scrollIntoViewIfNeeded();
  await cancel.click();
  await assert.rejects(
    () => cancel.waitFor({ state: 'visible', timeout: 500 }),
    /Timeout/,
  );

  await page.getByRole('button', { name: 'إضافة عميل' }).click();
  const customerName = `E2E Customer ${suffix}`;
  const customerCode = `E2E-${suffix}`;
  await page.getByLabel('اسم العميل *').fill(customerName);
  await page.getByLabel('رمز العميل *').fill(customerCode);
  await page.getByRole('button', { name: 'إضافة العميل' }).click();
  await page.getByText(customerName).first().waitFor({ timeout: 20000 });

  const search = page.getByPlaceholder('بحث بالاسم أو الرمز أو الرقم الضريبي…');
  await search.fill(customerCode);
  await page.getByText(customerName).first().waitFor({ timeout: 15000 });

  await page.getByRole('button', { name: 'تفاصيل' }).first().click();
  await page.getByText(customerName).first().waitFor({ timeout: 10000 });
  await page.keyboard.press('Escape');

  page.once('dialog', (dialog) => dialog.accept());
  await page.getByRole('button', { name: 'أرشفة' }).first().click();
  await page.getByText('تمت أرشفة العميل.').waitFor({ timeout: 15000 });

  assert.deepEqual(browserErrors, [], `Browser runtime errors: ${browserErrors.join('\n')}`);
  await context.close();
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    await verifyCustomersFlow(browser, { width: 1440, height: 900 });
    await verifyCustomersFlow(browser, { width: 390, height: 844 });
  } finally {
    await browser.close();
  }
  console.log('Customers EPIC 2 browser verification passed on desktop and mobile.');
})().catch((error) => {
  console.error(error);
  process.exit(1);
});

import { chromium } from 'playwright';
import fs from 'node:fs/promises';

const baseUrl = 'http://localhost:3000';
const apiUrl = 'http://localhost:8000';
await fs.mkdir('evidence/ui_demo/screenshots', { recursive: true });

const runtimeErrors = [];
const notes = [];
const uniq = Date.now().toString().slice(-6);
const company = {
  name: `UI Demo Co ${uniq}`,
  slug: `ui-demo-${uniq}`,
  legal: `UI Demo Legal ${uniq}`,
  phone: '+966550000001',
  email: `company+${uniq}@example.com`,
  adminName: 'UI Demo Admin',
  adminEmail: `admin+${uniq}@example.com`,
  adminPassword: 'UiDemo2026!'
};
const customer = { name: `UI Customer ${uniq}`, code: `UICUS-${uniq}` };
const supplier = { name: `UI Supplier ${uniq}`, code: `UISUP-${uniq}` };
const category = { name: `UI Category ${uniq}`, code: `UICAT${uniq}` };
const uom = { name: `UI Piece ${uniq}`, code: `UIP${uniq}` };
const product = { name: `UI Product ${uniq}`, sku: `UISKU-${uniq}` };
const quotation = { number: `UIQ-${uniq}`, amount: '1500' };
const order = { number: `UIO-${uniq}`, amount: '1500' };
const invoice = { number: `UII-${uniq}`, amount: '1500' };

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1600, height: 1000 } });
const page = await context.newPage();

page.on('pageerror', (err) => {
  runtimeErrors.push({ type: 'pageerror', message: String(err) });
});
page.on('console', (msg) => {
  if (msg.type() === 'error') {
    runtimeErrors.push({ type: 'console', message: msg.text() });
  }
});

async function shot(name) {
  await page.screenshot({ path: `evidence/ui_demo/screenshots/${name}.png`, fullPage: true });
}

try {
  await page.goto(baseUrl + '/login', { waitUntil: 'domcontentloaded' });
  await page.getByLabel('البريد الإلكتروني').fill('admin@gulf-trading.demo');
  await page.getByLabel('كلمة المرور').fill('BetaAdmin2026!');
  await page.getByRole('button', { name: 'تسجيل الدخول' }).click();
  await page.waitForURL('**/dashboard', { timeout: 20000 });
  await shot('01_login');

  await page.getByRole('button', { name: 'تسجيل الخروج' }).click();
  await page.waitForURL('**/login', { timeout: 20000 });

  await page.getByRole('link', { name: 'إنشاء شركة جديدة' }).click();
  await page.waitForURL('**/register', { timeout: 20000 });
  await page.getByLabel('اسم الشركة *').fill(company.name);
  await page.getByLabel('الاسم المختصر (slug) *').fill(company.slug);
  await page.getByLabel('الاسم القانوني').fill(company.legal);
  await page.getByLabel('رقم الهاتف').fill(company.phone);
  await page.getByLabel('البريد الإلكتروني للشركة').fill(company.email);
  await page.getByLabel('اسم المدير *').fill(company.adminName);
  await page.getByLabel('بريد المدير *').fill(company.adminEmail);
  await page.getByLabel('كلمة مرور المدير *').fill(company.adminPassword);
  await page.getByRole('button', { name: 'إنشاء الشركة' }).click();
  await page.waitForURL('**/dashboard', { timeout: 30000 });
  await shot('02_create_company');

  await page.goto(baseUrl + '/customers', { waitUntil: 'domcontentloaded' });
  await page.getByRole('button', { name: 'إضافة عميل' }).click();
  await page.getByLabel('اسم العميل *').fill(customer.name);
  await page.getByLabel('الرمز (كود) *').fill(customer.code);
  await page.getByRole('button', { name: 'إضافة العميل' }).click();
  await page.getByText(customer.name).first().waitFor({ timeout: 20000 });
  await shot('03_create_customer');

  await page.goto(baseUrl + '/suppliers', { waitUntil: 'domcontentloaded' });
  await page.getByRole('button', { name: 'إضافة مورد' }).click();
  await page.getByLabel('اسم المورد *').fill(supplier.name);
  await page.getByLabel('الرمز (كود) *').fill(supplier.code);
  await page.getByRole('button', { name: 'إضافة المورد' }).click();
  await page.getByText(supplier.name).first().waitFor({ timeout: 20000 });
  await shot('04_create_supplier');

  await page.goto(baseUrl + '/products', { waitUntil: 'domcontentloaded' });
  await page.getByRole('button', { name: 'إضافة منتج' }).click();

  await page.getByRole('button', { name: '+ جديد' }).nth(0).click();
  await page.getByRole('heading', { name: 'إضافة فئة جديدة' }).waitFor({ timeout: 10000 });
  await page.getByLabel('اسم الفئة *').fill(category.name);
  await page.getByLabel('الرمز *').fill(category.code);
  await page.getByRole('button', { name: 'إضافة' }).click();

  await page.getByRole('button', { name: '+ جديد' }).nth(1).click();
  await page.getByRole('heading', { name: 'إضافة وحدة قياس جديدة' }).waitFor({ timeout: 10000 });
  await page.getByLabel('اسم الوحدة *').fill(uom.name);
  await page.getByLabel('الرمز *').fill(uom.code);
  await page.getByRole('button', { name: 'إضافة' }).click();

  await page.getByLabel('اسم المنتج *').fill(product.name);
  await page.getByLabel('رمز SKU *').fill(product.sku);
  await page.getByLabel('سعر البيع *').fill('1500');
  await page.getByLabel('سعر التكلفة *').fill('1000');
  await page.getByRole('button', { name: 'إضافة المنتج' }).click();
  await page.getByText(product.name).first().waitFor({ timeout: 20000 });
  await shot('05_create_product');

  await page.goto(baseUrl + '/quotations', { waitUntil: 'domcontentloaded' });
  await page.getByRole('button', { name: 'إضافة عرض' }).click();
  await page.getByLabel('العميل *').selectOption({ label: customer.name });
  await page.getByLabel('رقم العرض').fill(quotation.number);
  await page.getByLabel('المبلغ الإجمالي').fill(quotation.amount);
  await page.getByLabel('الحالة').selectOption('accepted');
  await page.getByRole('button', { name: 'إضافة العرض' }).click();
  await page.getByText(quotation.number).first().waitFor({ timeout: 20000 });
  await shot('06_create_quotation');

  // Step 7: attempt quotation -> order conversion through UI
  const convertCandidates = page.locator('button, a', { hasText: /تحويل|Convert|convert/i });
  const convertCount = await convertCandidates.count();
  if (convertCount > 0) {
    await convertCandidates.first().click();
    notes.push('Found conversion action and clicked it.');
  } else {
    runtimeErrors.push({ type: 'functional', message: 'No UI action found to convert quotation to sales order.' });
    notes.push('No quotation->order conversion control in quotations UI; proceeded with manual order creation to continue flow.');
  }

  await page.goto(baseUrl + '/orders', { waitUntil: 'domcontentloaded' });
  await page.getByRole('button', { name: 'إضافة طلب' }).click();
  await page.getByLabel('العميل *').selectOption({ label: customer.name });
  await page.getByLabel('رقم الطلب').fill(order.number);
  await page.getByLabel('المبلغ الإجمالي').fill(order.amount);
  await page.getByLabel('الحالة').selectOption('confirmed');
  await page.getByRole('button', { name: 'إضافة الطلب' }).click();
  await page.getByText(order.number).first().waitFor({ timeout: 20000 });
  await shot('07_convert_to_order_or_manual_order');

  await page.goto(baseUrl + '/invoices', { waitUntil: 'domcontentloaded' });
  await page.getByRole('button', { name: 'إضافة فاتورة' }).click();
  await page.getByLabel('العميل *').selectOption({ label: customer.name });
  await page.getByLabel('رقم الفاتورة').fill(invoice.number);
  await page.getByLabel('المبلغ الإجمالي').fill(invoice.amount);
  // Link order if present
  const orderSelect = page.getByLabel('الطلب المرتبط');
  await orderSelect.selectOption({ label: order.number }).catch(async () => {
    await orderSelect.selectOption({ index: 1 }).catch(() => {});
  });
  await page.getByLabel('الحالة').selectOption('issued');
  await page.getByRole('button', { name: 'إضافة الفاتورة' }).click();
  await page.getByText(invoice.number).first().waitFor({ timeout: 20000 });
  await shot('08_create_invoice');

  await page.goto(baseUrl + '/dashboard', { waitUntil: 'domcontentloaded' });
  await page.getByText('العملاء').first().waitFor({ timeout: 15000 });
  await shot('09_dashboard_kpis');

  const dashboardText = await page.textContent('body');
  if (!dashboardText?.includes('العملاء') || !dashboardText?.includes('الفواتير')) {
    runtimeErrors.push({ type: 'functional', message: 'Dashboard KPI tiles not rendered as expected.' });
  }

} catch (err) {
  runtimeErrors.push({ type: 'fatal', message: String(err) });
} finally {
  await browser.close();
}

await fs.writeFile('evidence/ui_demo/runtime_errors.json', JSON.stringify(runtimeErrors, null, 2), 'utf8');
await fs.writeFile('evidence/ui_demo/notes.json', JSON.stringify(notes, null, 2), 'utf8');
console.log(JSON.stringify({
  baseUrl,
  apiUrl,
  screenshots: [
    'evidence/ui_demo/screenshots/01_login.png',
    'evidence/ui_demo/screenshots/02_create_company.png',
    'evidence/ui_demo/screenshots/03_create_customer.png',
    'evidence/ui_demo/screenshots/04_create_supplier.png',
    'evidence/ui_demo/screenshots/05_create_product.png',
    'evidence/ui_demo/screenshots/06_create_quotation.png',
    'evidence/ui_demo/screenshots/07_convert_to_order_or_manual_order.png',
    'evidence/ui_demo/screenshots/08_create_invoice.png',
    'evidence/ui_demo/screenshots/09_dashboard_kpis.png'
  ],
  runtimeErrorsFile: 'evidence/ui_demo/runtime_errors.json',
  notesFile: 'evidence/ui_demo/notes.json'
}, null, 2));

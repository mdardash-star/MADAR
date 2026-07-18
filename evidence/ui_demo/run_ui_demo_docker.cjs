const { chromium } = require('playwright');
const fs = require('node:fs/promises');

(async () => {
  const baseUrl = 'http://localhost:3000';
  await fs.mkdir('/workspaces/MADAR/evidence/ui_demo/screenshots', { recursive: true });

  const runtimeErrors = [];
  const notes = [];
  const stepStatus = {};
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

  page.on('pageerror', (err) => runtimeErrors.push({ type: 'pageerror', message: String(err) }));
  page.on('console', (msg) => {
    if (msg.type() === 'error') runtimeErrors.push({ type: 'console', message: msg.text() });
  });

  const shot = async (name) => {
    await page.screenshot({ path: `/workspaces/MADAR/evidence/ui_demo/screenshots/${name}.png`, fullPage: true });
  };

  const submitByFormId = async (formId) => {
    await page.evaluate((id) => {
      const form = document.getElementById(id);
      if (!form) throw new Error(`Form not found: ${id}`);
      if (typeof form.requestSubmit === 'function') {
        form.requestSubmit();
      } else {
        form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
      }
    }, formId);
  };

  try {
    // 1) Login
    try {
      await page.goto(baseUrl + '/login', { waitUntil: 'domcontentloaded' });
      await page.getByLabel('البريد الإلكتروني').fill('admin@gulf-trading.demo');
      await page.getByLabel('كلمة المرور').fill('BetaAdmin2026!');
      await page.getByRole('button', { name: 'تسجيل الدخول' }).click();
      await page.waitForURL('**/dashboard', { timeout: 20000 });
      await shot('01_login');
      stepStatus.login = 'pass';
    } catch (err) {
      await shot('01_login_error').catch(() => {});
      stepStatus.login = 'fail';
      runtimeErrors.push({ type: 'step1', message: String(err) });
    }

    // 2) Create Company
    try {
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
      stepStatus.create_company = 'pass';
    } catch (err) {
      await shot('02_create_company_error').catch(() => {});
      stepStatus.create_company = 'fail';
      runtimeErrors.push({ type: 'step2', message: String(err) });
    }

    // 3) Create Customer
    try {
      await page.goto(baseUrl + '/customers', { waitUntil: 'domcontentloaded' });
      await page.getByRole('button', { name: 'إضافة عميل' }).click();
      await page.getByLabel('اسم العميل *').fill(customer.name);
      await page.getByLabel('الرمز (كود) *').fill(customer.code);
      await submitByFormId('customer-form');
      await page.getByText(customer.name).first().waitFor({ timeout: 20000 });
      await shot('03_create_customer');
      stepStatus.create_customer = 'pass';
    } catch (err) {
      await shot('03_create_customer_error').catch(() => {});
      stepStatus.create_customer = 'fail';
      runtimeErrors.push({ type: 'step3', message: String(err) });
    }

    // 4) Create Supplier
    try {
      await page.goto(baseUrl + '/suppliers', { waitUntil: 'domcontentloaded' });
      await page.getByRole('button', { name: 'إضافة مورد' }).click();
      await page.getByLabel('اسم المورد *').fill(supplier.name);
      await page.getByLabel('الرمز (كود) *').fill(supplier.code);
      await submitByFormId('supplier-form');
      await page.getByText(supplier.name).first().waitFor({ timeout: 20000 });
      await shot('04_create_supplier');
      stepStatus.create_supplier = 'pass';
    } catch (err) {
      await shot('04_create_supplier_error').catch(() => {});
      stepStatus.create_supplier = 'fail';
      runtimeErrors.push({ type: 'step4', message: String(err) });
    }

    // 5) Create Product
    try {
      await page.goto(baseUrl + '/products', { waitUntil: 'domcontentloaded' });
      await page.getByRole('button', { name: 'إضافة منتج' }).click();

      await page.getByRole('button', { name: '+ جديد' }).nth(0).click();
      await page.getByRole('heading', { name: 'إضافة فئة جديدة' }).waitFor({ timeout: 10000 });
      await page.getByLabel('اسم الفئة *').fill(category.name);
      const catCode = page.getByLabel('الرمز *');
      await catCode.fill(category.code);
      await catCode.press('Enter');

      await page.getByRole('button', { name: '+ جديد' }).nth(1).click();
      await page.getByRole('heading', { name: 'إضافة وحدة قياس جديدة' }).waitFor({ timeout: 10000 });
      await page.getByLabel('اسم الوحدة *').fill(uom.name);
      const uomCode = page.getByLabel('الرمز *');
      await uomCode.fill(uom.code);
      await uomCode.press('Enter');

      await page.getByLabel('اسم المنتج *').fill(product.name);
      await page.getByLabel('رمز SKU *').fill(product.sku);
      await page.getByLabel('سعر البيع *').fill('1500');
      await page.getByLabel('سعر التكلفة *').fill('1000');
      await submitByFormId('product-form');
      await page.getByText(product.name).first().waitFor({ timeout: 20000 });
      await shot('05_create_product');
      stepStatus.create_product = 'pass';
    } catch (err) {
      await shot('05_create_product_error').catch(() => {});
      stepStatus.create_product = 'fail';
      runtimeErrors.push({ type: 'step5', message: String(err) });
    }

    // 6) Create Quotation
    try {
      await page.goto(baseUrl + '/quotations', { waitUntil: 'domcontentloaded' });
      await page.getByRole('button', { name: 'إضافة عرض' }).click();
      await page.getByLabel('العميل *').selectOption({ label: customer.name });
      await page.getByLabel('رقم العرض').fill(quotation.number);
      await page.getByLabel('المبلغ الإجمالي').fill(quotation.amount);
      await page.getByLabel('الحالة').selectOption('accepted');
      await submitByFormId('quotation-form');
      await page.getByText(quotation.number).first().waitFor({ timeout: 20000 });
      await shot('06_create_quotation');
      stepStatus.create_quotation = 'pass';
    } catch (err) {
      await shot('06_create_quotation_error').catch(() => {});
      stepStatus.create_quotation = 'fail';
      runtimeErrors.push({ type: 'step6', message: String(err) });
    }

    // 7) Convert Quotation to Sales Order
    try {
      await page.goto(baseUrl + '/quotations', { waitUntil: 'domcontentloaded' });
      const convertCandidates = page.locator('button, a', { hasText: /تحويل|Convert|convert/i });
      const convertCount = await convertCandidates.count();
      if (convertCount > 0) {
        await convertCandidates.first().click();
        notes.push('Found conversion action and clicked it.');
        await shot('07_convert_quote_to_order');
      } else {
        throw new Error('No UI action found to convert quotation to sales order.');
      }
      stepStatus.convert_quotation = 'pass';
    } catch (err) {
      await shot('07_convert_quote_to_order_error').catch(() => {});
      stepStatus.convert_quotation = 'fail';
      runtimeErrors.push({ type: 'step7', message: String(err) });
      notes.push('No quotation conversion control in quotations UI.');
    }

    // 8) Create Invoice (create order first if needed)
    try {
      await page.goto(baseUrl + '/orders', { waitUntil: 'domcontentloaded' });
      await page.getByRole('button', { name: 'إضافة طلب' }).click();
      await page.getByLabel('العميل *').selectOption({ label: customer.name });
      await page.getByLabel('رقم الطلب').fill(order.number);
      await page.getByLabel('المبلغ الإجمالي').fill(order.amount);
      await page.getByLabel('الحالة').selectOption('confirmed');
      await submitByFormId('order-form');
      await page.getByText(order.number).first().waitFor({ timeout: 15000 });

      await page.goto(baseUrl + '/invoices', { waitUntil: 'domcontentloaded' });
      await page.getByRole('button', { name: 'إضافة فاتورة' }).click();
      await page.getByLabel('العميل *').selectOption({ label: customer.name });
      await page.getByLabel('رقم الفاتورة').fill(invoice.number);
      await page.getByLabel('المبلغ الإجمالي').fill(invoice.amount);
      const orderSelect = page.getByLabel('الطلب المرتبط');
      await orderSelect.selectOption({ label: order.number }).catch(async () => {
        await orderSelect.selectOption({ index: 1 }).catch(() => {});
      });
      await page.getByLabel('الحالة').selectOption('issued');
      await submitByFormId('invoice-form');
      await page.getByText(invoice.number).first().waitFor({ timeout: 20000 });
      await shot('08_create_invoice');
      stepStatus.create_invoice = 'pass';
    } catch (err) {
      await shot('08_create_invoice_error').catch(() => {});
      stepStatus.create_invoice = 'fail';
      runtimeErrors.push({ type: 'step8', message: String(err) });
    }

    // 9) Verify Dashboard KPIs
    try {
      await page.goto(baseUrl + '/dashboard', { waitUntil: 'domcontentloaded' });
      await page.getByText('العملاء').first().waitFor({ timeout: 15000 });
      await shot('09_dashboard_kpis');
      stepStatus.dashboard_kpi = 'pass';
    } catch (err) {
      await shot('09_dashboard_kpis_error').catch(() => {});
      stepStatus.dashboard_kpi = 'fail';
      runtimeErrors.push({ type: 'step9', message: String(err) });
    }
  } catch (err) {
    runtimeErrors.push({ type: 'fatal_outer', message: String(err) });
    await shot('99_failure_state').catch(() => {});
  } finally {
    await browser.close();
  }

  await fs.writeFile('/workspaces/MADAR/evidence/ui_demo/runtime_errors.json', JSON.stringify(runtimeErrors, null, 2), 'utf8');
  await fs.writeFile('/workspaces/MADAR/evidence/ui_demo/notes.json', JSON.stringify(notes, null, 2), 'utf8');
  await fs.writeFile('/workspaces/MADAR/evidence/ui_demo/step_status.json', JSON.stringify(stepStatus, null, 2), 'utf8');
  console.log('done');
})();

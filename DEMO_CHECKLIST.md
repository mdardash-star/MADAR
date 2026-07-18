# MADAR ERP — Milestone 1 Demo Checklist

**Milestone**: Core Entity Management (End-to-End)  
**Date**: 2026-07-18  
**Stack**: FastAPI backend + Next.js frontend + PostgreSQL

---

## Before you start

```bash
# Start all services
docker compose up --build -d

# Apply migrations
docker compose exec api alembic upgrade head

# Confirm health
curl http://localhost:8000/health
# → {"status":"healthy"}
```

---

## Step 1 — Register a new company

1. Open http://localhost:3000/register
2. Fill in:
   - **اسم الشركة**: `شركة التجربة`
   - **الاسم المختصر**: `tajriba` (unique, no spaces)
   - **اسم المدير**: `محمد المدير`
   - **بريد المدير**: `admin@tajriba.com`
   - **كلمة المرور**: at least 8 characters
3. Click **إنشاء الشركة**

**Expected result**: Redirected to the Dashboard at `/dashboard`

---

## Step 2 — Dashboard loads with live KPIs

1. Verify you are on http://localhost:3000/dashboard
2. Check:
   - Company name shown in the sidebar header
   - 6 KPI tiles visible (العملاء, الموردون, المنتجات, طلبات البيع, الفواتير, فرص CRM)
   - All tiles show **0** (new empty company)
   - Sidebar navigation links: لوحة القيادة, العملاء, الموردون, المنتجات, الملف الشخصي

**Expected result**: Dashboard visible, KPIs = 0, navigation functional

---

## Step 3 — Customers: Create, Edit, Delete

### 3a — Navigate to Customers
1. Click **العملاء** in the sidebar
2. URL should be `/customers`
3. Page header shows "العملاء" with **إضافة عميل** button

### 3b — Create a customer
1. Click **إضافة عميل**
2. Fill in:
   - **اسم العميل**: `شركة أكمي للتقنية`
   - **الرمز**: `ACME-001`
   - **البريد الإلكتروني**: `billing@acme.com`
   - **رقم الهاتف**: `+966500000001`
3. Click **إضافة العميل**

**Expected result**: Modal closes, new customer appears in the list

### 3c — Edit the customer
1. Click **تعديل** on the new customer row
2. Change **رقم الهاتف** to `+966500000099`
3. Click **حفظ التعديلات**

**Expected result**: Phone number updated in the list

### 3d — Search
1. Type `acme` in the search box
2. Only the matching customer should appear

### 3e — Delete
1. Click **حذف** on the customer row
2. Confirm in the delete dialog

**Expected result**: Customer removed from the list; count decreases

### 3f — Dashboard KPI updated
1. Navigate back to the Dashboard
2. **العملاء** tile should now show **0** (since customer was deleted)

---

## Step 4 — Suppliers: Full workflow

Repeat Steps 3b–3e on the **الموردون** page (`/suppliers`) with:
- **اسم المورد**: `شركة الإمداد العالمية`
- **الرمز**: `SUP-001`
- **البريد الإلكتروني**: `supply@global.com`

**Expected result**: Supplier created, edited, and deleted successfully

---

## Step 5 — Products: Full workflow with dependencies

### 5a — Navigate to Products
1. Click **المنتجات** in the sidebar

### 5b — Add a product category
1. Click **إضافة منتج**
2. In the **الفئة** dropdown, click **+ جديد**
3. Enter:
   - **اسم الفئة**: `إلكترونيات`
   - **الرمز**: `ELEC`
4. Click **إضافة**

**Expected result**: Category created and auto-selected in the dropdown

### 5c — Add a unit of measure
1. In the **وحدة القياس** dropdown, click **+ جديد**
2. Enter:
   - **اسم الوحدة**: `قطعة`
   - **الرمز**: `PC`
3. Click **إضافة**

**Expected result**: UoM created and auto-selected

### 5d — Create the product
1. Fill in:
   - **اسم المنتج**: `لابتوب برو 15`
   - **رمز SKU**: `LP15-001`
   - **سعر البيع**: `2999`
   - **سعر التكلفة**: `1800`
   - Verify category and UoM are selected
2. Click **إضافة المنتج**

**Expected result**: Product appears in the list with category and UoM visible

### 5e — Edit the price
1. Click **تعديل** on the product
2. Change **سعر البيع** to `2799`
3. Save

**Expected result**: Selling price updated

### 5f — Delete
1. Click **حذف** and confirm

**Expected result**: Product removed from list

---

## Step 6 — Profile page

1. Click **الملف الشخصي** in the sidebar
2. Verify:
   - Full name shown
   - Email shown
   - Company name shown
   - Company ID shown

---

## Step 7 — Logout and re-login

1. Click **تسجيل الخروج** in the sidebar footer
2. Redirected to `/login`
3. Enter your credentials and click **تسجيل الدخول**
4. Redirected back to `/dashboard`
5. Company name and KPIs are correct

---

## Step 8 — API Tests

```bash
cd apps/api
source .venv/bin/activate
pytest -q
# Expected: 48 passed, 0 failed
```

---

## Step 9 — Full stack test (end-to-end API verification)

```bash
# Verify all release gate tests pass
pytest -v tests/test_release_v01.py
# Expected: 18 passed, 0 failed
```

---

## Checklist summary

| # | Feature | Browser Test | API Test |
|---|---------|-------------|----------|
| 1 | Company registration | ☐ | ✅ |
| 2 | Login with JWT | ☐ | ✅ |
| 3 | Dashboard KPIs (live data) | ☐ | ✅ |
| 4 | Customers — Create | ☐ | ✅ |
| 5 | Customers — Edit | ☐ | ✅ |
| 6 | Customers — Search | ☐ | ✅ |
| 7 | Customers — Delete | ☐ | ✅ |
| 8 | Suppliers — Full CRUD | ☐ | ✅ |
| 9 | Products — Category quick-create | ☐ | ✅ |
| 10 | Products — UoM quick-create | ☐ | ✅ |
| 11 | Products — Full CRUD | ☐ | ✅ |
| 12 | Profile page | ☐ | ✅ |
| 13 | Logout + re-login flow | ☐ | ✅ |
| 14 | Navigation sidebar | ☐ | N/A |

**Legend**: ☐ = Requires manual browser test | ✅ = Automated test passing

---

## Known limitations at this milestone

- Sales, Purchasing, Inventory, Accounting, HR, Assets, CRM modules have no frontend UI yet — API-only
- Product search in the list is client-filtered; server-side search is available via API
- No pagination UI (load limit = 100 records per page)
- No multi-branch or multi-role management UI yet

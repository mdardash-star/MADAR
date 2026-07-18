# MADAR — Closed Beta User Test Plan

**Version**: 1.0  
**Date**: 2026-07-18  
**Beta Program**: v1.0.0-beta  
**Estimated Duration**: 45–90 minutes per tester

---

## Welcome to the MADAR Beta Program

Thank you for participating in the MADAR closed beta. This test plan walks you through the key workflows of the system. Please follow each scenario in order, note any issues you encounter, and submit feedback using the provided templates.

---

## Before You Begin

### Access Details

| URL | Purpose |
|-----|---------|
| `http://localhost:3000` | Web application (frontend) |
| `http://localhost:8000/docs` | Interactive API documentation |
| `http://localhost:8000/health` | System health status |

### Demo Credentials

| Role | Email | Password | What You Can Do |
|------|-------|----------|----------------|
| **System Administrator** | admin@gulf-trading.demo | BetaAdmin2026! | Full access to all modules |
| **Sales Manager** | sales@gulf-trading.demo | BetaSales2026! | Customers, quotations, orders, invoices |
| **Inventory Manager** | inventory@gulf-trading.demo | BetaInventory2026! | Warehouses, products, stock movements |
| **Accountant** | accountant@gulf-trading.demo | BetaAccount2026! | Invoices, reports, financial data |

### Demo Company

**Gulf Electronics & Trading Ltd**  
A regional electronics distributor operating across Saudi Arabia and UAE.

Pre-loaded data includes:
- 3 branch offices (Riyadh HQ, Dammam, Dubai)
- 4 warehouses
- 8 customers (major enterprise accounts)
- 5 suppliers (international distributors)
- 15 products (consumer electronics, networking, office equipment)
- 6 quotations in various statuses
- 6 sales orders
- 3 invoices
- 13 stock movements

---

## Test Scenarios

---

### Scenario 1 — System Login & Navigation

**User Role**: Any  
**Time**: ~5 minutes  
**Objective**: Verify login works and the application navigates correctly.

#### Steps

1. Open `http://localhost:3000` in your browser
2. Verify the login page loads with email and password fields
3. Enter credentials for the **Sales Manager** role:
   - Email: `sales@gulf-trading.demo`
   - Password: `BetaSales2026!`
4. Click **Login**

#### Expected Outcomes

- [ ] Login page displays correctly without visual glitches
- [ ] Invalid credentials (wrong password) shows a clear error message
- [ ] Successful login redirects to the Dashboard
- [ ] Sidebar navigation shows all menu items
- [ ] User name appears in the top navigation bar
- [ ] Application is responsive on desktop (1920×1080 minimum)

#### Also Test

- [ ] Log out and log back in as **Inventory Manager** (inventory@gulf-trading.demo)
- [ ] Log out and log back in as **Accountant** (accountant@gulf-trading.demo)
- [ ] Verify each role sees the appropriate menu items

---

### Scenario 2 — Dashboard Overview

**User Role**: System Administrator  
**Time**: ~5 minutes  
**Objective**: Verify the KPI dashboard loads and displays accurate data.

#### Steps

1. Log in as: `admin@gulf-trading.demo` / `BetaAdmin2026!`
2. Navigate to the **Dashboard**
3. Verify the KPI tiles display

#### Expected Outcomes

- [ ] Dashboard loads within 3 seconds
- [ ] Following KPI counts are visible:
  - Branches: **3**
  - Warehouses: **4**
  - Customers: **8**
  - Suppliers: **5**
  - Products: **15**
  - Quotations: **6**
  - Sales Orders: **6**
  - Invoices: **3**
- [ ] All numbers match the counts above
- [ ] No blank or error tiles
- [ ] Dashboard refreshes correctly on page reload

---

### Scenario 3 — Branch & Warehouse Management

**User Role**: System Administrator  
**Time**: ~10 minutes  
**Objective**: Test CRUD operations on organizational structure.

#### Steps — Create a Branch

1. Navigate to **Branches** in the sidebar
2. Verify the existing 3 branches are listed
3. Click **Add Branch** (or equivalent button)
4. Fill in the form:
   - Name: `Jeddah Branch`
   - Code: `JED-001`
   - Country: `Saudi Arabia`
   - City: `Jeddah`
   - Timezone: `Asia/Riyadh`
5. Save the branch

#### Expected Outcomes — Branch Creation

- [ ] Branch list shows 3 branches on load
- [ ] Add Branch form opens correctly
- [ ] Required field validation shows error if name/code is empty
- [ ] Branch saves successfully with success notification
- [ ] New branch appears in the list (total: 4)
- [ ] Dashboard branch count updates to **4**

#### Steps — Edit a Branch

1. Click the **Edit** button on "Jeddah Branch"
2. Change the name to `Jeddah West Branch`
3. Save changes

#### Expected Outcomes — Branch Edit

- [ ] Edit form opens with pre-filled current values
- [ ] Name updates correctly
- [ ] Updated name appears immediately in the list

#### Steps — Create a Warehouse

1. Navigate to **Warehouses**
2. Click **Add Warehouse**
3. Fill in:
   - Name: `Jeddah Distribution Center`
   - Code: `WH-JED-01`
   - Branch: select `Jeddah West Branch`
   - Address: `King Abdul Aziz Industrial, Jeddah`
4. Save

#### Expected Outcomes — Warehouse Creation

- [ ] Warehouse creation form has branch selector
- [ ] Branch dropdown shows all branches including new one
- [ ] Warehouse saves successfully
- [ ] Warehouse count on dashboard updates to **5**

#### Steps — Delete a Record

1. Delete the "Jeddah West Branch" you just created
2. Confirm the deletion prompt

#### Expected Outcomes — Deletion

- [ ] Delete confirmation prompt appears (not immediate delete)
- [ ] After confirmation, branch disappears from list
- [ ] Dashboard count returns to **3**

---

### Scenario 4 — Customer Management

**User Role**: Sales Manager  
**Time**: ~10 minutes  
**Objective**: Test customer CRUD and search functionality.

#### Steps — View Customers

1. Log in as: `sales@gulf-trading.demo` / `BetaSales2026!`
2. Navigate to **Customers**
3. Review the customer list

#### Expected Outcomes

- [ ] 8 customers are listed
- [ ] Customer table shows: Name, Code, Email, Phone, Status
- [ ] No blank rows or display errors

#### Steps — Create a New Customer

1. Click **Add Customer**
2. Fill in:
   - Name: `Emirates NBD Technology Dept`
   - Code: `GULF-CUS-009`
   - Email: `it-procurement@emiratesnbd.com`
   - Phone: `+971-4-2345678`
   - Address: `ENBD HQ, Deira, Dubai`
3. Save

#### Expected Outcomes

- [ ] Form validates email format
- [ ] Form validates required fields (name, code)
- [ ] Customer saves with success message
- [ ] Total customers: **9**
- [ ] New customer appears in list

#### Steps — Edit a Customer

1. Edit the new customer you created
2. Add/update the phone number to `+971-4-2345679`
3. Save

#### Expected Outcomes

- [ ] Edit form opens with existing data pre-filled
- [ ] Update saves successfully
- [ ] Change reflected in the list

#### Steps — Search/Filter

1. Use the search bar to filter by "Aramco"

#### Expected Outcomes

- [ ] Search filters results to show only Aramco-related customers
- [ ] Clearing search restores full list

---

### Scenario 5 — Product Catalog

**User Role**: Inventory Manager  
**Time**: ~10 minutes  
**Objective**: Test product management.

#### Steps

1. Log in as: `inventory@gulf-trading.demo` / `BetaInventory2026!`
2. Navigate to **Products**
3. Verify 15 products are listed with SKU, name, category, price
4. Click **Add Product**
5. Fill in:
   - Name: `Lenovo ThinkPad X1 Carbon`
   - SKU: `LT-LEN-X1C`
   - Category: `Consumer Electronics`
   - Unit of Measure: `Piece`
   - Cost Price: `1600.00`
   - Selling Price: `2199.99`
6. Save

#### Expected Outcomes

- [ ] Product list shows 15 products on load
- [ ] Category selector shows all 5 categories
- [ ] UoM selector shows available units
- [ ] Numeric fields only accept numbers
- [ ] Selling price and cost price are separate fields
- [ ] Product saves successfully
- [ ] Product count: **16**

---

### Scenario 6 — Full Sales Workflow (Critical Path)

**User Role**: Sales Manager  
**Time**: ~20 minutes  
**Objective**: Test the complete quotation → order → invoice workflow.

#### Step 6.1 — Create a Quotation

1. Log in as Sales Manager
2. Navigate to **Quotations**
3. Verify 6 existing quotations in various statuses
4. Click **Create Quotation**
5. Fill in:
   - Customer: `Emirates NBD Technology Dept` (the one you created)
   - Quotation Date: today
   - Valid Until: 30 days from today
   - Warehouse: `Main Warehouse – Riyadh`
   - Total Amount: `15000.00`
   - Status: `draft`
6. Save

#### Expected Outcomes — Quotation

- [ ] Quotation list shows correct existing quotations
- [ ] Customer selector includes all 9 customers
- [ ] Warehouse selector shows all warehouses
- [ ] Date picker works correctly
- [ ] Quotation saves with an auto-generated code (QT-BETA-*)
- [ ] New quotation appears in list

#### Step 6.2 — Convert to Sales Order

1. Navigate to **Orders**
2. Click **Create Order**
3. Fill in:
   - Customer: `Al-Faisaliah Group`
   - Order Date: today
   - Warehouse: `Main Warehouse – Riyadh`
   - Status: `confirmed`
   - Total Amount: `18999.90`
4. Save

#### Expected Outcomes — Order

- [ ] Order list shows existing 6 orders
- [ ] New order saves with code SO-BETA-*
- [ ] Order count: **7**

#### Step 6.3 — Generate Invoice

1. Navigate to **Invoices**
2. Click **Create Invoice**
3. Fill in:
   - Customer: `Al-Faisaliah Group`
   - Invoice Date: today
   - Due Date: 30 days from today
   - Status: `issued`
   - Total Amount: `21849.89` (18999.90 + 15% VAT)
4. Save

#### Expected Outcomes — Invoice

- [ ] Invoice list shows existing 3 invoices
- [ ] New invoice saves with code INV-BETA-*
- [ ] Invoice count: **4**
- [ ] Dashboard invoice count updates

---

### Scenario 7 — Inventory Management

**User Role**: Inventory Manager  
**Time**: ~10 minutes  
**Objective**: Test stock movement recording.

#### Steps — Record Stock Receipt

1. Log in as Inventory Manager
2. Navigate to **Inventory → Stock Movements**
3. Verify 13 existing movements
4. Record a new stock receipt:
   - Product: `Dell Latitude 5540`
   - Warehouse: `Main Warehouse – Riyadh`
   - Quantity: `20`
   - Movement Type: `purchase`
   - Reference Type: `supplier`
   - Note: `Beta test stock receipt`
5. Save

#### Expected Outcomes

- [ ] Stock movements list shows 13 existing records
- [ ] Product selector shows all products
- [ ] Warehouse selector shows all warehouses
- [ ] Quantity must be a positive number
- [ ] Movement saves successfully
- [ ] Movement count: **14**

---

### Scenario 8 — User Profile

**User Role**: Any  
**Time**: ~5 minutes  
**Objective**: Test user profile page.

#### Steps

1. Click on your name/profile icon in the top navigation
2. Navigate to your profile page

#### Expected Outcomes

- [ ] Profile page shows user's full name, email, and role
- [ ] Company information is displayed
- [ ] Page loads without errors

---

### Scenario 9 — API Documentation

**User Role**: Developer/Technical Tester  
**Time**: ~5 minutes  
**Objective**: Verify API documentation is accessible and functional.

#### Steps

1. Open `http://localhost:8000/docs` in your browser
2. Find the `POST /auth/login` endpoint
3. Click **Try it out**
4. Enter your credentials and execute

#### Expected Outcomes

- [ ] Swagger UI loads completely
- [ ] All endpoint groups are listed
- [ ] Login via Swagger returns a token
- [ ] Token can be used to authorize further requests

---

### Scenario 10 — Cross-Role Validation

**User Role**: All roles  
**Time**: ~10 minutes  
**Objective**: Verify each role sees appropriate data and has correct access.

| Test | Admin | Sales Mgr | Inventory Mgr | Accountant |
|------|-------|-----------|---------------|------------|
| View Dashboard | ✓ | ✓ | ✓ | ✓ |
| View Customers | ✓ | ✓ | ✓ | ✓ |
| Create Customer | ✓ | ✓ | ✗ | ✗ |
| View Products | ✓ | ✓ | ✓ | ✓ |
| Create Product | ✓ | ✗ | ✓ | ✗ |
| View Quotations | ✓ | ✓ | ✗ | ✓ |
| Create Quotation | ✓ | ✓ | ✗ | ✗ |
| View Stock Movements | ✓ | ✓ | ✓ | ✗ |
| Create Stock Movement | ✓ | ✗ | ✓ | ✗ |
| View Invoices | ✓ | ✓ | ✗ | ✓ |
| Create Invoice | ✓ | ✓ | ✗ | ✓ |

> **Note for Beta**: Role enforcement at the UI level is currently limited. The API enforces permissions via JWT roles. UI permission gates are planned for v1.1.0. Please note any cases where the UI allows actions that should be restricted.

---

## Reporting Issues

Please use the provided templates for all findings:

- **[BUG_REPORT_TEMPLATE.md](BUG_REPORT_TEMPLATE.md)** — for defects and unexpected behavior
- **[BETA_FEEDBACK_TEMPLATE.md](BETA_FEEDBACK_TEMPLATE.md)** — for general feedback and suggestions

### Severity Guide

| Severity | When to Use |
|----------|------------|
| **Critical (P1)** | System crashes, data loss, complete feature failure |
| **High (P2)** | Feature not working, but workaround exists |
| **Medium (P3)** | Minor issues, confusing UI, slow performance |
| **Low (P4)** | Cosmetic issues, typos, minor UX improvements |

---

## Known Limitations for Beta Testers

Please be aware of these known limitations before testing:

1. **UI Role Enforcement**: The frontend does not currently restrict menu visibility by role. All users see all menu items regardless of permissions. Permission enforcement happens at the API layer only.

2. **No Pagination**: List tables load all records simultaneously. With large datasets (500+ records), page load times may increase.

3. **Data Export**: No export (CSV/PDF) functionality yet.

4. **In-App Notifications**: No email or push notifications for workflow events (e.g., invoice due, order status change).

5. **API Docs in Production**: The `/docs` endpoint is available in this beta build. It will be disabled in production.

6. **Code Uniqueness**: Customer and supplier codes must be globally unique (not just per-company). If you encounter a "duplicate code" error, add a company prefix (e.g., "GULF-").

7. **No Print/Export**: Quotations, orders, and invoices cannot be printed or exported as PDF.

8. **No Real-Time Updates**: Dashboard counts do not auto-refresh. You must reload the page to see updated counts.

9. **Browser Support**: Tested on Chrome and Firefox. Safari/Edge may have minor visual differences.

10. **RTL Completeness**: Arabic RTL layout is implemented at the navigation level. Some UI components may not fully respect RTL direction.

---

## Test Completion Checklist

Once you have completed all scenarios, please confirm:

- [ ] Scenario 1: Login & Navigation — PASS / FAIL / PARTIAL
- [ ] Scenario 2: Dashboard — PASS / FAIL / PARTIAL
- [ ] Scenario 3: Branch & Warehouse Management — PASS / FAIL / PARTIAL
- [ ] Scenario 4: Customer Management — PASS / FAIL / PARTIAL
- [ ] Scenario 5: Product Catalog — PASS / FAIL / PARTIAL
- [ ] Scenario 6: Full Sales Workflow — PASS / FAIL / PARTIAL
- [ ] Scenario 7: Inventory Management — PASS / FAIL / PARTIAL
- [ ] Scenario 8: User Profile — PASS / FAIL / PARTIAL
- [ ] Scenario 9: API Documentation — PASS / FAIL / PARTIAL
- [ ] Scenario 10: Cross-Role Validation — PASS / FAIL / PARTIAL
- [ ] Bug reports submitted for all failures
- [ ] Beta feedback form completed

---

## Contact & Support

If you encounter a blocking issue during testing, contact:

- **Email**: beta@madar.app
- **GitHub Issues**: https://github.com/mdardash-star/MADAR/issues (use Beta label)
- **Response time**: Within 2 business hours for critical issues

---

*Thank you for your time and feedback — it directly shapes the MADAR v1.0 release!*

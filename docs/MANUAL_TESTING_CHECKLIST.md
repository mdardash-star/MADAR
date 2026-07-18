# MADAR v0.1.0-beta Manual Testing Checklist

This document lists all manual testing steps that require human verification before the release.

**Last Updated**: 2026-07-18  
**Tester**: [Name]  
**Date Tested**: [Date]  
**Status**: ⏳ Pending / ✅ Complete / ❌ Failed

---

## Pre-Testing Setup

- [ ] Fresh clone of repository
- [ ] `.env` files copied and configured
- [ ] Docker Compose stack running (`docker compose up --build`)
- [ ] Database migrations completed (`docker compose exec api alembic upgrade head`)
- [ ] Sample data seeded (`docker compose exec api python scripts/seed_sample_data.py`)
- [ ] Frontend accessible at http://localhost:3000
- [ ] API accessible at http://localhost:8000/docs

---

## 1. Installation & Setup (CRITICAL)

### 1.1 Fresh Repository Clone
- [ ] Clone repository: `git clone https://github.com/mdardash-star/MADAR.git`
- [ ] Navigate to directory: `cd MADAR`
- [ ] Confirm directory structure is complete
- [ ] All `.env.example` files present

### 1.2 Environment Configuration
- [ ] Copy `.env.example` to `.env`
- [ ] Copy `apps/api/.env.example` to `apps/api/.env`
- [ ] Copy `apps/web/.env.example` to `apps/web/.env`
- [ ] Update `.env` with valid values if needed
- [ ] No errors when sourcing `.env` files

### 1.3 Docker Compose Startup
- [ ] `docker compose up --build` completes without errors
- [ ] All 4 services start successfully:
  - [ ] PostgreSQL (port 5432)
  - [ ] Redis (port 6379)
  - [ ] FastAPI (port 8000)
  - [ ] Next.js (port 3000)
- [ ] No critical errors in logs
- [ ] Wait 30 seconds, all services remain running

### 1.4 Database Migrations
- [ ] Run `docker compose exec api alembic upgrade head`
- [ ] Command completes successfully
- [ ] No migration errors
- [ ] All tables created in database
- [ ] Verify with: `docker compose exec db psql -U madar -d madar -c "\dt"`

---

## 2. API Endpoints (CRITICAL)

### 2.1 Health & Status
- [ ] `GET /health` returns `{"status":"healthy"}`
- [ ] `GET /api/v1/` returns API info
- [ ] API Docs available at `/docs` (Swagger UI)
- [ ] API ReDoc available at `/redoc`

### 2.2 Authentication Endpoints
- [ ] `POST /companies/register` creates company
  - [ ] Returns company ID, admin details, JWT tokens
  - [ ] Admin user automatically created
  - [ ] Head Office branch auto-created
  - [ ] Permissions and roles seeded
- [ ] `POST /auth/login` authenticates user
  - [ ] Valid credentials return access token
  - [ ] Invalid credentials return 401
  - [ ] Response includes `access_token`, `refresh_token`, `token_type`
- [ ] `POST /auth/refresh` refreshes tokens
  - [ ] Valid refresh token returns new access token
  - [ ] Expired refresh token returns 401
- [ ] `GET /api/v1/me` returns user profile
  - [ ] Returns authenticated user details
  - [ ] Requires valid Bearer token
  - [ ] Returns 401 without token

### 2.3 Master Data Endpoints

#### 2.3.1 Branches
- [ ] `GET /api/v1/master-data/branches` lists branches (filtered by company)
- [ ] `POST /api/v1/master-data/branches` creates branch
- [ ] `PUT /api/v1/master-data/branches/{id}` updates branch
- [ ] `DELETE /api/v1/master-data/branches/{id}` soft deletes branch
- [ ] Deleted branches excluded from list query

#### 2.3.2 Warehouses
- [ ] `GET /api/v1/master-data/warehouses` lists warehouses
- [ ] `POST /api/v1/master-data/warehouses` creates warehouse with branch_id
- [ ] `PUT /api/v1/master-data/warehouses/{id}` updates warehouse
- [ ] `DELETE /api/v1/master-data/warehouses/{id}` soft deletes warehouse

#### 2.3.3 Customers
- [ ] `GET /api/v1/master-data/customers` lists customers
- [ ] `POST /api/v1/master-data/customers` creates customer
- [ ] `PUT /api/v1/master-data/customers/{id}` updates customer
- [ ] `DELETE /api/v1/master-data/customers/{id}` soft deletes customer

#### 2.3.4 Suppliers
- [ ] `GET /api/v1/master-data/suppliers` lists suppliers
- [ ] `POST /api/v1/master-data/suppliers` creates supplier
- [ ] `PUT /api/v1/master-data/suppliers/{id}` updates supplier
- [ ] `DELETE /api/v1/master-data/suppliers/{id}` soft deletes supplier

#### 2.3.5 Products
- [ ] `GET /api/v1/master-data/products` lists products
- [ ] `POST /api/v1/master-data/products` creates product with category_id and unit_of_measure_id
- [ ] `PUT /api/v1/master-data/products/{id}` updates product
- [ ] `DELETE /api/v1/master-data/products/{id}` soft deletes product

### 2.4 Sales Workflow Endpoints

#### 2.4.1 Quotations
- [ ] `POST /api/v1/sales/quotations` creates quotation
  - [ ] Returns 201 with quotation details
  - [ ] Requires: customer_id, quotation_date, expiry_date, total_amount, warehouse_id
  - [ ] Auto-generates code and quotation_number
- [ ] `GET /api/v1/sales/quotations` lists quotations
- [ ] `PUT /api/v1/sales/quotations/{id}` updates quotation
- [ ] `DELETE /api/v1/sales/quotations/{id}` soft deletes quotation

#### 2.4.2 Sales Orders
- [ ] `POST /api/v1/sales/orders` creates order
  - [ ] Returns 201 with order details
  - [ ] Requires: customer_id, order_date, total_amount, warehouse_id
- [ ] `GET /api/v1/sales/orders` lists orders
- [ ] `PUT /api/v1/sales/orders/{id}` updates order
- [ ] `DELETE /api/v1/sales/orders/{id}` soft deletes order

#### 2.4.3 Sales Invoices
- [ ] `POST /api/v1/sales/invoices` creates invoice
  - [ ] Returns 201 with invoice details
  - [ ] Requires: customer_id, invoice_date, order_id, total_amount
- [ ] `GET /api/v1/sales/invoices` lists invoices
- [ ] `PUT /api/v1/sales/invoices/{id}` updates invoice
- [ ] `DELETE /api/v1/sales/invoices/{id}` soft deletes invoice

### 2.5 Dashboard Endpoint
- [ ] `GET /api/v1/dashboard/summary?company_id={id}` returns KPIs
  - [ ] Returns: branches, warehouses, customers, suppliers, products, quotations, sales_orders, sales_invoices, crm_leads counts
  - [ ] All counts are correct and current
  - [ ] Counts reflect only non-deleted items
  - [ ] Counts are filtered by company_id

### 2.6 Error Handling
- [ ] Invalid JWT token returns 401
- [ ] Missing required fields return 422 with validation details
- [ ] Duplicate codes/emails return 400
- [ ] Non-existent resources return 404
- [ ] Unauthorized actions return 403

---

## 3. Frontend UI Testing

### 3.1 Navigation & Layout
- [ ] Login page displays on first visit
- [ ] Sidebar navigation visible after login
- [ ] All 9 menu items are clickable:
  - [ ] Dashboard
  - [ ] Branches
  - [ ] Warehouses
  - [ ] Customers
  - [ ] Suppliers
  - [ ] Products
  - [ ] Quotations
  - [ ] Orders
  - [ ] Invoices
- [ ] User profile dropdown in top-right
- [ ] Logout button works and redirects to login

### 3.2 Registration & Login
- [ ] Registration page displays with all required fields
- [ ] Form validation shows errors for:
  - [ ] Empty company name
  - [ ] Invalid email
  - [ ] Weak password
  - [ ] Mismatched passwords
- [ ] Successful registration redirects to login
- [ ] Login with valid credentials shows dashboard
- [ ] Login with invalid credentials shows error
- [ ] "Remember me" checkbox functional (optional)

### 3.3 Dashboard
- [ ] All 9 KPI tiles display
- [ ] KPI tiles show correct numbers
- [ ] Color coding is consistent
- [ ] Tiles are responsive on different screen sizes
- [ ] Dashboard updates when new data is added

### 3.4 Master Data Pages (CRUD Operations)

#### 3.4.1 Branches
- [ ] **List**: Shows all branches in table
- [ ] **Create**: "Add Branch" button opens modal
  - [ ] Form has: name, code, country, city, timezone
  - [ ] Form validation works
  - [ ] Submit creates branch (visual confirmation)
- [ ] **Edit**: Click edit icon opens modal with pre-filled data
  - [ ] Data is editable
  - [ ] Submit updates data
  - [ ] Changes reflect in list
- [ ] **Delete**: Delete button shows confirmation modal
  - [ ] Confirm deletes branch
  - [ ] Branch disappears from list (soft delete)
  - [ ] Cancel aborts deletion
- [ ] **Search**: Search field filters branches by name/code

#### 3.4.2 Warehouses (Same structure as Branches)
- [ ] List, Create, Edit, Delete, Search all functional

#### 3.4.3 Customers (Same structure)
- [ ] List, Create, Edit, Delete, Search all functional

#### 3.4.4 Suppliers (Same structure)
- [ ] List, Create, Edit, Delete, Search all functional

#### 3.4.5 Products
- [ ] List shows: name, SKU, category, UoM, price
- [ ] Create product requires:
  - [ ] Name, SKU, category, UoM, cost price, selling price
  - [ ] Category and UoM selectors work (dropdowns show options)
- [ ] Edit and Delete work as expected
- [ ] Search filters by name/SKU

### 3.5 Sales Workflow Pages

#### 3.5.1 Quotations
- [ ] List shows quotations with status
- [ ] Create quotation:
  - [ ] Customer selector shows list
  - [ ] Date pickers work
  - [ ] Warehouse selector shows available warehouses
  - [ ] Form submits and creates quotation
- [ ] Edit quotation updates data
- [ ] Delete quotation removes from list

#### 3.5.2 Orders (Same structure as Quotations)
- [ ] CRUD operations fully functional

#### 3.5.3 Invoices (Same structure as Quotations)
- [ ] CRUD operations fully functional

### 3.6 Form Validations
- [ ] Required fields show error if empty
- [ ] Email fields validate email format
- [ ] Number fields only accept numbers
- [ ] Date fields show date picker
- [ ] Duplicate codes show error
- [ ] Success messages show after save
- [ ] Error messages display clearly

### 3.7 Responsive Design
- [ ] Desktop (1920x1080): All elements visible, properly aligned
- [ ] Tablet (768px): Layout adapts, navigation remains accessible
- [ ] Mobile (375px): Sidebar collapses, menu becomes hamburger, content readable
- [ ] Tables scroll horizontally on small screens

### 3.8 RTL/Arabic Support (If Applicable)
- [ ] Text direction is RTL
- [ ] Input fields have RTL direction
- [ ] Icons and buttons aligned correctly for RTL
- [ ] Sidebar positioned on right side
- [ ] Navigation items display in RTL order

---

## 4. Data Management Testing

### 4.1 Company Isolation (Multi-tenancy)
- [ ] User A data is not visible to User B
- [ ] Register two companies with separate admins
- [ ] Each admin only sees their own company data
- [ ] Create branch in Company A, verify Company B admin doesn't see it
- [ ] API filters correctly: only returns data for authenticated user's company

### 4.2 Soft Deletes
- [ ] Deleted items don't appear in lists
- [ ] Database still contains deleted items (check `is_deleted=true`)
- [ ] Deleted items can theoretically be restored (soft delete functionality)

### 4.3 Data Persistence
- [ ] Create data, restart Docker, verify data still exists
- [ ] Database persists across container restarts

### 4.4 Cascade Operations
- [ ] Deleting customer doesn't cause errors
- [ ] Deleting product doesn't affect other products
- [ ] Relationship integrity maintained

---

## 5. Performance Testing

### 5.1 API Response Times
- [ ] List endpoints respond < 500ms with 100+ records
- [ ] Create endpoints respond < 300ms
- [ ] Update endpoints respond < 300ms
- [ ] Delete endpoints respond < 200ms

### 5.2 Frontend Performance
- [ ] Dashboard loads < 2 seconds
- [ ] Page transitions smooth (<300ms)
- [ ] No noticeable lag in forms
- [ ] Tables with 100+ rows render without freezing

### 5.3 Database Performance
- [ ] Queries execute efficiently
- [ ] No N+1 query problems visible in API logs
- [ ] Indexes properly configured (check migration)

---

## 6. Security Testing

### 6.1 Authentication
- [ ] Unauthorized users cannot access `/api/v1/*` endpoints
- [ ] Missing JWT token returns 401
- [ ] Expired JWT token returns 401
- [ ] Invalid JWT signature returns 401
- [ ] JWT tokens contain company_id and user_id

### 6.2 Password Security
- [ ] Passwords are hashed (not stored in plain text)
- [ ] Weak passwords rejected during registration
- [ ] Password requirements enforced

### 6.3 CORS & Headers
- [ ] Frontend can call API without CORS errors
- [ ] Appropriate security headers present

### 6.4 Input Validation
- [ ] SQL injection attempts blocked (parametrized queries used)
- [ ] XSS attempts blocked (React/Pydantic validation)
- [ ] File uploads (if any) validated

---

## 7. Database Testing

### 7.1 Data Integrity
- [ ] Foreign key constraints enforced
- [ ] Required fields cannot be null
- [ ] Unique constraints work (e.g., unique codes per company)
- [ ] No orphaned records

### 7.2 Migrations
- [ ] `alembic upgrade head` completes without errors
- [ ] `alembic downgrade base` reverses all migrations
- [ ] `alembic upgrade head` reapplies all migrations
- [ ] No data loss during migration

### 7.3 Timestamps
- [ ] `created_at` timestamp set automatically
- [ ] `updated_at` timestamp set on creation
- [ ] `updated_at` changes when record modified
- [ ] Timestamps are in UTC

---

## 8. End-to-End Workflow Testing

### 8.1 Complete 12-Step Workflow
- [ ] Register company → Success
- [ ] Login → Success
- [ ] Create branch → Success
- [ ] Create warehouse → Success
- [ ] Create customer → Success
- [ ] Create supplier → Success
- [ ] Create product → Success
- [ ] Create quotation → Success
- [ ] Create order → Success
- [ ] Create invoice → Success
- [ ] Record inventory movement → Success
- [ ] Dashboard KPIs updated → Success
- [ ] All operations maintain data integrity

---

## 9. Documentation Review

### 9.1 README.md
- [ ] Accurate project description
- [ ] Prerequisites listed correctly
- [ ] Quick start instructions work as written
- [ ] Links to other docs functional
- [ ] No outdated information

### 9.2 INSTALL.md
- [ ] Step-by-step instructions accurate
- [ ] Prerequisites correct and complete
- [ ] Docker Compose setup verified
- [ ] Local dev setup verified
- [ ] Database migration instructions work

### 9.3 QUICK_START.md
- [ ] 5-minute setup actually takes ~5 minutes
- [ ] All commands execute without error
- [ ] End result is working application

### 9.4 CONTRIBUTING.md
- [ ] Coding standards clear
- [ ] Branch naming convention documented
- [ ] Pull request process outlined
- [ ] Testing guidelines provided

### 9.5 API Documentation
- [ ] `/docs` (Swagger) is complete and accurate
- [ ] All endpoints documented with examples
- [ ] Request/response schemas correct
- [ ] Error responses documented

---

## 10. Sample Data & Seeding

### 10.1 Sample Data Script
- [ ] `python scripts/seed_sample_data.py` completes without error
- [ ] Demo company created: ACME Corporation
- [ ] Admin user created: admin@acme-demo.com
- [ ] 3 branches created and visible in UI
- [ ] 3 warehouses created and visible
- [ ] 4 customers created
- [ ] 3 suppliers created
- [ ] 5 products created
- [ ] 2 quotations created
- [ ] 2 orders created
- [ ] 1 invoice created

### 10.2 Demo Data in Dashboard
- [ ] Dashboard shows correct counts:
  - [ ] Branches: 3
  - [ ] Warehouses: 3
  - [ ] Customers: 4
  - [ ] Suppliers: 3
  - [ ] Products: 5
  - [ ] Quotations: 2
  - [ ] Orders: 2
  - [ ] Invoices: 1

---

## 11. Browser Compatibility

### 11.1 Chrome/Chromium
- [ ] All pages render correctly
- [ ] Forms work
- [ ] No console errors
- [ ] Responsive design works

### 11.2 Firefox
- [ ] All pages render correctly
- [ ] Forms work
- [ ] No console errors
- [ ] Responsive design works

### 11.3 Safari
- [ ] All pages render correctly
- [ ] Forms work
- [ ] No console errors

### 11.4 Edge
- [ ] All pages render correctly
- [ ] Forms work
- [ ] No console errors

---

## 12. Release Checklist

- [ ] All above tests passed
- [ ] No critical bugs found
- [ ] No high-priority issues blocking release
- [ ] Documentation complete and accurate
- [ ] Sample data seeding works
- [ ] GitHub release draft created
- [ ] CHANGELOG updated
- [ ] Version bumped (if applicable)

---

## Notes & Issues Found

### Critical Issues (Must Fix Before Release)
- [ ] Issue 1: [Description]
- [ ] Issue 2: [Description]

### High Priority Issues (Should Fix Before Release)
- [ ] Issue 1: [Description]

### Medium Priority Issues (Can Fix in Next Release)
- [ ] Issue 1: [Description]

### Low Priority Issues / Suggestions
- [ ] Issue 1: [Description]

---

## Sign-Off

**Tested By**: [Name]  
**Date**: [Date]  
**Overall Status**: ⏳ Pending / ✅ PASSED / ❌ FAILED  
**Release Ready**: ⏳ No / ✅ Yes / ❌ No

**Signature**: ___________________

**Additional Notes**:
[Any additional notes or observations]

---

## Retest Log

| Date | Tester | Status | Notes |
|------|--------|--------|-------|
| YYYY-MM-DD | Name | ✅ PASSED | Initial test complete |
| | | | |

---

**Questions?** Contact: [maintainer email]

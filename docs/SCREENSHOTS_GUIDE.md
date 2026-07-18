# MADAR Screenshots & Demo Guide

This guide provides instructions for generating screenshots and creating demo videos for MADAR.

## Prerequisites

- Running MADAR instance (see [QUICK_START.md](QUICK_START.md))
- Demo company and sample data seeded (run `python scripts/seed_sample_data.py`)
- Demo credentials: `admin@acme-demo.com` / `Demo123!`

## Screenshot Workflow

### 1. Landing Page / Login

**File**: `docs/screenshots/01_login.png`

1. Navigate to http://localhost:3000
2. Screenshot the login/register page
3. Shows the initial entry point

**Key Elements**:
- MADAR logo/branding
- Login form
- "Register Company" button/link

---

### 2. Company Registration

**File**: `docs/screenshots/02_registration.png`

**Steps**:
1. Click "Register Company"
2. Fill registration form:
   - Company Name: `ACME Demo Corp`
   - Company Slug: `acme-demo`
   - Admin Email: `admin@acme.com`
   - Password: `Demo123!`
   - Admin Full Name: `John Doe`
3. Click Register
4. Screenshot success page with company details

**Key Elements**:
- Registration form validation
- Success confirmation

---

### 3. Dashboard KPIs

**File**: `docs/screenshots/03_dashboard.png`

**Steps**:
1. Login with demo credentials
2. Land on dashboard
3. Screenshot showing:
   - KPI tiles (Branches, Warehouses, Customers, Suppliers, Products, etc.)
   - Real-time data from database
   - Color-coded indicators

**Key Elements**:
- 9 KPI cards with metrics
- Dashboard grid layout
- Data summary

---

### 4. Master Data Management

#### 4a. Branches
**File**: `docs/screenshots/04_branches.png`

**Steps**:
1. Navigate to Branches (sidebar)
2. Show branch list
3. Show create/edit modal
4. Screenshot the page

**Key Elements**:
- Branch table with list of branches
- Add Branch button
- Edit/Delete actions

#### 4b. Warehouses
**File**: `docs/screenshots/04b_warehouses.png`

Same structure but for warehouses.

#### 4c. Customers
**File**: `docs/screenshots/04c_customers.png`

Same structure but for customers.

#### 4d. Suppliers
**File**: `docs/screenshots/04d_suppliers.png`

Same structure but for suppliers.

#### 4e. Products
**File**: `docs/screenshots/04e_products.png`

Same structure but for products.

---

### 5. Sales Workflow

#### 5a. Create Quotation
**File**: `docs/screenshots/05_quotation.png`

**Steps**:
1. Navigate to Quotations
2. Click "Add Quotation"
3. Fill form:
   - Customer: Select from dropdown
   - Quotation Number: Auto-generated
   - Date & Expiry: Fill dates
   - Items: Show pricing breakdown
4. Screenshot the form

**Key Elements**:
- Quotation form with validation
- Customer selector
- Pricing fields (subtotal, tax, discount, total)

#### 5b. Create Sales Order
**File**: `docs/screenshots/05b_order.png`

Same workflow for orders, showing order-specific fields.

#### 5c. Generate Invoice
**File**: `docs/screenshots/05c_invoice.png`

Same workflow for invoices, showing invoice-specific fields.

---

### 6. Inventory Management

**File**: `docs/screenshots/06_inventory.png`

**Steps**:
1. Navigate to Stock Movements (or Inventory)
2. Show list of stock movements
3. Show create movement form
4. Screenshot the interface

**Key Elements**:
- Stock movement list with transaction history
- Product selector
- Quantity field
- Movement type (purchase, sale, adjustment)

---

### 7. User Profile

**File**: `docs/screenshots/07_profile.png`

**Steps**:
1. Click profile icon (top right)
2. View profile page
3. Screenshot showing user info

**Key Elements**:
- User information display
- Company info
- Role/Permissions display
- Logout option

---

## Demo Video Workflow

### Screen Recording Setup

Using a tool like OBS Studio, recordmydesktop, or browser dev tools:

1. Set resolution to 1920x1080 (recommended)
2. Zoom browser to 100%
3. Use clear, readable fonts
4. Slow down interactions (2-3 seconds per action)

### Demo Script (3-5 minutes)

```
[Scene 1: Title] (5 sec)
"MADAR - Enterprise ERP SaaS"

[Scene 2: Login] (30 sec)
1. Show login page
2. Enter credentials
3. Click login
4. Wait for dashboard to load

[Scene 3: Dashboard] (30 sec)
"The dashboard provides real-time KPIs for your business"
Hover over KPI cards to show tooltips

[Scene 4: Creating Master Data] (1 min)
1. Navigate to Branches
2. Click Add Branch
3. Fill form and save
4. Show the new branch in list

[Scene 5: Sales Workflow] (1.5 min)
1. Create Quotation
   - Select customer
   - Fill pricing
   - Save
2. Convert to Order
3. Generate Invoice
4. Show the complete workflow

[Scene 6: Dashboard Update] (30 sec)
"Notice how the dashboard KPIs updated in real-time"
Refresh dashboard to show updated counts

[Outro] (15 sec)
"MADAR - Enterprise ERP for SMEs"
```

---

## Screenshots Checklist

### Before Release

- [ ] Dashboard with KPIs
- [ ] Login/Registration page
- [ ] Master data (Branches, Warehouses, Customers, Suppliers, Products)
- [ ] Sales workflow (Quotation → Order → Invoice)
- [ ] Inventory management
- [ ] User profile
- [ ] API documentation (Swagger UI)
- [ ] Mobile view (if responsive)
- [ ] RTL layout (if Arabic)

### Image Requirements

- **Format**: PNG (for lossless quality)
- **Resolution**: 1920x1080 minimum
- **Size**: Optimize before uploading (<200KB per image)
- **Naming**: `{sequence}_{feature_name}.png`
- **Location**: Store in `/docs/screenshots/`

---

## Optimization Tools

### Compress Screenshots

```bash
# Using ImageMagick
convert original.png -quality 85 optimized.png

# Using pngquant
pngquant --speed 1 --quality 70-85 -- original.png
```

### Create thumbnails

```bash
# Using ImageMagick
convert original.png -resize 400x300 thumbnail.png
```

---

## RTL/Arabic Screenshots

If documenting RTL support:

1. Change language to Arabic in app
2. Verify RTL layout is proper
3. Screenshot key pages showing RTL formatting
4. Store in `/docs/screenshots/rtl/` folder

---

## Accessibility Screenshots

Show:
- Keyboard navigation (Tab through elements)
- Focus indicators
- Color contrast
- Alternative text for images

---

## Demo Data Notes

The demo company **ACME Corporation** includes:

**Branches** (3):
- Headquarters (HQ-NYC) - New York
- West Coast Hub (WC-LAX) - Los Angeles
- East Coast Warehouse (EC-BOS) - Boston

**Customers** (4):
- ABC Trading Corp
- Global Imports LLC
- Pacific Distributors
- Northeast Retailers

**Products** (5):
- Laptop Pro 15 ($1,299.99)
- Desktop PC ($899.99)
- Industrial Printer ($2,499.99)
- Steel Bars ($150.00/100kg)
- Adhesive Tape ($25.00)

**Quotations/Orders/Invoices**:
- Pre-populated sample transactions showing complete workflow

---

## Hosting Screenshots

### In Documentation

```markdown
![Dashboard KPI Screenshot](docs/screenshots/03_dashboard.png)
*Figure 1: Dashboard showing real-time KPIs*
```

### In README

```markdown
## Features

### Dashboard
![Dashboard](docs/screenshots/03_dashboard.png)

### Sales Management
![Quotations](docs/screenshots/05_quotation.png)
```

### In GitHub Release

Upload screenshots to the release notes to show:
- New features added
- Bug fixes
- UI improvements

---

## Video Hosting

Options for hosting demo videos:

1. **YouTube**: Upload unlisted video, embed in README
2. **GitHub Releases**: Upload video file (max 10MB recommended)
3. **Loom**: Record and share link in docs
4. **OBS + Streamable**: Quick recording sharing

---

## Tips for Good Screenshots

✅ **Good**:
- Clean, uncluttered UI
- Relevant data visible
- Proper zoom level (readable text)
- Consistent styling
- Focused on the feature

❌ **Avoid**:
- Sensitive data (real customer names, emails)
- Cluttered backgrounds
- Poor contrast
- Unfinished forms
- Error states (unless demonstrating error handling)

---

## Update Schedule

- [ ] Create initial screenshots for v0.1.0-beta
- [ ] Update after major UI changes
- [ ] Add new feature screenshots before release
- [ ] Review for consistency quarterly

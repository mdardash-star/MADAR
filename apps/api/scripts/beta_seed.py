#!/usr/bin/env python3
"""
MADAR Closed Beta — Demo Database Seed Script
==============================================

Creates a complete, realistic demo environment for beta testing with:
  - Gulf Trading Company (Gulf Electronics & Trading Ltd)
  - 4 demo user accounts with distinct roles
  - Realistic operational data across all modules

Usage:
    # From Docker (recommended):
    docker compose exec api sh -c "cd /app && PYTHONPATH=/app python scripts/beta_seed.py"

    # Local dev:
    cd apps/api && python scripts/beta_seed.py

Demo Accounts Created:
    admin@gulf-trading.demo      / BetaAdmin2026!     (System Administrator)
    sales@gulf-trading.demo      / BetaSales2026!     (Sales Manager)
    inventory@gulf-trading.demo  / BetaInventory2026! (Inventory Manager)
    accountant@gulf-trading.demo / BetaAccount2026!   (Accountant)
"""

import sys
from datetime import datetime, timedelta, date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.branch import Branch
from app.models.company import Company
from app.models.customer import Customer
from app.models.permission import Permission
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.role import Role, role_permission_association
from app.models.sales_invoice import SalesInvoice
from app.models.sales_order import SalesOrder
from app.models.sales_quotation import SalesQuotation
from app.models.stock_movement import StockMovement
from app.models.supplier import Supplier
from app.models.unit_of_measure import UnitOfMeasure
from app.models.user import User
from app.models.warehouse import Warehouse


# ─── Permission sets per role ────────────────────────────────────────────────

ALL_PERMISSIONS = [
    # Identity & company
    ("company.manage",     "Manage company settings"),
    ("branch.manage",      "Create and manage branches"),
    ("user.manage",        "Create and manage users"),
    ("rbac.manage",        "Manage roles and permissions"),
    ("audit.view",         "View audit log"),
    # Master data
    ("customers.read",     "View customers"),
    ("customers.write",    "Create and edit customers"),
    ("customers.delete",   "Delete customers"),
    ("suppliers.read",     "View suppliers"),
    ("suppliers.write",    "Create and edit suppliers"),
    ("suppliers.delete",   "Delete suppliers"),
    ("products.read",      "View product catalog"),
    ("products.write",     "Create and edit products"),
    ("products.delete",    "Delete products"),
    ("warehouses.read",    "View warehouses"),
    ("warehouses.write",   "Create and edit warehouses"),
    ("warehouses.delete",  "Delete warehouses"),
    # Sales
    ("quotations.read",    "View quotations"),
    ("quotations.write",   "Create and edit quotations"),
    ("quotations.delete",  "Delete quotations"),
    ("orders.read",        "View sales orders"),
    ("orders.write",       "Create and edit orders"),
    ("orders.delete",      "Delete orders"),
    ("invoices.read",      "View invoices"),
    ("invoices.write",     "Create and edit invoices"),
    ("invoices.delete",    "Delete invoices"),
    # Inventory
    ("inventory.read",     "View stock levels"),
    ("inventory.write",    "Record stock movements"),
    ("inventory.delete",   "Delete stock movements"),
    # Reporting
    ("reports.view",       "View dashboards and reports"),
    ("reports.export",     "Export reports"),
    # Finance
    ("accounts.read",      "View chart of accounts"),
    ("accounts.write",     "Create journal entries"),
]

ROLE_PERMISSIONS = {
    "admin": {p[0] for p in ALL_PERMISSIONS},
    "sales-manager": {
        "customers.read", "customers.write",
        "suppliers.read",
        "products.read",
        "warehouses.read",
        "quotations.read", "quotations.write", "quotations.delete",
        "orders.read", "orders.write", "orders.delete",
        "invoices.read", "invoices.write",
        "inventory.read",
        "reports.view", "reports.export",
    },
    "inventory-manager": {
        "products.read", "products.write",
        "warehouses.read", "warehouses.write",
        "suppliers.read", "suppliers.write",
        "customers.read",
        "inventory.read", "inventory.write", "inventory.delete",
        "orders.read",
        "reports.view",
    },
    "accountant": {
        "invoices.read", "invoices.write",
        "orders.read",
        "quotations.read",
        "customers.read",
        "suppliers.read",
        "products.read",
        "accounts.read", "accounts.write",
        "reports.view", "reports.export",
    },
}

# ─── Demo users ──────────────────────────────────────────────────────────────

DEMO_USERS = [
    {
        "email":      "admin@gulf-trading.demo",
        "password":   "BetaAdmin2026!",
        "full_name":  "Mohammed Al-Rashidi",
        "role_slug":  "admin",
        "title":      "System Administrator",
    },
    {
        "email":      "sales@gulf-trading.demo",
        "password":   "BetaSales2026!",
        "full_name":  "Sara Al-Mansouri",
        "role_slug":  "sales-manager",
        "title":      "Sales Manager",
    },
    {
        "email":      "inventory@gulf-trading.demo",
        "password":   "BetaInventory2026!",
        "full_name":  "Khalid Al-Otaibi",
        "role_slug":  "inventory-manager",
        "title":      "Inventory Manager",
    },
    {
        "email":      "accountant@gulf-trading.demo",
        "password":   "BetaAccount2026!",
        "full_name":  "Fatima Al-Zahrawi",
        "role_slug":  "accountant",
        "title":      "Accountant",
    },
]


def seed_permissions(db) -> dict[str, Permission]:
    """Create all permissions; return codename → Permission map."""
    perm_map = {}
    for codename, description in ALL_PERMISSIONS:
        p = db.query(Permission).filter(Permission.codename == codename).first()
        if not p:
            p = Permission(codename=codename, description=description)
            db.add(p)
    db.flush()
    for codename, _ in ALL_PERMISSIONS:
        perm_map[codename] = db.query(Permission).filter(Permission.codename == codename).first()
    return perm_map


def seed_roles(db, company_id: int, perm_map: dict) -> dict[str, Role]:
    """Create 4 roles with scoped permission sets."""
    role_definitions = [
        ("admin",             "Administrator",     "Full system access"),
        ("sales-manager",     "Sales Manager",     "Sales workflow and customer management"),
        ("inventory-manager", "Inventory Manager", "Warehouse and stock management"),
        ("accountant",        "Accountant",        "Finance and invoicing"),
    ]
    role_map = {}
    for slug, name, _desc in role_definitions:
        role = db.query(Role).filter(
            Role.company_id == company_id, Role.slug == slug
        ).first()
        if not role:
            role = Role(company_id=company_id, name=name, slug=slug)
            db.add(role)
            db.flush()
        allowed = ROLE_PERMISSIONS.get(slug, set())
        role.permissions = [perm_map[c] for c in allowed if c in perm_map]
        role_map[slug] = role
    db.flush()
    return role_map


def seed_users(db, company_id: int, role_map: dict, branch_id: int) -> dict[str, User]:
    """Create 4 demo users; return email → User map."""
    user_map = {}
    for ud in DEMO_USERS:
        user = db.query(User).filter(User.email == ud["email"]).first()
        if not user:
            user = User(
                company_id=company_id,
                branch_id=branch_id,
                role_id=role_map[ud["role_slug"]].id,
                email=ud["email"],
                full_name=ud["full_name"],
                hashed_password=get_password_hash(ud["password"]),
                is_active=True,
            )
            db.add(user)
        else:
            user.role_id = role_map[ud["role_slug"]].id
            user.full_name = ud["full_name"]
        user_map[ud["email"]] = user
    db.flush()
    return user_map


# ─── Main seeding logic ───────────────────────────────────────────────────────

def seed_beta_data():
    db = SessionLocal()
    try:
        print("\n" + "=" * 65)
        print("  MADAR Closed Beta — Demo Database Seeding")
        print("=" * 65)

        # ── Company ──────────────────────────────────────────────────────
        print("\n▶  Company")
        company = db.query(Company).filter(Company.slug == "beta-gulf-trading").first()
        if not company:
            company = Company(
                name="Gulf Electronics & Trading Ltd",
                slug="beta-gulf-trading",
                legal_name="Gulf Electronics & Trading Limited Company",
                email="info@gulf-trading.demo",
                phone="+966-11-4567890",
                is_active=True,
            )
            db.add(company)
            db.flush()
            print(f"   ✓ Created: {company.name} (ID {company.id})")
        else:
            print(f"   ℹ Already exists: {company.name} (ID {company.id})")
        cid = company.id

        # ── Branches ─────────────────────────────────────────────────────
        print("\n▶  Branches")
        branch_data = [
            ("Head Office – Riyadh",      "HO-RUH",  "Saudi Arabia", "Riyadh",  "Asia/Riyadh"),
            ("Eastern Province Branch",   "EP-DMM",  "Saudi Arabia", "Dammam",  "Asia/Riyadh"),
            ("Dubai Sales Office",        "SO-DXB",  "UAE",          "Dubai",   "Asia/Dubai"),
        ]
        branches = []
        for name, code, country, city, tz in branch_data:
            b = db.query(Branch).filter(Branch.code == code).first()
            if not b:
                b = Branch(company_id=cid, name=name, code=code,
                           country=country, city=city, timezone=tz, is_active=True)
                db.add(b)
                db.flush()
                print(f"   ✓ {name}")
            else:
                print(f"   ℹ {name} (exists)")
            branches.append(b)
        db.flush()

        # ── Permissions + Roles ──────────────────────────────────────────
        print("\n▶  Permissions & Roles")
        perm_map = seed_permissions(db)
        role_map = seed_roles(db, cid, perm_map)
        for slug, role in role_map.items():
            print(f"   ✓ Role [{slug}] — {len(role.permissions)} permissions")
        db.flush()

        # ── Users ────────────────────────────────────────────────────────
        print("\n▶  Demo User Accounts")
        user_map = seed_users(db, cid, role_map, branches[0].id)
        for ud in DEMO_USERS:
            print(f"   ✓ {ud['full_name']:30s}  {ud['email']:35s}  [{ud['role_slug']}]")
        db.flush()

        # ── Warehouses ───────────────────────────────────────────────────
        print("\n▶  Warehouses")
        warehouse_data = [
            ("Main Warehouse – Riyadh",      "WH-RUH-01", branches[0].id, "Industrial Zone, Riyadh"),
            ("Eastern Province Warehouse",    "WH-DMM-01", branches[1].id, "King Fahd Industrial, Dammam"),
            ("Dubai Transit Hub",             "WH-DXB-01", branches[2].id, "Dubai Airport Freezone"),
            ("Riyadh Returns Warehouse",      "WH-RUH-02", branches[0].id, "South Industrial, Riyadh"),
        ]
        warehouses = []
        for name, code, bid, addr in warehouse_data:
            wh = db.query(Warehouse).filter(
                Warehouse.company_id == cid, Warehouse.code == code
            ).first()
            if not wh:
                wh = Warehouse(company_id=cid, branch_id=bid, name=name,
                               code=code, address=addr, is_active=True)
                db.add(wh)
                db.flush()
                print(f"   ✓ {name}")
            else:
                print(f"   ℹ {name} (exists)")
            warehouses.append(wh)
        db.flush()

        # ── Product Categories ────────────────────────────────────────────
        print("\n▶  Product Categories")
        cat_data = [
            ("Consumer Electronics",  "CAT-CE",  "Laptops, tablets, phones, accessories"),
            ("Networking Equipment",  "CAT-NET", "Routers, switches, access points, cables"),
            ("Office Equipment",      "CAT-OFC", "Printers, scanners, projectors"),
            ("Smart Home Devices",    "CAT-SHD", "Smart speakers, cameras, automation"),
            ("Spare Parts",           "CAT-SP",  "Replacement components and accessories"),
        ]
        categories = []
        for name, code, desc in cat_data:
            cat = db.query(ProductCategory).filter(
                ProductCategory.company_id == cid, ProductCategory.code == code
            ).first()
            if not cat:
                cat = ProductCategory(company_id=cid, name=name, code=code,
                                      description=desc, is_active=True)
                db.add(cat)
                db.flush()
                print(f"   ✓ {name}")
            else:
                print(f"   ℹ {name} (exists)")
            categories.append(cat)
        db.flush()

        # ── Units of Measure ─────────────────────────────────────────────
        print("\n▶  Units of Measure")
        uom_data = [
            ("Piece",   "PCS", "pc"),
            ("Box",     "BOX", "bx"),
            ("Carton",  "CTN", "ctn"),
            ("Pallet",  "PLT", "plt"),
            ("Set",     "SET", "set"),
            ("Meter",   "MTR", "m"),
        ]
        uoms = []
        for name, code, abbr in uom_data:
            # code is globally unique across all companies
            uom = db.query(UnitOfMeasure).filter(UnitOfMeasure.code == code).first()
            if not uom:
                uom = UnitOfMeasure(company_id=cid, name=name, code=code,
                                    abbreviation=abbr, is_active=True)
                db.add(uom)
                db.flush()
                print(f"   ✓ {name}")
            else:
                print(f"   ℹ {name} (exists globally, reusing)")
            uoms.append(uom)
        db.flush()

        # ── Products ─────────────────────────────────────────────────────
        print("\n▶  Products")
        product_data = [
            # name,                  sku,          cost,      sell,      cat_idx, uom_idx
            ("Dell Latitude 5540",   "LT-DELL-5540",  1450.00,  1899.99,  0, 0),
            ("MacBook Air M3",       "LT-APPLE-M3",   1800.00,  2499.99,  0, 0),
            ("iPad Pro 12.9\"",      "TB-APPLE-IPP",   950.00,  1299.99,  0, 0),
            ("iPhone 15 Pro",        "PH-APPLE-I15P", 1050.00,  1449.99,  0, 0),
            ("Samsung Galaxy S24",   "PH-SAM-S24",     850.00,  1099.99,  0, 0),
            ("Cisco Router RV340",   "NW-CSC-RV340",   280.00,   399.99,  1, 0),
            ("Ubiquiti UAP-AC-Pro",  "NW-UBI-UAPAC",   120.00,   179.99,  1, 0),
            ("HP LaserJet Pro 4001", "PR-HP-LJ4001",   350.00,   499.99,  2, 0),
            ("Epson EcoTank L3250",  "PR-EPS-L3250",   185.00,   269.99,  2, 0),
            ("Ring Video Doorbell",  "SH-RING-VDB",     65.00,    99.99,  3, 0),
            ("Philips Hue Starter",  "SH-PHI-HSK",      75.00,   119.99,  3, 4),
            ("Dell Laptop Battery",  "SP-DELL-BAT",     35.00,    59.99,  4, 0),
            ("USB-C Charging Cable", "SP-USB-C-2M",      3.50,     9.99,  4, 1),
            ("Cat6 Network Cable",   "NW-CAT6-50M",     12.00,    24.99,  1, 5),
            ("Logitech MX Keys",     "PH-LOG-MXKY",     65.00,    99.99,  0, 0),
        ]
        products = []
        for name, sku, cost, sell, ci, ui in product_data:
            prod = db.query(Product).filter(
                Product.company_id == cid, Product.sku == sku
            ).first()
            if not prod:
                prod = Product(
                    company_id=cid,
                    name=name, sku=sku,
                    cost_price=cost, selling_price=sell,
                    category_id=categories[ci].id,
                    unit_of_measure_id=uoms[ui].id,
                    is_active=True,
                )
                db.add(prod)
                db.flush()
            products.append(prod)
        print(f"   ✓ {len(products)} products seeded")
        db.flush()

        # ── Customers ────────────────────────────────────────────────────
        print("\n▶  Customers")
        customer_data = [
            ("Al-Faisaliah Group",         "GULF-CUS-001", "procurement@alfaisaliah.com", "+966-11-2345678", "Riyadh, KSA"),
            ("Aramco Digital Solutions",   "GULF-CUS-002", "it-procurement@aramco.com",   "+966-13-8901234", "Dhahran, KSA"),
            ("Dubai Smart City Office",    "GULF-CUS-003", "procurement@dsc.gov.ae",      "+971-4-5678901",  "Dubai, UAE"),
            ("Sabic Innovation Center",    "GULF-CUS-004", "lab-orders@sabic.com",        "+966-13-3456789", "Jubail, KSA"),
            ("Maaden Technology Dept",     "GULF-CUS-005", "tech@maaden.com.sa",          "+966-16-7890123", "Riyadh, KSA"),
            ("NEOM Technology Division",   "GULF-CUS-006", "it@neom.com",                 "+966-11-9012345", "Tabuk, KSA"),
            ("STC Enterprise Solutions",   "GULF-CUS-007", "enterprise@stc.com.sa",       "+966-11-4567890", "Riyadh, KSA"),
            ("Aldar Properties IT Dept",   "GULF-CUS-008", "procurement@aldar.com",       "+971-2-6789012",  "Abu Dhabi, UAE"),
        ]
        customers = []
        for name, code, email, phone, addr in customer_data:
            cust = db.query(Customer).filter(
                Customer.company_id == cid, Customer.code == code
            ).first()
            if not cust:
                cust = Customer(company_id=cid, name=name, code=code,
                                email=email, phone=phone, address=addr, is_active=True)
                db.add(cust)
                db.flush()
            customers.append(cust)
        print(f"   ✓ {len(customers)} customers seeded")
        db.flush()

        # ── Suppliers ────────────────────────────────────────────────────
        print("\n▶  Suppliers")
        supplier_data = [
            ("Dell Technologies MEA",   "GULF-SUP-001", "supply@dell-mea.com",       "+971-4-3456789", "Dubai, UAE"),
            ("Apple Authorized Dist.",  "GULF-SUP-002", "b2b@apple-me.com",          "+971-4-9012345", "Dubai, UAE"),
            ("Cisco Systems MENA",      "GULF-SUP-003", "cisco-mena@cisco.com",      "+971-4-5678901", "Dubai, UAE"),
            ("Ingram Micro KSA",        "GULF-SUP-004", "orders@ingrammicro.com.sa", "+966-11-2345678", "Riyadh, KSA"),
            ("Samsung B2B Gulf",        "GULF-SUP-005", "b2bgulf@samsung.com",       "+971-4-1234567", "Dubai, UAE"),
        ]
        suppliers = []
        for name, code, email, phone, addr in supplier_data:
            sup = db.query(Supplier).filter(
                Supplier.company_id == cid, Supplier.code == code
            ).first()
            if not sup:
                sup = Supplier(company_id=cid, name=name, code=code,
                               email=email, phone=phone, address=addr, is_active=True)
                db.add(sup)
                db.flush()
            suppliers.append(sup)
        print(f"   ✓ {len(suppliers)} suppliers seeded")
        db.flush()

        # ── Sales Quotations ─────────────────────────────────────────────
        print("\n▶  Sales Quotations")
        today = date.today()
        quotation_scenarios = [
            # (customer_idx, warehouse_idx, subtotal, status, days_back, valid_days)
            (0, 0, 18999.90,  "sent",      5,  30),   # Al-Faisaliah — 10 Dell laptops
            (1, 0, 24999.90,  "sent",      3,  30),   # Aramco — 10 MacBooks
            (2, 2, 12999.90,  "draft",     1,  14),   # Dubai — iPads
            (3, 0,  4999.95,  "accepted",  8,  30),   # Sabic — phones
            (4, 1,  8999.91,  "expired",  45,  14),   # Maaden — networking (expired)
            (5, 0, 34999.80,  "draft",     0,  30),   # NEOM — large deal
        ]
        quotations = []
        for i, (ci2, wi, subtotal, status, days_back, valid_days) in enumerate(quotation_scenarios):
            code = f"QT-BETA-{i + 1:04d}"
            q = db.query(SalesQuotation).filter(
                SalesQuotation.company_id == cid, SalesQuotation.code == code
            ).first()
            if not q:
                qdate = today - timedelta(days=days_back)
                tax = round(subtotal * 0.15, 2)
                q = SalesQuotation(
                    company_id=cid,
                    customer_id=customers[ci2].id,
                    warehouse_id=warehouses[wi].id,
                    code=code,
                    quote_date=qdate,
                    valid_until=qdate + timedelta(days=valid_days),
                    status=status,
                    subtotal_amount=subtotal,
                    tax_amount=tax,
                    discount_amount=0.00,
                    total_amount=subtotal + tax,
                    note=f"Beta demo quotation #{i + 1}",
                )
                db.add(q)
                db.flush()
            quotations.append(q)
        print(f"   ✓ {len(quotations)} quotations seeded")
        db.flush()

        # ── Sales Orders ─────────────────────────────────────────────────
        print("\n▶  Sales Orders")
        order_scenarios = [
            (0, 0,  18999.90, "confirmed", 4),   # From QT-BETA-0001
            (1, 0,  24999.90, "processing", 2),  # From QT-BETA-0002
            (3, 0,   4999.95, "delivered",  7),  # From QT-BETA-0004
            (5, 0,  34999.80, "confirmed",  0),  # From QT-BETA-0006
            (6, 1,   9999.85, "confirmed",  3),  # STC — new order
            (7, 2,  14499.90, "draft",      1),  # Aldar — pending
        ]
        orders = []
        for i, (ci2, wi, subtotal, status, days_back) in enumerate(order_scenarios):
            code = f"SO-BETA-{i + 1:04d}"
            o = db.query(SalesOrder).filter(
                SalesOrder.company_id == cid, SalesOrder.code == code
            ).first()
            if not o:
                odate = today - timedelta(days=days_back)
                tax = round(subtotal * 0.15, 2)
                disc = 0.00
                o = SalesOrder(
                    company_id=cid,
                    customer_id=customers[ci2].id,
                    warehouse_id=warehouses[wi].id,
                    code=code,
                    order_date=odate,
                    status=status,
                    subtotal_amount=subtotal,
                    tax_amount=tax,
                    discount_amount=disc,
                    total_amount=subtotal + tax,
                    payment_status="pending",
                    note=f"Beta demo order #{i + 1}",
                )
                db.add(o)
                db.flush()
            orders.append(o)
        print(f"   ✓ {len(orders)} orders seeded")
        db.flush()

        # ── Sales Invoices ────────────────────────────────────────────────
        print("\n▶  Sales Invoices")
        invoice_scenarios = [
            (0, 0, 18999.90, "issued",  4, 30),
            (2, 0,  4999.95, "paid",    7, 30),
            (4, 1,  9999.85, "issued",  3, 30),
        ]
        invoices = []
        for i, (oi, wi, subtotal, status, days_back, due_days) in enumerate(invoice_scenarios):
            code = f"INV-BETA-{i + 1:04d}"
            inv = db.query(SalesInvoice).filter(
                SalesInvoice.company_id == cid, SalesInvoice.code == code
            ).first()
            if not inv:
                idate = today - timedelta(days=days_back)
                tax = round(subtotal * 0.15, 2)
                inv = SalesInvoice(
                    company_id=cid,
                    customer_id=orders[oi].customer_id,
                    order_id=orders[oi].id,
                    warehouse_id=warehouses[wi].id,
                    code=code,
                    invoice_date=idate,
                    due_date=idate + timedelta(days=due_days),
                    status=status,
                    subtotal_amount=subtotal,
                    tax_amount=tax,
                    discount_amount=0.00,
                    total_amount=subtotal + tax,
                    payment_status="pending" if status == "issued" else "paid",
                    note=f"Beta demo invoice #{i + 1}",
                )
                db.add(inv)
                db.flush()
            invoices.append(inv)
        print(f"   ✓ {len(invoices)} invoices seeded")
        db.flush()

        # ── Stock Movements ───────────────────────────────────────────────
        print("\n▶  Stock Movements")
        movement_data = [
            (0, 0, 50,  "purchase",  0),   # Dell Latitude received
            (1, 0, 30,  "purchase",  1),   # MacBook Air received
            (2, 0, 40,  "purchase",  0),   # iPad Pro
            (3, 0, 60,  "purchase",  1),   # iPhone 15
            (4, 0, 80,  "purchase",  2),   # Samsung S24
            (5, 1, 25,  "purchase",  2),   # Cisco Router
            (6, 1, 50,  "purchase",  3),   # Ubiquiti
            (7, 0, 15,  "purchase",  0),   # HP Printer
            (0, 0, -10, "sale",      0),   # Laptops sold
            (1, 0, -8,  "sale",      1),   # MacBooks sold
            (3, 0, -15, "sale",      0),   # Phones sold
            (12, 1, 200, "purchase", 4),   # USB cables bulk
            (13, 1, 30,  "purchase", 2),   # Cat6 cables
        ]
        movement_count = 0
        existing_movements = db.query(StockMovement).filter(
            StockMovement.company_id == cid
        ).count()
        if existing_movements == 0:
            for pi, wi, qty, mtype, si in movement_data:
                m = StockMovement(
                    company_id=cid,
                    product_id=products[pi].id,
                    warehouse_id=warehouses[wi].id,
                    quantity=qty,
                    movement_type=mtype,
                    reference_type="supplier" if mtype == "purchase" else "order",
                    reference_id=suppliers[si].id,
                    movement_date=today - timedelta(days=abs(pi % 7)),
                    note=f"Beta stock movement — {mtype}",
                )
                db.add(m)
                movement_count += 1
            db.flush()
        print(f"   ✓ {movement_count or existing_movements} stock movements seeded")

        db.commit()

        # ── Summary ──────────────────────────────────────────────────────
        print("\n" + "=" * 65)
        print("  ✅  BETA DEMO DATABASE READY")
        print("=" * 65)
        print(f"""
  Company:    Gulf Electronics & Trading Ltd
  Slug:       beta-gulf-trading
  Company ID: {cid}

  ┌──────────────────────────────────────────────────────────┐
  │              DEMO USER CREDENTIALS                       │
  ├────────────────────────┬─────────────────────────────────┤
  │ Email                  │ Password          │ Role        │
  ├────────────────────────┼───────────────────┼─────────────┤
  │ admin@gulf-trading.demo│ BetaAdmin2026!    │ Admin       │
  │ sales@gulf-trading.demo│ BetaSales2026!    │ Sales Mgr   │
  │ inv.@gulf-trading.demo │ BetaInventory2026!│ Inv. Mgr    │
  │ acct@gulf-trading.demo │ BetaAccount2026!  │ Accountant  │
  └────────────────────────┴───────────────────┴─────────────┘

  Data Summary:
    Branches:    {len(branches)}
    Warehouses:  {len(warehouses)}
    Customers:   {len(customers)}
    Suppliers:   {len(suppliers)}
    Products:    {len(products)}
    Quotations:  {len(quotations)}
    Orders:      {len(orders)}
    Invoices:    {len(invoices)}

  Access:
    Frontend: http://localhost:3000
    API Docs: http://localhost:8000/docs
""")
    except Exception as exc:
        db.rollback()
        print(f"\n  ❌  Seeding failed: {exc}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_beta_data()

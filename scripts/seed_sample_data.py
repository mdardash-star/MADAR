#!/usr/bin/env python3
"""
MADAR Sample Data Seeder
=========================

This script creates sample data for demo and testing purposes.
Run this after the application starts to populate the database with realistic data.

Usage:
    python scripts/seed_sample_data.py
    
Or from Docker:
    docker compose exec api python scripts/seed_sample_data.py
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "apps" / "api"))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.company import Company
from app.models.user import User
from app.models.branch import Branch
from app.models.warehouse import Warehouse
from app.models.customer import Customer
from app.models.supplier import Supplier
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.unit_of_measure import UnitOfMeasure
from app.models.sales_quotation import SalesQuotation
from app.models.sales_order import SalesOrder
from app.models.sales_invoice import SalesInvoice
from app.models.stock_movement import StockMovement
from app.models.role import Role
from app.models.permission import Permission
from app.core.security import get_password_hash
from app.services.seed_service import SeedService


def seed_sample_data():
    """Create sample data for demonstration"""
    db = SessionLocal()
    
    try:
        print("🌱 Starting MADAR Sample Data Seeding...")
        
        # Step 1: Create Company
        print("\n📋 Creating Demo Company...")
        demo_company = db.query(Company).filter(
            Company.slug == "demo-acme"
        ).first()
        
        if not demo_company:
            demo_company = Company(
                name="ACME Corporation",
                slug="demo-acme",
                legal_name="ACME Corporation Inc.",
                email="contact@acme-demo.com",
                phone="+1-555-0123",
                country="USA",
                city="New York",
            )
            db.add(demo_company)
            db.flush()
            print(f"   ✓ Company created: {demo_company.name} (ID: {demo_company.id})")
        else:
            print(f"   ℹ Company already exists: {demo_company.name} (ID: {demo_company.id})")
        
        company_id = demo_company.id
        
        # Step 2: Seed permissions and roles
        print("\n🔐 Setting up Roles and Permissions...")
        SeedService.seed_initial_permissions(db)
        admin_role = SeedService.seed_initial_roles(db, company_id)
        print(f"   ✓ Admin role configured with permissions")
        
        # Step 3: Create Admin User
        print("\n👤 Creating Demo Admin User...")
        admin_user = db.query(User).filter(
            User.company_id == company_id,
            User.email == "admin@acme-demo.com"
        ).first()
        
        if not admin_user:
            admin_user = User(
                company_id=company_id,
                email="admin@acme-demo.com",
                full_name="System Administrator",
                hashed_password=get_password_hash("Demo123!"),
                is_active=True,
                role_id=admin_role.id,
            )
            db.add(admin_user)
            db.flush()
            print(f"   ✓ Admin user created")
            print(f"   📧 Email: admin@acme-demo.com")
            print(f"   🔑 Password: Demo123!")
        else:
            print(f"   ℹ Admin user already exists")
        
        # Step 4: Create Branches
        print("\n🏢 Creating Branches...")
        branches_data = [
            {"name": "Headquarters", "code": "HQ-NYC", "country": "USA", "city": "New York", "timezone": "America/New_York"},
            {"name": "West Coast Hub", "code": "WC-LAX", "country": "USA", "city": "Los Angeles", "timezone": "America/Los_Angeles"},
            {"name": "East Coast Warehouse", "code": "EC-BOS", "country": "USA", "city": "Boston", "timezone": "America/New_York"},
        ]
        
        branches = []
        for branch_data in branches_data:
            existing = db.query(Branch).filter(
                Branch.company_id == company_id,
                Branch.code == branch_data["code"]
            ).first()
            
            if not existing:
                branch = Branch(company_id=company_id, **branch_data, is_active=True)
                db.add(branch)
                db.flush()
                branches.append(branch)
                print(f"   ✓ {branch.name} ({branch.code})")
            else:
                branches.append(existing)
        
        # Step 5: Create Warehouses
        print("\n🏭 Creating Warehouses...")
        warehouse_data = [
            {"name": "Main Warehouse", "code": "WH-001", "location": "Brooklyn", "branch_id": branches[0].id},
            {"name": "Distribution Center", "code": "WH-002", "location": "Pasadena", "branch_id": branches[1].id},
            {"name": "Regional Storage", "code": "WH-003", "location": "Quincy", "branch_id": branches[2].id},
        ]
        
        warehouses = []
        for wh_data in warehouse_data:
            existing = db.query(Warehouse).filter(
                Warehouse.company_id == company_id,
                Warehouse.code == wh_data["code"]
            ).first()
            
            if not existing:
                warehouse = Warehouse(company_id=company_id, **wh_data)
                db.add(warehouse)
                db.flush()
                warehouses.append(warehouse)
                print(f"   ✓ {warehouse.name} ({warehouse.code}) - {wh_data['location']}")
            else:
                warehouses.append(existing)
        
        # Step 6: Create Customers
        print("\n👥 Creating Customers...")
        customers_data = [
            {"name": "ABC Trading Corp", "code": "CUST-001", "email": "sales@abctrading.com", "phone": "+1-555-1001"},
            {"name": "Global Imports LLC", "code": "CUST-002", "email": "info@globalimports.com", "phone": "+1-555-1002"},
            {"name": "Pacific Distributors", "code": "CUST-003", "email": "orders@pacificdist.com", "phone": "+1-555-1003"},
            {"name": "Northeast Retailers", "code": "CUST-004", "email": "purchasing@nretailers.com", "phone": "+1-555-1004"},
        ]
        
        customers = []
        for cust_data in customers_data:
            existing = db.query(Customer).filter(
                Customer.company_id == company_id,
                Customer.code == cust_data["code"]
            ).first()
            
            if not existing:
                customer = Customer(company_id=company_id, **cust_data)
                db.add(customer)
                db.flush()
                customers.append(customer)
                print(f"   ✓ {customer.name}")
            else:
                customers.append(existing)
        
        # Step 7: Create Suppliers
        print("\n🤝 Creating Suppliers...")
        suppliers_data = [
            {"name": "Global Supplies Inc", "code": "SUP-001", "email": "sales@globalsupplies.com", "phone": "+1-555-2001"},
            {"name": "Premium Components Ltd", "code": "SUP-002", "email": "orders@premiumcomp.com", "phone": "+1-555-2002"},
            {"name": "FastShip Logistics", "code": "SUP-003", "email": "logistics@fastship.com", "phone": "+1-555-2003"},
        ]
        
        suppliers = []
        for sup_data in suppliers_data:
            existing = db.query(Supplier).filter(
                Supplier.company_id == company_id,
                Supplier.code == sup_data["code"]
            ).first()
            
            if not existing:
                supplier = Supplier(company_id=company_id, **sup_data)
                db.add(supplier)
                db.flush()
                suppliers.append(supplier)
                print(f"   ✓ {supplier.name}")
            else:
                suppliers.append(existing)
        
        # Step 8: Create Product Categories
        print("\n📦 Creating Product Categories...")
        categories_data = [
            {"name": "Electronics", "code": "ELEC", "description": "Electronic equipment and devices"},
            {"name": "Machinery", "code": "MACH", "description": "Industrial machinery and equipment"},
            {"name": "Raw Materials", "code": "RAW", "description": "Raw materials for manufacturing"},
            {"name": "Consumables", "code": "CONS", "description": "Consumable items and supplies"},
        ]
        
        categories = []
        for cat_data in categories_data:
            existing = db.query(ProductCategory).filter(
                ProductCategory.company_id == company_id,
                ProductCategory.code == cat_data["code"]
            ).first()
            
            if not existing:
                category = ProductCategory(company_id=company_id, **cat_data)
                db.add(category)
                db.flush()
                categories.append(category)
                print(f"   ✓ {category.name}")
            else:
                categories.append(existing)
        
        # Step 9: Create Units of Measure
        print("\n📐 Creating Units of Measure...")
        uom_data = [
            {"name": "Piece", "code": "PCS", "abbreviation": "pc"},
            {"name": "Box", "code": "BOX", "abbreviation": "bx"},
            {"name": "Carton", "code": "CTN", "abbreviation": "ctn"},
            {"name": "Kilogram", "code": "KG", "abbreviation": "kg"},
            {"name": "Liter", "code": "LTR", "abbreviation": "L"},
        ]
        
        uoms = []
        for uom_item in uom_data:
            existing = db.query(UnitOfMeasure).filter(
                UnitOfMeasure.company_id == company_id,
                UnitOfMeasure.code == uom_item["code"]
            ).first()
            
            if not existing:
                uom = UnitOfMeasure(company_id=company_id, **uom_item)
                db.add(uom)
                db.flush()
                uoms.append(uom)
                print(f"   ✓ {uom.name}")
            else:
                uoms.append(existing)
        
        # Step 10: Create Products
        print("\n🛍️ Creating Sample Products...")
        products_data = [
            {"name": "Laptop Pro 15", "sku": "LAP-001", "selling_price": 1299.99, "cost_price": 800.00, "category_id": categories[0].id, "uom_id": uoms[0].id},
            {"name": "Desktop PC", "sku": "DTP-001", "selling_price": 899.99, "cost_price": 550.00, "category_id": categories[0].id, "uom_id": uoms[0].id},
            {"name": "Industrial Printer", "sku": "PRT-001", "selling_price": 2499.99, "cost_price": 1500.00, "category_id": categories[1].id, "uom_id": uoms[0].id},
            {"name": "Steel Bars (100kg)", "sku": "STL-001", "selling_price": 150.00, "cost_price": 100.00, "category_id": categories[2].id, "uom_id": uoms[3].id},
            {"name": "Adhesive Tape", "sku": "TAP-001", "selling_price": 25.00, "cost_price": 15.00, "category_id": categories[3].id, "uom_id": uoms[1].id},
        ]
        
        products = []
        for prod_data in products_data:
            existing = db.query(Product).filter(
                Product.company_id == company_id,
                Product.sku == prod_data["sku"]
            ).first()
            
            if not existing:
                product = Product(
                    company_id=company_id,
                    name=prod_data["name"],
                    sku=prod_data["sku"],
                    selling_price=prod_data["selling_price"],
                    cost_price=prod_data["cost_price"],
                    category_id=prod_data["category_id"],
                    unit_of_measure_id=prod_data["uom_id"],
                )
                db.add(product)
                db.flush()
                products.append(product)
                print(f"   ✓ {product.name} (SKU: {product.sku})")
            else:
                products.append(existing)
        
        # Step 11: Create Quotations
        print("\n💰 Creating Sample Quotations...")
        quotations = []
        for i, customer in enumerate(customers[:2]):
            existing = db.query(SalesQuotation).filter(
                SalesQuotation.company_id == company_id,
                SalesQuotation.quotation_number == f"QT-{company_id:03d}-{i+1:04d}"
            ).first()
            
            if not existing:
                quotation = SalesQuotation(
                    company_id=company_id,
                    customer_id=customer.id,
                    code=f"QT-{company_id:03d}-{i+1:04d}",
                    quotation_number=f"QT-{company_id:03d}-{i+1:04d}",
                    quotation_date=datetime.now().date(),
                    expiry_date=(datetime.now() + timedelta(days=30)).date(),
                    subtotal_amount=5000.00 + (i * 1000),
                    tax_amount=1000.00 + (i * 200),
                    discount_amount=0.00,
                    total_amount=6000.00 + (i * 1200),
                    warehouse_id=warehouses[i % len(warehouses)].id,
                    status="sent" if i == 0 else "draft",
                )
                db.add(quotation)
                db.flush()
                quotations.append(quotation)
                print(f"   ✓ QT-{company_id:03d}-{i+1:04d} for {customer.name}")
            else:
                quotations.append(existing)
        
        # Step 12: Create Sales Orders
        print("\n📋 Creating Sample Sales Orders...")
        orders = []
        for i, customer in enumerate(customers[:2]):
            existing = db.query(SalesOrder).filter(
                SalesOrder.company_id == company_id,
                SalesOrder.order_number == f"SO-{company_id:03d}-{i+1:04d}"
            ).first()
            
            if not existing:
                order = SalesOrder(
                    company_id=company_id,
                    customer_id=customer.id,
                    code=f"SO-{company_id:03d}-{i+1:04d}",
                    order_number=f"SO-{company_id:03d}-{i+1:04d}",
                    order_date=datetime.now().date(),
                    subtotal_amount=4500.00 + (i * 1000),
                    tax_amount=900.00 + (i * 200),
                    discount_amount=100.00,
                    total_amount=5300.00 + (i * 1200),
                    warehouse_id=warehouses[i % len(warehouses)].id,
                    status="confirmed",
                )
                db.add(order)
                db.flush()
                orders.append(order)
                print(f"   ✓ SO-{company_id:03d}-{i+1:04d} for {customer.name}")
            else:
                orders.append(existing)
        
        # Step 13: Create Invoices
        print("\n📄 Creating Sample Invoices...")
        for i, order in enumerate(orders[:1]):
            existing = db.query(SalesInvoice).filter(
                SalesInvoice.company_id == company_id,
                SalesInvoice.invoice_number == f"INV-{company_id:03d}-{i+1:04d}"
            ).first()
            
            if not existing:
                invoice = SalesInvoice(
                    company_id=company_id,
                    customer_id=order.customer_id,
                    code=f"INV-{company_id:03d}-{i+1:04d}",
                    invoice_number=f"INV-{company_id:03d}-{i+1:04d}",
                    invoice_date=datetime.now().date(),
                    subtotal_amount=order.subtotal_amount,
                    tax_amount=order.tax_amount,
                    discount_amount=order.discount_amount,
                    total_amount=order.total_amount,
                    order_id=order.id,
                    warehouse_id=order.warehouse_id,
                    status="issued",
                    due_date=(datetime.now() + timedelta(days=30)).date(),
                )
                db.add(invoice)
                db.flush()
                print(f"   ✓ INV-{company_id:03d}-{i+1:04d} for {order.customer.name}")
        
        # Step 14: Create Stock Movements
        print("\n📊 Creating Stock Movements...")
        for i, product in enumerate(products[:3]):
            movement = StockMovement(
                company_id=company_id,
                product_id=product.id,
                warehouse_id=warehouses[i % len(warehouses)].id,
                quantity=10 + (i * 5),
                movement_type="purchase",
                reference_type="supplier_order",
                reference_id=suppliers[i % len(suppliers)].id,
            )
            db.add(movement)
        
        db.commit()
        print(f"   ✓ Stock movements recorded")
        
        print("\n" + "=" * 60)
        print("✅ SAMPLE DATA SEEDING COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"   Company: {demo_company.name}")
        print(f"   Branches: {len(branches)}")
        print(f"   Warehouses: {len(warehouses)}")
        print(f"   Customers: {len(customers)}")
        print(f"   Suppliers: {len(suppliers)}")
        print(f"   Products: {len(products)}")
        print(f"   Quotations: {len(quotations)}")
        print(f"   Orders: {len(orders)}")
        print(f"\n🔐 Demo Credentials:")
        print(f"   Email: admin@acme-demo.com")
        print(f"   Password: Demo123!")
        print(f"\n🌐 Access the application:")
        print(f"   Frontend: http://localhost:3000")
        print(f"   API Docs: http://localhost:8000/docs")
        print()
        
    except Exception as e:
        print(f"\n❌ Error seeding data: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_sample_data()

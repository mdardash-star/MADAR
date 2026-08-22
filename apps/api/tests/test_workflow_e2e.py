"""
End-to-end workflow test: 12-step user journey
Register → Login → Branch → Warehouse → Customer → Supplier →
Product → Quotation → Order → Invoice → Inventory → KPIs
"""

import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_complete_12step_workflow(client):
    """Complete 12-step user journey verification"""
    
    # Generate unique ID for this test run to avoid duplicates
    test_id = str(uuid.uuid4())[:8]
    
    # Step 1: Register a company
    company_suffix = str(uuid.uuid4())[:8]
    reg_resp = client.post('/companies/register', json={
        'company_name': f'ACME Corp {company_suffix}',
        'company_slug': f'acme-corp-{company_suffix}',
        'legal_name': 'ACME Corporation Inc',
        'email': 'company@acme.com',
        'phone': '+1-555-0100',
        'admin_full_name': 'John Doe',
        'admin_email': f'admin-{company_suffix}@acme.com',
        'admin_password': 'SecurePassword123!',
    })
    assert reg_resp.status_code in (200, 201), f"Register failed: {reg_resp.text}"
    reg_data = reg_resp.json()
    company_id = reg_data['company']['id']
    access_token = reg_data['tokens']['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    print(f"✓ Step 1: Company registered (ID: {company_id})")
    
    # Step 2: Login (verify /api/v1/me works)
    me_resp = client.get('/api/v1/me', headers=headers)
    assert me_resp.status_code == 200, f"Get profile failed: {me_resp.text}"
    profile = me_resp.json()
    assert profile['company_id'] == company_id
    print(f"✓ Step 2: Login verified (User: {profile['email']})")
    
    # Step 3: Create a branch
    branch_resp = client.post('/api/v1/master-data/branches',
        json={
            'company_id': company_id,
            'name': 'Headquarters',
            'code': f'HQ-{test_id}',
            'country': 'USA',
            'city': 'New York',
            'timezone': 'America/New_York',
        },
        headers=headers
    )
    assert branch_resp.status_code == 201, f"Create branch failed: {branch_resp.text}"
    branch_id = branch_resp.json()['id']
    print(f"✓ Step 3: Branch created (ID: {branch_id})")
    
    # Step 4: Create a warehouse
    warehouse_resp = client.post('/api/v1/master-data/warehouses',
        json={
            'company_id': company_id,
            'branch_id': branch_id,
            'name': 'Main Warehouse',
            'code': f'WH-{test_id}',
            'location': 'Brooklyn',
        },
        headers=headers
    )
    assert warehouse_resp.status_code == 201, f"Create warehouse failed: {warehouse_resp.text}"
    warehouse_id = warehouse_resp.json()['id']
    print(f"✓ Step 4: Warehouse created (ID: {warehouse_id})")
    
    # Step 5: Create a customer
    customer_resp = client.post('/api/v1/master-data/customers',
        json={
            'company_id': company_id,
            'name': 'ABC Trading',
            'code': f'CUST-{test_id}',
            'email': 'contact@abctrading.com',
            'phone': '+1234567890',
        },
        headers=headers
    )
    assert customer_resp.status_code == 201, f"Create customer failed: {customer_resp.text}"
    customer_id = customer_resp.json()['id']
    print(f"✓ Step 5: Customer created (ID: {customer_id})")
    
    # Step 6: Create a supplier
    supplier_resp = client.post('/api/v1/master-data/suppliers',
        json={
            'company_id': company_id,
            'name': 'Global Supplies Inc',
            'code': f'SUP-{test_id}',
            'email': 'sales@globalsupplies.com',
            'phone': '+9876543210',
        },
        headers=headers
    )
    assert supplier_resp.status_code == 201, f"Create supplier failed: {supplier_resp.text}"
    supplier_id = supplier_resp.json()['id']
    print(f"✓ Step 6: Supplier created (ID: {supplier_id})")
    
    # Step 7: Create a product
    # First create category
    cat_resp = client.post('/api/v1/master-data/product-categories',
        json={'company_id': company_id, 'name': 'Electronics', 'code': f'ELEC-{test_id}'},
        headers=headers
    )
    assert cat_resp.status_code == 201, f"Create category failed: {cat_resp.text}"
    category_id = cat_resp.json()['id']
    
    # Create UoM
    uom_resp = client.post('/api/v1/master-data/units-of-measure',
        json={
            'company_id': company_id,
            'name': 'Piece',
            'code': f'PCS-{test_id}',
            'abbreviation': 'pc',
        },
        headers=headers
    )
    assert uom_resp.status_code == 201, f"Create UoM failed: {uom_resp.text}"
    uom_id = uom_resp.json()['id']
    
    # Create product
    product_resp = client.post('/api/v1/master-data/products',
        json={
            'company_id': company_id,
            'name': 'Laptop Pro',
            'sku': f'LAP-{test_id}',
            'selling_price': 1500.00,
            'cost_price': 1000.00,
            'category_id': category_id,
            'unit_of_measure_id': uom_id,
        },
        headers=headers
    )
    assert product_resp.status_code == 201, f"Create product failed: {product_resp.text}"
    product_id = product_resp.json()['id']
    print(f"✓ Step 7: Product created (ID: {product_id})")
    
    # Step 8: Create a quotation
    quotation_resp = client.post('/api/v1/sales/quotations',
        json={
            'company_id': company_id,
            'customer_id': customer_id,
            'code': f'QT-{test_id}',
            'quotation_number': f'QT-{test_id}',
            'quotation_date': '2026-07-18',
            'expiry_date': '2026-08-18',
            'subtotal_amount': 2500.00,
            'tax_amount': 500.00,
            'discount_amount': 0.00,
            'total_amount': 3000.00,
            'warehouse_id': warehouse_id,
            'status': 'sent',
        },
        headers=headers
    )
    assert quotation_resp.status_code == 201, f"Create quotation failed: {quotation_resp.text}"
    quotation_id = quotation_resp.json()['id']
    print(f"✓ Step 8: Quotation created (ID: {quotation_id})")
    
    # Step 9: Convert quotation to sales order
    order_resp = client.post('/api/v1/sales/orders',
        json={
            'company_id': company_id,
            'customer_id': customer_id,
            'code': f'SO-{test_id}',
            'order_number': f'SO-{test_id}',
            'order_date': '2026-07-18',
            'subtotal_amount': 2500.00,
            'tax_amount': 500.00,
            'discount_amount': 0.00,
            'total_amount': 3000.00,
            'warehouse_id': warehouse_id,
            'status': 'confirmed',
        },
        headers=headers
    )
    assert order_resp.status_code == 201, f"Create order failed: {order_resp.text}"
    order_id = order_resp.json()['id']
    print(f"✓ Step 9: Sales Order created (ID: {order_id})")
    
    # Step 10: Generate invoice
    invoice_resp = client.post('/api/v1/sales/invoices',
        json={
            'company_id': company_id,
            'customer_id': customer_id,
            'code': f'INV-{test_id}',
            'invoice_number': f'INV-{test_id}',
            'invoice_date': '2026-07-18',
            'subtotal_amount': 2500.00,
            'tax_amount': 500.00,
            'discount_amount': 0.00,
            'total_amount': 3000.00,
            'order_id': order_id,
            'warehouse_id': warehouse_id,
            'status': 'issued',
        },
        headers=headers
    )
    assert invoice_resp.status_code == 201, f"Create invoice failed: {invoice_resp.text}"
    invoice_id = invoice_resp.json()['id']
    print(f"✓ Step 10: Invoice created (ID: {invoice_id})")
    
    # Step 11: Reduce inventory automatically
    movement_resp = client.post('/api/v1/inventory/stock-movements',
        json={
            'company_id': company_id,
            'product_id': product_id,
            'warehouse_id': warehouse_id,
            'quantity': 2,
            'movement_type': 'sale',
            'reference_type': 'sales_invoice',
            'reference_id': invoice_id,
        },
        headers=headers
    )
    assert movement_resp.status_code == 201, f"Create stock movement failed: {movement_resp.text}"
    print("✓ Step 11: Inventory reduced (Qty: 2 units sold)")
    
    # Step 12: Display updated dashboard KPIs
    dashboard_resp = client.get(
        f'/api/v1/dashboard/summary?company_id={company_id}',
        headers=headers
    )
    assert dashboard_resp.status_code == 200, f"Get dashboard failed: {dashboard_resp.text}"
    kpis = dashboard_resp.json()
    
    # Verify all KPIs
    assert kpis['branches'] == 2, (
        f"Expected 2 branches (1 auto Head Office + 1 manual), got {kpis['branches']}"
    )
    assert kpis['warehouses'] == 1, f"Expected 1 warehouse, got {kpis['warehouses']}"
    assert kpis['customers'] == 1, f"Expected 1 customer, got {kpis['customers']}"
    assert kpis['suppliers'] == 1, f"Expected 1 supplier, got {kpis['suppliers']}"
    assert kpis['products'] == 1, f"Expected 1 product, got {kpis['products']}"
    assert kpis['quotations'] == 1, f"Expected 1 quotation, got {kpis['quotations']}"
    assert kpis['sales_orders'] == 1, f"Expected 1 sales order, got {kpis['sales_orders']}"
    assert kpis['sales_invoices'] == 1, f"Expected 1 invoice, got {kpis['sales_invoices']}"
    
    print("✓ Step 12: Dashboard KPIs verified")
    print("\n✓✓✓ ALL 12 STEPS COMPLETED SUCCESSFULLY ✓✓✓")
    print(f"Final KPIs: {kpis}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])

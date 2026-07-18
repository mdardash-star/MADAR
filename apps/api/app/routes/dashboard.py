from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.branch import Branch
from app.models.crm_lead import CrmLead
from app.models.customer import Customer
from app.models.product import Product
from app.models.sales_invoice import SalesInvoice
from app.models.sales_order import SalesOrder
from app.models.sales_quotation import SalesQuotation
from app.models.supplier import Supplier
from app.models.warehouse import Warehouse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary(
    company_id: int = Query(...),
    db: Session = Depends(get_db),
) -> dict:
    """Return key KPI counts for the authenticated company dashboard."""
    branches = db.query(Branch).filter(
        Branch.company_id == company_id, Branch.is_deleted.is_(False)
    ).count()

    warehouses = db.query(Warehouse).filter(
        Warehouse.company_id == company_id, Warehouse.is_deleted.is_(False)
    ).count()

    customers = db.query(Customer).filter(
        Customer.company_id == company_id, Customer.is_deleted.is_(False)
    ).count()

    suppliers = db.query(Supplier).filter(
        Supplier.company_id == company_id, Supplier.is_deleted.is_(False)
    ).count()

    products = db.query(Product).filter(
        Product.company_id == company_id, Product.is_deleted.is_(False)
    ).count()

    quotations = db.query(SalesQuotation).filter(
        SalesQuotation.company_id == company_id, SalesQuotation.is_deleted.is_(False)
    ).count()

    orders = db.query(SalesOrder).filter(
        SalesOrder.company_id == company_id, SalesOrder.is_deleted.is_(False)
    ).count()

    invoices = db.query(SalesInvoice).filter(
        SalesInvoice.company_id == company_id, SalesInvoice.is_deleted.is_(False)
    ).count()

    leads = db.query(CrmLead).filter(
        CrmLead.company_id == company_id, CrmLead.is_deleted.is_(False)
    ).count()

    return {
        "branches": branches,
        "warehouses": warehouses,
        "customers": customers,
        "suppliers": suppliers,
        "products": products,
        "quotations": quotations,
        "sales_orders": orders,
        "sales_invoices": invoices,
        "crm_leads": leads,
    }

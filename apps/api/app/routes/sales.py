from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.sales import (
    SalesInvoiceCreateRequest,
    SalesInvoiceUpdateRequest,
    SalesOrderCreateRequest,
    SalesOrderUpdateRequest,
    SalesQuotationCreateRequest,
    SalesQuotationUpdateRequest,
)
from app.services.sales_service import SalesService

router = APIRouter(prefix="/sales", tags=["sales"])


def _serialize(instance: Any) -> dict[str, Any]:
    return {key: value for key, value in instance.__dict__.items() if key != "_sa_instance_state"}


@router.get("/quotations")
def list_quotations(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in SalesService.list_quotations(db, company_id, skip, limit, search)]


@router.post("/quotations", status_code=status.HTTP_201_CREATED)
def create_quotation(payload: SalesQuotationCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(SalesService.create_quotation(db, payload.model_dump()))


@router.put("/quotations/{quotation_id}")
def update_quotation(quotation_id: int, payload: SalesQuotationUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = SalesService.update_quotation(db, quotation_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quotation not found")
    return _serialize(item)


@router.delete("/quotations/{quotation_id}")
def delete_quotation(quotation_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = SalesService.delete_quotation(db, quotation_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quotation not found")
    return {"status": "deleted", "id": str(quotation_id)}


@router.get("/orders")
def list_orders(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in SalesService.list_orders(db, company_id, skip, limit, search)]


@router.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(payload: SalesOrderCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(SalesService.create_order(db, payload.model_dump()))


@router.put("/orders/{order_id}")
def update_order(order_id: int, payload: SalesOrderUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = SalesService.update_order(db, order_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return _serialize(item)


@router.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = SalesService.delete_order(db, order_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {"status": "deleted", "id": str(order_id)}


@router.get("/invoices")
def list_invoices(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in SalesService.list_invoices(db, company_id, skip, limit, search)]


@router.post("/invoices", status_code=status.HTTP_201_CREATED)
def create_invoice(payload: SalesInvoiceCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(SalesService.create_invoice(db, payload.model_dump()))


@router.put("/invoices/{invoice_id}")
def update_invoice(invoice_id: int, payload: SalesInvoiceUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = SalesService.update_invoice(db, invoice_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return _serialize(item)


@router.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = SalesService.delete_invoice(db, invoice_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return {"status": "deleted", "id": str(invoice_id)}

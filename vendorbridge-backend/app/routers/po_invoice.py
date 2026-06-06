import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import po_invoice as po_invoice_crud
from app.database import get_db
from app.schemas.invoice import InvoiceCreate, InvoiceEmailRequest, InvoiceEmailResponse, InvoiceRead, InvoiceStatusUpdate
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderRead, PurchaseOrderStatusUpdate
from app.utils.email import send_email_with_attachment
from app.utils.pdf import generate_invoice_pdf

purchase_order_router = APIRouter(prefix="/purchase-orders", tags=["Purchase Orders"])
invoice_router = APIRouter(prefix="/invoices", tags=["Invoices"])


@purchase_order_router.post("/", response_model=PurchaseOrderRead, status_code=status.HTTP_201_CREATED)
async def create_purchase_order(payload: PurchaseOrderCreate, db: AsyncSession = Depends(get_db)):
    return await po_invoice_crud.create_purchase_order(db, payload.rfq_id, payload.quotation_id)


@purchase_order_router.get("/{po_id}", response_model=PurchaseOrderRead)
async def get_purchase_order(po_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    purchase_order = await po_invoice_crud.get_purchase_order(db, po_id)
    if purchase_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
    return purchase_order


@purchase_order_router.patch("/{po_id}/status", response_model=PurchaseOrderRead)
async def update_purchase_order_status(po_id: uuid.UUID, payload: PurchaseOrderStatusUpdate, db: AsyncSession = Depends(get_db)):
    purchase_order = await po_invoice_crud.update_purchase_order_status(db, po_id, payload.status)
    if purchase_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
    return purchase_order


@invoice_router.post("/", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
async def create_invoice(payload: InvoiceCreate, db: AsyncSession = Depends(get_db)):
    return await po_invoice_crud.create_invoice(db, payload.po_id)


@invoice_router.get("/{invoice_id}", response_model=InvoiceRead)
async def get_invoice(invoice_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    invoice = await po_invoice_crud.get_invoice(db, invoice_id)
    if invoice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoice


@invoice_router.get("/{invoice_id}/pdf")
async def get_invoice_pdf(invoice_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    invoice = await po_invoice_crud.get_invoice(db, invoice_id)
    if invoice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    pdf_path = generate_invoice_pdf(invoice)
    return FileResponse(path=pdf_path, filename=pdf_path.name, media_type="application/pdf")


@invoice_router.post("/{invoice_id}/email", response_model=InvoiceEmailResponse)
async def email_invoice(invoice_id: uuid.UUID, payload: InvoiceEmailRequest, db: AsyncSession = Depends(get_db)):
    invoice = await po_invoice_crud.get_invoice(db, invoice_id)
    if invoice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    pdf_path = generate_invoice_pdf(invoice)
    send_email_with_attachment(str(payload.recipient_email), payload.subject, payload.body, pdf_path)
    return {"success": True, "message": "Invoice sent successfully"}


@invoice_router.patch("/{invoice_id}/status", response_model=InvoiceRead)
async def update_invoice_status(invoice_id: uuid.UUID, payload: InvoiceStatusUpdate, db: AsyncSession = Depends(get_db)):
    invoice = await po_invoice_crud.update_invoice_status(db, invoice_id, payload.status)
    if invoice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoice

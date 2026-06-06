import tempfile
from pathlib import Path

from openpyxl import Workbook
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.invoice import Invoice
from app.models.purchase_order import PurchaseOrder


async def generate_procurement_export(db: AsyncSession) -> Path:
    workbook = Workbook()
    po_sheet = workbook.active
    po_sheet.title = "Purchase Orders"
    po_sheet.append(["PO Number", "PO ID", "RFQ ID", "Quotation ID", "Status", "Created At", "Subtotal", "Tax Amount", "Total Amount"])
    purchase_orders = (await db.execute(select(PurchaseOrder).options(selectinload(PurchaseOrder.items)).order_by(PurchaseOrder.created_at.desc()))).scalars().all()
    for po in purchase_orders:
        subtotal = sum(item.quantity * item.unit_price for item in po.items)
        tax_amount = sum(item.quantity * item.unit_price * item.tax_pct / 100 for item in po.items)
        po_sheet.append([po.po_number, str(po.id), str(po.rfq_id), str(po.quotation_id), po.status.value, po.created_at.isoformat(), subtotal, tax_amount, subtotal + tax_amount])
    invoice_sheet = workbook.create_sheet("Invoices")
    invoice_sheet.append(["Invoice Number", "Invoice ID", "PO ID", "Status", "Created At", "Subtotal", "Tax Amount", "Total Amount"])
    invoices = (await db.execute(select(Invoice).order_by(Invoice.created_at.desc()))).scalars().all()
    for invoice in invoices:
        invoice_sheet.append([invoice.invoice_number, str(invoice.id), str(invoice.po_id), invoice.status.value, invoice.created_at.isoformat(), invoice.subtotal, invoice.tax_amount, invoice.total_amount])
    for sheet in workbook.worksheets:
        for column_cells in sheet.columns:
            width = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
            sheet.column_dimensions[column_cells[0].column_letter].width = min(max(width + 2, 12), 45)
    path = Path(tempfile.gettempdir()) / "vendorbridge-procurement-export.xlsx"
    workbook.save(path)
    return path

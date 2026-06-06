import tempfile
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.models.invoice import Invoice


def generate_invoice_pdf(invoice: Invoice) -> Path:
    path = Path(tempfile.gettempdir()) / f"{invoice.invoice_number}.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=A4)
    styles = getSampleStyleSheet()
    vendor_id = invoice.purchase_order.quotation.vendor_id if invoice.purchase_order and invoice.purchase_order.quotation else "N/A"
    elements = [
        Paragraph("VendorBridge", styles["Title"]),
        Paragraph("Procurement & Vendor Management ERP", styles["Normal"]),
        Spacer(1, 18),
        Paragraph(f"Invoice Number: {invoice.invoice_number}", styles["Heading2"]),
        Paragraph(f"Date: {invoice.created_at:%Y-%m-%d}", styles["Normal"]),
        Paragraph(f"Vendor Reference: {vendor_id}", styles["Normal"]),
        Spacer(1, 18),
    ]
    table_data = [["Description", "Qty", "Unit Price", "Tax %", "Line Total"]]
    for item in invoice.items:
        table_data.append([
            item.description,
            f"{item.quantity:.2f}",
            f"{item.unit_price:.2f}",
            f"{item.tax_pct:.2f}",
            f"{item.line_total:.2f}",
        ])
    table = Table(table_data, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    elements.extend(
        [
            table,
            Spacer(1, 18),
            Paragraph(f"Subtotal: {invoice.subtotal:.2f}", styles["Normal"]),
            Paragraph(f"Tax Amount: {invoice.tax_amount:.2f}", styles["Normal"]),
            Paragraph(f"Grand Total: {invoice.total_amount:.2f}", styles["Heading2"]),
        ]
    )
    doc.build(elements)
    return path

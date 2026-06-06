# VendorBridge Backend

FastAPI backend for Procurement & Vendor Management workflows: RFQs, quotations, purchase orders, invoices, PDF/email delivery, and analytics.

## Setup

```bash
cd vendorbridge-backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Update `.env` with your PostgreSQL and SMTP credentials. The backend also reads a workspace-level `../.env`, so keeping `E:\VendorBridge\.env` is supported. The `users` and `vendors` tables must already exist because they are owned by another team.

## Run Migrations

```bash
alembic upgrade head
```

## Start Server

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive OpenAPI UI.

## API Endpoints

- `GET /health`
- `POST /rfqs/`
- `GET /rfqs/?status_filter=open&created_by={uuid}`
- `GET /rfqs/{rfq_id}`
- `PATCH /rfqs/{rfq_id}/status`
- `DELETE /rfqs/{rfq_id}`
- `POST /quotations/`
- `GET /quotations/{quotation_id}`
- `PATCH /quotations/{quotation_id}`
- `PATCH /quotations/{quotation_id}/submit`
- `GET /rfqs/{rfq_id}/quotations?sort_by=price&order=asc`
- `POST /purchase-orders/`
- `GET /purchase-orders/{po_id}`
- `PATCH /purchase-orders/{po_id}/status`
- `POST /invoices/`
- `GET /invoices/{invoice_id}`
- `GET /invoices/{invoice_id}/pdf`
- `POST /invoices/{invoice_id}/email`
- `PATCH /invoices/{invoice_id}/status`
- `GET /analytics/summary`
- `GET /analytics/monthly-trend`
- `GET /analytics/vendor-performance`
- `GET /analytics/export`

## Notes

- RFQ deletion is implemented as a soft delete by setting status to `cancelled`.
- Purchase orders can be generated only from quotations with status `accepted`.
- Vendor names are returned as UUID-based references because vendor profile data is managed outside this service.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import analytics_router, comparison_router, invoice_router, purchase_order_router, quotation_router, rfq_router

app = FastAPI(title="VendorBridge API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rfq_router)
app.include_router(comparison_router)
app.include_router(quotation_router)
app.include_router(purchase_order_router)
app.include_router(invoice_router)
app.include_router(analytics_router)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

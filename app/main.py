from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ShippingRequest, ShippingResponse, CourierRate
from app.services import delhivery, dtdc, bluedart, shiprocket

app = FastAPI(title="Courier Rate Comparator API")

# Allow Lovable domain to call your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://preview--courier-compass-43.lovable.app",  # your Lovable preview domain
        "https://courier-compass-43.lovable.app",            # published domain
        "https://lovable.app",
        "*"  # optional: allow all during testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/compare-rates", response_model=ShippingResponse)
def compare_rates(request: ShippingRequest):
    try:
        results = []

        for courier_func in [shiprocket.get_rate, delhivery.get_rate, dtdc.get_rate, bluedart.get_rate]:
            rate = courier_func(request)
            if rate:
                results.append(rate)

        if not results:
            raise HTTPException(status_code=404, detail="No rates found")

        # Sort by price
        sorted_results = sorted(results, key=lambda x: x.price)

        return ShippingResponse(
            origin=request.origin_pincode,
            destination=request.destination_pincode,
            results=sorted_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

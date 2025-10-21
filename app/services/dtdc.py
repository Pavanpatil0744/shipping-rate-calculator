from app.schemas import ShippingRequest, CourierRate

def get_rate(request: ShippingRequest) -> CourierRate:
    # Mock logic
    base_price = 100 + (request.weight * 15)
    return CourierRate(courier="DTDC", price=base_price, eta_days=3)

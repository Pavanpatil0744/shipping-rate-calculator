from app.schemas import ShippingRequest, CourierRate

def get_rate(request: ShippingRequest) -> CourierRate:
    # Mock logic
    base_price = 120 + (request.weight * 10)
    return CourierRate(courier="BlueDart", price=base_price, eta_days=2)

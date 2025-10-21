import requests
from app.schemas import ShippingRequest, CourierRate
from app.utils import get_env

BASE_URL = "https://apiv2.shiprocket.in/v1/external"

def authenticate():
    payload = {
        "email": get_env("SHIPROCKET_EMAIL"),
        "password": get_env("SHIPROCKET_PASSWORD")
    }
    resp = requests.post(f"{BASE_URL}/auth/login", json=payload)
    if resp.status_code != 200:
        raise Exception(f"Shiprocket auth failed: {resp.text}")
    return resp.json().get("token")

def get_rate(request: ShippingRequest) -> CourierRate:
    try:
        token = authenticate()
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "pickup_postcode": request.origin_pincode,
            "delivery_postcode": request.destination_pincode,
            "weight": request.weight,
            "cod": 0,
            "length": request.length,
            "breadth": request.width,
            "height": request.height
        }

        resp = requests.post(f"{BASE_URL}/courier/serviceability", headers=headers, json=payload)
        data = resp.json()

        if not data.get("data") or not data["data"].get("available_courier_companies"):
            return CourierRate(courier="Shiprocket", price=0, remarks="No serviceable couriers found")

        best_courier = min(
            data["data"]["available_courier_companies"], key=lambda x: x["rate"]
        )

        return CourierRate(
            courier=f"Shiprocket ({best_courier['courier_name']})",
            price=best_courier["rate"],
            eta_days=best_courier.get("etd"),
        )

    except Exception as e:
        return CourierRate(courier="Shiprocket", price=0, remarks=f"Error: {str(e)}")

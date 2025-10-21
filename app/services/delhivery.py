import requests
from app.schemas import ShippingRequest, CourierRate
from app.utils import get_env

def get_rate(request: ShippingRequest) -> CourierRate:
    try:
        url = "https://api.delhivery.com/api/kinko/v1/invoice/charges/.json"
        headers = {
            "Authorization": f"Token {get_env('DELHIVERY_TOKEN')}",
            "Content-Type": "application/json"
        }

        # Convert weight to grams if passed in kg
        weight_grams = int(float(request.weight) * 1000)

        params = {
            "md": "E",  # Mode: Express
            "ss": "Delivered",
            "o_pin": request.origin_pincode,
            "d_pin": request.destination_pincode,
            "cgm": weight_grams,
            "pt": getattr(request, "payment_type", "Pre-paid")  # fallback to Pre-paid
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, list) or len(data) == 0:
            raise ValueError(f"Unexpected API response: {data}")

        rate_info = data[0]

        return CourierRate(
            courier="Delhivery",
            price=rate_info.get("total_amount", 0),  # ✅ match schema field name
            currency="INR",
            raw_data=rate_info  # optional for debugging
        )

    except Exception as e:
        return CourierRate(
            courier="Delhivery",
            price=0,
            currency="INR",
            error=str(e)
        )

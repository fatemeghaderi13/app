import random
import requests
from decouple import config


def create_phone_otp(phone: str) -> dict:
    try:
        otp_code = str(random.randint(100000, 999999))

        url = "https://api.sms.ir/v1/send/verify"

        headers = {
            "Content-Type": "application/json",
            "Accept": "text/plain",
            "x-api-key": config("X_API_KEY", "U9v1HDYtblT3Qw6tqakaraL60meytZd07Vl9dkn9yWb5tXSF"),
        }

        payload = {
            "mobile": f"0{phone}",
            "templateid": 123456,
            "parameters": [
                {
                    "name": "code",
                    "value": otp_code
                }
            ]
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)

        if response.status_code != 200:
            print("SMS.IR error:", response.text)
            return {"status": False, "code": None}

        return {
            "status": True,
            "code": otp_code
        }

    except Exception as e:
        print(f"Error sending OTP SMS: {e}")
        return {"status": False, "code": None}

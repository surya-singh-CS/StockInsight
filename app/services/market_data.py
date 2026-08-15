import os
import requests

from dotenv import load_dotenv

load_dotenv()

TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

BASE_URL = "https://api.twelvedata.com"


def get_current_price(symbol: str):
    response = requests.get(
        f"{BASE_URL}/price",
        params={
            "symbol": symbol,
            "apikey": TWELVE_DATA_API_KEY
        }
    )

    data = response.json()

    if "price" not in data:
        raise Exception(
            f"Unable to fetch price for {symbol}"
        )

    return float(data["price"])
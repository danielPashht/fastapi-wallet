import requests

API_URL_BINANCE = "https://api.binance.com/api/v3/ticker/price"


def get_crypto_price(symbol: str) -> float | str:
    """
    :symbol: str, cryptocurrency symbol (e.g., BTC, TRX, ETH)
    """
    #
    symbol = symbol.upper().strip()
    url = API_URL_BINANCE + f"?symbol={symbol.upper()}USDT"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("price"):
            return float(data["price"])
    else:
        return "Error fetching price"


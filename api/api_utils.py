import random

import httpx

API_URL_BINANCE = "https://api.binance.com/api/v3/ticker/price"


async def get_crypto_price(symbol: str) -> float | str:
    """
    :symbol: str, cryptocurrency symbol (e.g., BTC, TRX, ETH)
    """
    #
    if isinstance(symbol, str):
        symbol = symbol.upper().strip()
    else:
        return "Invalid symbol"
    url = API_URL_BINANCE + f"?symbol={symbol.upper()}USDT"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("price"):
                return float(data["price"])
        else:
            return "Error fetching price"


API_BASE_URL = "http://localhost:8000"


async def prepare_test_env():
    async with httpx.AsyncClient() as client:
        # 1. Create user if not exists with id 1:
        user_exists = await client.get(f"{API_BASE_URL}/users/1")
        if not user_exists.status_code == 200:
            user_data = {"username": "testuser", "password": "testpass"}
            user_response = await client.post(f"{API_BASE_URL}/users/", json=user_data)
            user_response.raise_for_status()
            user = user_response.json()
            user_id = user["id"]
        else:
            user = user_exists.json()
            user_id = user["id"]

        # 3. Create wallet for user
        wallet_data = {"user_id": user_id, "strategies": "{}"}
        wallet_response = await client.post(f"{API_BASE_URL}/wallets/", json=wallet_data)
        wallet_response.raise_for_status()
        wallet = wallet_response.json()
        wallet_id = wallet["user_id"]

        # 2. Create assets
        assets_data = [
            {
                "symbol": "BTC",
                "balance": random.uniform(0.1, 1.0),
                "usd_price": 100000,
                "average_buy_price_usd": 80000,
                "wallet_id": 1
            },
            {
                "symbol": "ETH",
                "balance": random.uniform(1.0, 10.0),
                "usd_price": 3000,
                "average_buy_price_usd": 2500,
                "wallet_id": 1
            },
        ]
        for asset_data in assets_data:
            asset_response = await client.post(f"{API_BASE_URL}/assets/", json=asset_data)
            asset_response.raise_for_status()

        # 4. Add assets to wallet
        for asset_data in assets_data:
            asset_data["wallet_id"] = wallet_id
            asset_response = await client.post(f"{API_BASE_URL}/assets/", json=asset_data)
            asset_response.raise_for_status()

        print("Test environment prepared successfully")

if __name__ == "__main__":
    import asyncio
    asyncio.run(prepare_test_env())

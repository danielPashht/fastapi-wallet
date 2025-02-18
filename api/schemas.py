from typing import List

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int | None = None
    username: str
    password: str


class AssetSchema(BaseModel):
    symbol: str
    balance: float
    usd_price: float | None = None


class WalletSchema(BaseModel):
    user_id: int
    assets: List[AssetSchema]
    strategy: dict | None = None

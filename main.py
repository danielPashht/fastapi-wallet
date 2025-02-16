from typing import Dict

import yaml
from dataclasses import dataclass

from fastapi import FastAPI

from utils import get_crypto_price
from db import engine
from models import Base
from contextlib import asynccontextmanager
from api.api import router


# ------ App Init ------ #
@asynccontextmanager
async def lifespan(app: FastAPI):
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all, checkfirst=True)
	yield
	await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

STRATEGY = 'SELL'


def load_strategies(file_path: str) -> dict:
	with open(file_path, 'r') as file:
		strategies = yaml.safe_load(file)
	return strategies.get(STRATEGY, {})


@dataclass
class Asset:
	symbol: str
	balance: float
	usd_price: float = None


class Wallet:
	"""
	:param assets: tuple of Asset objects
	:param strategy: dict, optional
	"""

	def __init__(
			self,
			assets: tuple[Asset, ...],
			strategy: Dict[str, float] = None
	):
		self.assets = assets
		self.strategy = strategy
		self.set_usd_value_for_each_asset_in_wallet()

	@property
	def wallet_usd_value(self) -> float:
		return sum(asset.usd_price * asset.balance for asset in self.assets)

	def set_usd_value_for_each_asset_in_wallet(self):
		for asset in self.assets:
			price: float = get_crypto_price(asset.symbol)

			if isinstance(price, float):
				asset.usd_price = price
			else:
				print(f"Error fetching price for {asset.symbol}")
				continue


# I want to add feature to create strategy for assets, for example:
# 1. set desirable sell price for each asset in wallet
# 2. check the current price of asset and compare it with sell price
# 3. if current price is higher or equal to sell price -
#   then notify user to sell asset


def main():
	assets = (
		Asset(symbol='BTC', balance=0.1),
		Asset(symbol='ETH', balance=1.5),
		Asset(symbol='BNB', balance=10),
	)
	wallet = Wallet(assets)

	print('Total USD balance:', wallet.wallet_usd_value)

	strategies = load_strategies('strategies.yaml')
	print(strategies)


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

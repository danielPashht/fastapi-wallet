from pybit.unified_trading import HTTP
from tabulate import tabulate
import matplotlib.pyplot as plt


# https://bybit-exchange.github.io/docs/v5/asset/all-balance

api_key, secret = 'JYbkKr1FwLjyiaxfHD', '0Efeczb9pcMjh6yAdgLFj0j0GpTDUzKcs0rW'


session_unified = HTTP(
	testnet=False,
	api_key=api_key,
	api_secret=secret,
)


def get_unified_wallet_balance(pie: bool = False, table: bool = True, raw: bool = False):
	balances = {}
	balance = session_unified.get_wallet_balance(accountType='UNIFIED')
	coins = balance['result']['list'][0]['coin']
	for coin in coins:
		balances[coin['coin']] = coin['usdValue']
	if raw:
		return balances
	# Pie:
	if pie:
		labels = balances.keys()
		sizes = balances.values()
		fig, ax = plt.subplots(figsize=(10, 8))
		ax.pie(sizes, labels=labels, autopct='%1.1f%%')  # Add percentage labels
		plt.show()
	if table:
		return tabulate_data('UNIFIED', balances, 'usd', True)
	return balances


def get_fund_wallet_balance(table: bool = True):
	balances = {}
	account_type = 'FUND'
	balance = session_unified.get_coins_balance(accountType=account_type)
	coins = balance['result']['balance']
	for coin in coins:
		balances[coin['coin']] = coin['walletBalance']
	if table:
		return tabulate_data('FUND', balances, 'asset')
	return balances


def tabulate_data(wallet_type: str, balances: dict, balance_asset: str, add_total_row: bool = False):
	data = [['Asset', f'Balance ({balance_asset})', 'Price (USD)']]
	for asset, balance in balances.items():
		data.append([asset, balance])

	if add_total_row:
		asset_sum = 0
		for balance in balances.values():
			asset_sum += float(balance)
		data.append(['TOTAL (USD)', asset_sum])

	table = tabulate(data, headers='firstrow', tablefmt='grid', numalign='left')
	print(wallet_type, ':\n')
	print(table+'\n')


get_fund_wallet_balance()
get_unified_wallet_balance()
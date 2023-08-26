



class stone(kucoinSRC.Data):
	''' '''
	def __init__(self):
		''' '''
		pxcfg = f'{here}z-data_/kucoin.yaml'#									||use default configuration
		self.config = config.instruct(pxcfg).override(cfg)
		p = [src, srct, srcn, sink, snkt, snkn, self.config]
		kucoinSRC.Data.__init__(self, *p)

	def create_account(self, account_type, currency):
		"""Create an account
		https://docs.kucoin.com/#create-an-account
		:param account_type: Account type - main or trade
		:type account_type: string
		:param currency: Currency code
		:type currency: string
		.. code:: python
			account = client.create_account('trade', 'BTC')
		:returns: API Response
		.. code-block:: python
			{
				"id": "5bd6e9286d99522a52e458de"
			}
		:raises:  KucoinResponseException, KucoinAPIException
		"""
		data = {
			'type': account_type,
			'currency': currency
		}
		return self._post('accounts', True, data=data)
	def create_inner_transfer(self, from_account_id, to_account_id, amount, order_id=None):
		"""Get account holds placed for any active orders or pending withdraw requests
		https://docs.kucoin.com/#get-holds
		:param from_account_id: ID of account to transfer funds from - from list_accounts()
		:type from_account_id: str
		:param to_account_id: ID of account to transfer funds to - from list_accounts()
		:type to_account_id: str
		:param amount: Amount to transfer
		:type amount: int
		:param order_id: (optional) Request ID (default flat_uuid())
		:type order_id: string
		.. code:: python
			transfer = client.create_inner_transfer('5bd6e9216d99522a52e458d6', 5bc7f080b39c5c03286eef8e', 20)
		:returns: API Response
		.. code-block:: python
			{
				"orderId": "5bd6e9286d99522a52e458de"
			}
		:raises:  KucoinResponseException, KucoinAPIException
		"""
		data = {
			'payAccountId': from_account_id,
			'recAccountId': to_account_id,
			'amount': amount
		}
		if order_id:
			data['clientOid'] = order_id
		else:
			data['clientOid'] = flat_uuid()
		return self._post('accounts/inner-transfer', True, data=data)
	# Deposit Endpoints
	def create_deposit_address(self, currency):
		"""Create deposit address of currency for deposit. You can just create one deposit address.
		https://docs.kucoin.com/#create-deposit-address
		:param currency: Name of currency
		:type currency: string
		.. code:: python
			address = client.create_deposit_address('NEO')
		:returns: ApiResponse
		.. code:: python
			{
				"address": "0x78d3ad1c0aa1bf068e19c94a2d7b16c9c0fcd8b1",
				"memo": "5c247c8a03aa677cea2a251d"
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {
			'currency': currency
		}
		return self._post('deposit-addresses', True, data=data)
	def create_withdrawal(self, currency, amount, address, memo=None, is_inner=False, remark=None):
		"""Process a withdrawal
		https://docs.kucoin.com/#apply-withdraw
		:param currency: Name of currency
		:type currency: string
		:param amount: Amount to withdraw
		:type amount: number
		:param address: Address to withdraw to
		:type address: string
		:param memo: (optional) Remark to the withdrawal address
		:type memo: string
		:param is_inner: (optional) Remark to the withdrawal address
		:type is_inner: bool
		:param remark: (optional) Remark
		:type remark: string
		.. code:: python
			withdrawal = client.create_withdrawal('NEO', 20, '598aeb627da3355fa3e851')
		:returns: ApiResponse
		.. code:: python
			{
				"withdrawalId": "5bffb63303aa675e8bbe18f9"
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {
			'currency': currency,
			'amount': amount,
			'address': address
		}
		if memo:
			data['memo'] = memo
		if is_inner:
			data['isInner'] = is_inner
		if remark:
			data['remark'] = remark
		return self._post('withdrawals', True, data=data)

	def cancel_withdrawal(self, withdrawal_id):
		"""Cancel a withdrawal
		https://docs.kucoin.com/#cancel-withdrawal
		:param withdrawal_id: ID of withdrawal
		:type withdrawal_id: string
		.. code:: python
			client.cancel_withdrawal('5bffb63303aa675e8bbe18f9')
		:returns: None
		:raises: KucoinResponseException, KucoinAPIException
		"""
		return self._delete('withdrawals/{}'.format(withdrawal_id), True)
	# Order Endpoints
	def create_market_order(self, symbol, side, size=None, funds=None, client_oid=None, remark=None, stp=None):
		"""Create a market order
		One of size or funds must be set
		https://docs.kucoin.com/#place-a-new-order
		:param symbol: Name of symbol e.g. KCS-BTC
		:type symbol: string
		:param side: buy or sell
		:type side: string
		:param size: (optional) Desired amount in base currency
		:type size: string
		:param funds: (optional) Desired amount of quote currency to use
		:type funds: string
		:param client_oid: (optional) Unique order id (default flat_uuid())
		:type client_oid: string
		:param remark: (optional) remark for the order, max 100 utf8 characters
		:type remark: string
		:param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
		:type stp: string
		.. code:: python
			order = client.create_market_order('NEO', Client.SIDE_BUY, size=20)
		:returns: ApiResponse
		.. code:: python
			{
				"orderOid": "596186ad07015679730ffa02"
			}
		:raises: KucoinResponseException, KucoinAPIException, MarketOrderException
		"""
		if not size and not funds:
			raise MarketOrderException('Need size or fund parameter')
		if size and funds:
			raise MarketOrderException('Need size or fund parameter not both')
		data = {
			'side': side,
			'symbol': symbol,
			'type': self.ORDER_MARKET
		}
		if size:
			data['size'] = size
		if funds:
			data['funds'] = funds
		if client_oid:
			data['clientOid'] = client_oid
		else:
			data['clientOid'] = flat_uuid()
		if remark:
			data['remark'] = remark
		if stp:
			data['stp'] = stp
		return self._post('orders', True, data=data)
	def create_limit_order(self, symbol, side, price, size, client_oid=None, remark=None,
						   time_in_force=None, stop=None, stop_price=None, stp=None, cancel_after=None, post_only=None,
						   hidden=None, iceberg=None, visible_size=None):
		"""Create an order
		https://docs.kucoin.com/#place-a-new-order
		:param symbol: Name of symbol e.g. KCS-BTC
		:type symbol: string
		:param side: buy or sell
		:type side: string
		:param price: Name of coin
		:type price: string
		:param size: Amount of base currency to buy or sell
		:type size: string
		:param client_oid: (optional) Unique order_id  default flat_uuid()
		:type client_oid: string
		:param remark: (optional) remark for the order, max 100 utf8 characters
		:type remark: string
		:param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
		:type stp: string
		:param time_in_force: (optional) GTC, GTT, IOC, or FOK (default is GTC)
		:type time_in_force: string
		:param stop: (optional) stop type loss or entry - requires stop_price
		:type stop: string
		:param stop_price: (optional) trigger price for stop order
		:type stop_price: string
		:param cancel_after: (optional) number of seconds to cancel the order if not filled
			required time_in_force to be GTT
		:type cancel_after: string
		:param post_only: (optional) indicates that the order should only make liquidity. If any part of
			the order results in taking liquidity, the order will be rejected and no part of it will execute.
		:type post_only: bool
		:param hidden: (optional) Orders not displayed in order book
		:type hidden: bool
		:param iceberg:  (optional) Only visible portion of the order is displayed in the order book
		:type iceberg: bool
		:param visible_size: (optional) The maximum visible size of an iceberg order
		:type visible_size: bool
		.. code:: python
			order = client.create_limit_order('KCS-BTC', Client.SIDE_BUY, '0.01', '1000')
		:returns: ApiResponse
		.. code:: python
			{
				"orderOid": "596186ad07015679730ffa02"
			}
		:raises: KucoinResponseException, KucoinAPIException, LimitOrderException
		"""
		if stop and not stop_price:
			raise LimitOrderException('Stop order needs stop_price')
		if stop_price and not stop:
			raise LimitOrderException('Stop order type required with stop_price')
		if cancel_after and time_in_force != self.TIMEINFORCE_GOOD_TILL_TIME:
			raise LimitOrderException('Cancel after only works with time_in_force = "GTT"')
		if hidden and iceberg:
			raise LimitOrderException('Order can be either "hidden" or "iceberg"')
		if iceberg and not visible_size:
			raise LimitOrderException('Iceberg order requires visible_size')
		data = {
			'symbol': symbol,
			'side': side,
			'type': self.ORDER_LIMIT,
			'price': price,
			'size': size
		}
		if client_oid:
			data['clientOid'] = client_oid
		else:
			data['clientOid'] = flat_uuid()
		if remark:
			data['remark'] = remark
		if stp:
			data['stp'] = stp
		if time_in_force:
			data['timeInForce'] = time_in_force
		if cancel_after:
			data['cancelAfter'] = cancel_after
		if post_only:
			data['postOnly'] = post_only
		if stop:
			data['stop'] = stop
			data['stopPrice'] = stop_price
		if hidden:
			data['hidden'] = hidden
		if iceberg:
			data['iceberg'] = iceberg
			data['visible_size'] = visible_size
		return self._post('orders', True, data=data)
	def cancel_order(self, order_id):
		"""Cancel an order
		https://docs.kucoin.com/#cancel-an-order
		:param order_id: Order id
		:type order_id: string
		.. code:: python
			res = client.cancel_order('5bd6e9286d99522a52e458de)
		:returns: ApiResponse
		.. code:: python
			{
				"cancelledOrderIds": [
					"5bd6e9286d99522a52e458de"
				]
			}
		:raises: KucoinResponseException, KucoinAPIException
		KucoinAPIException If order_id is not found
		"""
		return self._delete('orders/{}'.format(order_id), True)
	def cancel_all_orders(self, symbol=None):
		"""Cancel all orders
		https://docs.kucoin.com/#cancel-all-orders
		.. code:: python
			res = client.cancel_all_orders()
		:returns: ApiResponse
		.. code:: python
			{
				"cancelledOrderIds": [
					"5bd6e9286d99522a52e458de"
				]
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {}
		if symbol is not None:
			data['symbol'] = symbol
		return self._delete('orders', True, data=data)
	# User Account Endpoints
	def get_accounts(self):
		"""Get a list of accounts
		https://docs.kucoin.com/#accounts
		.. code:: python
			accounts = client.get_accounts()
		:returns: API Response
		.. code-block:: python
			[
				{
					"id": "5bd6e9286d99522a52e458de",
					"currency": "BTC",
					"type": "main",
					"balance": "237582.04299",
					"available": "237582.032",
					"holds": "0.01099"
				},
				{
					"id": "5bd6e9216d99522a52e458d6",
					"currency": "BTC",
					"type": "trade",
					"balance": "1234356",
					"available": "1234356",
					"holds": "0"
				}
			]
		:raises:  KucoinResponseException, KucoinAPIException
		"""
		return self._get('accounts', True)
	def get_account(self, account_id):
		"""Get an individual account
		https://docs.kucoin.com/#get-an-account
		:param account_id: ID for account - from list_accounts()
		:type account_id: string
		.. code:: python
			account = client.get_account('5bd6e9216d99522a52e458d6')
		:returns: API Response
		.. code-block:: python
			{
				"currency": "KCS",
				"balance": "1000000060.6299",
				"available": "1000000060.6299",
				"holds": "0"
			}
		:raises:  KucoinResponseException, KucoinAPIException
		"""
		return self._get('accounts/{}'.format(account_id), True)

	def get_account_activity(self, account_id, start=None, end=None, page=None, limit=None):
		"""Get list of account activity
		https://docs.kucoin.com/#get-account-history
		:param account_id: ID for account - from list_accounts()
		:type account_id: string
		:param start: (optional) Start time as unix timestamp
		:type start: string
		:param end: (optional) End time as unix timestamp
		:type end: string
		:param page: (optional) Current page - default 1
		:type page: int
		:param limit: (optional) Number of results to return - default 50
		:type limit: int
		.. code:: python
			history = client.get_account_activity('5bd6e9216d99522a52e458d6')
			history = client.get_account_activity('5bd6e9216d99522a52e458d6', start='1540296039000')
			history = client.get_account_activity('5bd6e9216d99522a52e458d6', page=2, page_size=10)
		:returns: API Response
		.. code-block:: python
			{
				"currentPage": 1,
				"pageSize": 10,
				"totalNum": 2,
				"totalPage": 1,
				"items": [
					{
						"currency": "KCS",
						"amount": "0.0998",
						"fee": "0",
						"balance": "1994.040596",
						"bizType": "withdraw",
						"direction": "in",
						"createdAt": 1540296039000,
						"context": {
							 "orderId": "5bc7f080b39c5c03286eef8a",
							 "currency": "BTC"
						 }
					},
					{
						"currency": "KCS",
						"amount": "0.0998",
						"fee": "0",
						"balance": "1994.140396",
						"bizType": "trade exchange",
						"direction": "in",
						"createdAt": 1540296039000,
						"context": {
							 "orderId": "5bc7f080b39c5c03286eef8e",
							 "tradeId": "5bc7f080b3949c03286eef8a",
							 "symbol": "BTC-USD"
						}
					}
				]
			}
		:raises:  KucoinResponseException, KucoinAPIException
		"""
		data = {}
		if start:
			data['startAt'] = start
		if end:
			data['endAt'] = end
		if page:
			data['currentPage'] = page
		if limit:
			data['pageSize'] = limit
		return self._get('accounts/{}/ledgers'.format(account_id), True, data=data)
	def get_account_holds(self, account_id, page=None, page_size=None):
		"""Get account holds placed for any active orders or pending withdraw requests
		https://docs.kucoin.com/#get-holds
		:param account_id: ID for account - from list_accounts()
		:type account_id: string
		:param page: (optional) Current page - default 1
		:type page: int
		:param page_size: (optional) Number of results to return - default 50
		:type page_size: int
		.. code:: python
			holds = client.get_account_holds('5bd6e9216d99522a52e458d6')
			holds = client.get_account_holds('5bd6e9216d99522a52e458d6', page=2, page_size=10)
		:returns: API Response
		.. code-block:: python
			{
				"currentPage": 1,
				"pageSize": 10,
				"totalNum": 2,
				"totalPage": 1,
				"items": [
					{
						"currency": "ETH",
						"holdAmount": "5083",
						"bizType": "Withdraw",
						"orderId": "5bc7f080b39c5c03286eef8e",
						"createdAt": 1545898567000,
						"updatedAt": 1545898567000
					},
					{
						"currency": "ETH",
						"holdAmount": "1452",
						"bizType": "Withdraw",
						"orderId": "5bc7f518b39c5c033818d62d",
						"createdAt": 1545898567000,
						"updatedAt": 1545898567000
					}
				]
			}
		:raises:  KucoinResponseException, KucoinAPIException
		"""
		data = {}
		if page:
			data['currentPage'] = page
		if page_size:
			data['pageSize'] = page_size
		return self._get('accounts/{}/holds'.format(account_id), True, data=data)


	def get_deposit_address(self, currency):
		"""Get deposit address for a currency
		https://docs.kucoin.com/#get-deposit-address
		:param currency: Name of currency
		:type currency: string
		.. code:: python
			address = client.get_deposit_address('NEO')
		:returns: ApiResponse
		.. code:: python
			{
				"address": "0x78d3ad1c0aa1bf068e19c94a2d7b16c9c0fcd8b1",
				"memo": "5c247c8a03aa677cea2a251d"
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {
			'currency': currency
		}
		return self._get('deposit-addresses', True, data=data)
	def get_deposits(self, currency=None, status=None, start=None, end=None, page=None, limit=None):
		"""Get deposit records for a currency
		https://docs.kucoin.com/#get-deposit-list
		:param currency: Name of currency (optional)
		:type currency: string
		:param status: optional - Status of deposit (PROCESSING, SUCCESS, FAILURE)
		:type status: string
		:param start: (optional) Start time as unix timestamp
		:type start: string
		:param end: (optional) End time as unix timestamp
		:type end: string
		:param page: (optional) Page to fetch
		:type page: int
		:param limit: (optional) Number of transactions
		:type limit: int
		.. code:: python
			deposits = client.get_deposits('NEO')
		:returns: ApiResponse
		.. code:: python
			{
				"currentPage": 1,
				"pageSize": 5,
				"totalNum": 2,
				"totalPage": 1,
				"items": [
					{
						"address": "0x5f047b29041bcfdbf0e4478cdfa753a336ba6989",
						"memo": "5c247c8a03aa677cea2a251d",
						"amount": 1,
						"fee": 0.0001,
						"currency": "KCS",
						"isInner": false,
						"walletTxId": "5bbb57386d99522d9f954c5a@test004",
						"status": "SUCCESS",
						"createdAt": 1544178843000,
						"updatedAt": 1544178891000
					}, {
						"address": "0x5f047b29041bcfdbf0e4478cdfa753a336ba6989",
						"memo": "5c247c8a03aa677cea2a251d",
						"amount": 1,
						"fee": 0.0001,
						"currency": "KCS",
						"isInner": false,
						"walletTxId": "5bbb57386d99522d9f954c5a@test003",
						"status": "SUCCESS",
						"createdAt": 1544177654000,
						"updatedAt": 1544178733000
					}
				]
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {}
		if currency:
			data['currency'] = currency
		if status:
			data['status'] = status
		if start:
			data['startAt'] = start
		if end:
			data['endAt'] = end
		if limit:
			data['pageSize'] = limit
		if page:
			data['page'] = page
		return self._get('deposits', True, data=data)
	# Withdraw Endpoints
	def get_withdrawals(self, currency=None, status=None, start=None, end=None, page=None, limit=None):
		"""Get deposit records for a currency
		https://docs.kucoin.com/#get-withdrawals-list
		:param currency: Name of currency (optional)
		:type currency: string
		:param status: optional - Status of deposit (PROCESSING, SUCCESS, FAILURE)
		:type status: string
		:param start: (optional) Start time as unix timestamp
		:type start: string
		:param end: (optional) End time as unix timestamp
		:type end: string
		:param page: (optional) Page to fetch
		:type page: int
		:param limit: (optional) Number of transactions
		:type limit: int
		.. code:: python
			withdrawals = client.get_withdrawals('NEO')
		:returns: ApiResponse
		.. code:: python
			{
				"currentPage": 1,
				"pageSize": 10,
				"totalNum": 1,
				"totalPage": 1,
				"items": [
					{
						"id": "5c2dc64e03aa675aa263f1ac",
						"address": "0x5bedb060b8eb8d823e2414d82acce78d38be7fe9",
						"memo": "",
						"currency": "ETH",
						"amount": 1.0000000,
						"fee": 0.0100000,
						"walletTxId": "3e2414d82acce78d38be7fe9",
						"isInner": false,
						"status": "FAILURE",
						"createdAt": 1546503758000,
						"updatedAt": 1546504603000
					}
				]
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {}
		if currency:
			data['currency'] = currency
		if status:
			data['status'] = status
		if start:
			data['startAt'] = start
		if end:
			data['endAt'] = end
		if limit:
			data['pageSize'] = limit
		if page:
			data['page'] = page
		return self._get('withdrawals', True, data=data)
	def get_withdrawal_quotas(self, currency):
		"""Get withdrawal quotas for a currency
		https://docs.kucoin.com/#get-withdrawal-quotas
		:param currency: Name of currency
		:type currency: string
		.. code:: python
			quotas = client.get_withdrawal_quotas('ETH')
		:returns: ApiResponse
		.. code:: python
			{
				"currency": "ETH",
				"availableAmount": 2.9719999,
				"remainAmount": 2.9719999,
				"withdrawMinSize": 0.1000000,
				"limitBTCAmount": 2.0,
				"innerWithdrawMinFee": 0.00001,
				"isWithdrawEnabled": true,
				"withdrawMinFee": 0.0100000,
				"precision": 7
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {
			'currency': currency
		}
		return self._get('withdrawals/quotas', True, data=data)
	def get_orders(self, symbol=None, status=None, side=None, order_type=None,
				   start=None, end=None, page=None, limit=None):
		"""Get list of orders
		https://docs.kucoin.com/#list-orders
		:param symbol: (optional) Name of symbol e.g. KCS-BTC
		:type symbol: string
		:param status: (optional) Specify status active or done (default done)
		:type status: string
		:param side: (optional) buy or sell
		:type side: string
		:param order_type: (optional) limit, market, limit_stop or market_stop
		:type order_type: string
		:param start: (optional) Start time as unix timestamp
		:type start: string
		:param end: (optional) End time as unix timestamp
		:type end: string
		:param page: (optional) Page to fetch
		:type page: int
		:param limit: (optional) Number of orders
		:type limit: int
		.. code:: python
			orders = client.get_orders(symbol='KCS-BTC', status='active')
		:returns: ApiResponse
		.. code:: python
			{
				"currentPage": 1,
				"pageSize": 1,
				"totalNum": 153408,
				"totalPage": 153408,
				"items": [
					{
						"id": "5c35c02703aa673ceec2a168",
						"symbol": "BTC-USDT",
						"opType": "DEAL",
						"type": "limit",
						"side": "buy",
						"price": "10",
						"size": "2",
						"funds": "0",
						"dealFunds": "0.166",
						"dealSize": "2",
						"fee": "0",
						"feeCurrency": "USDT",
						"stp": "",
						"stop": "",
						"stopTriggered": false,
						"stopPrice": "0",
						"timeInForce": "GTC",
						"postOnly": false,
						"hidden": false,
						"iceberge": false,
						"visibleSize": "0",
						"cancelAfter": 0,
						"channel": "IOS",
						"clientOid": null,
						"remark": null,
						"tags": null,
						"isActive": false,
						"cancelExist": false,
						"createdAt": 1547026471000
					}
				]
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {}
		if symbol:
			data['symbol'] = symbol
		if status:
			data['status'] = status
		if side:
			data['side'] = side
		if order_type:
			data['type'] = order_type
		if start:
			data['startAt'] = start
		if end:
			data['endAt'] = end
		if page:
			data['page'] = page
		if limit:
			data['pageSize'] = limit
		return self._get('orders', True, data=data)
	def get_historical_orders(self, symbol=None, side=None,
							  start=None, end=None, page=None, limit=None):
		"""List of KuCoin V1 historical orders.
		https://docs.kucoin.com/#get-v1-historical-orders-list
		:param symbol: (optional) Name of symbol e.g. KCS-BTC
		:type symbol: string
		:param side: (optional) buy or sell
		:type side: string
		:param start: (optional) Start time as unix timestamp
		:type start: string
		:param end: (optional) End time as unix timestamp
		:type end: string
		:param page: (optional) Page to fetch
		:type page: int
		:param limit: (optional) Number of orders
		:type limit: int
		.. code:: python
			orders = client.get_historical_orders(symbol='KCS-BTC')
		:returns: ApiResponse
		.. code:: python
			{
				"currentPage": 1,
				"pageSize": 50,
				"totalNum": 1,
				"totalPage": 1,
				"items": [
					{
						"symbol": "SNOV-ETH",
						"dealPrice": "0.0000246",
						"dealValue": "0.018942",
						"amount": "770",
						"fee": "0.00001137",
						"side": "sell",
						"createdAt": 1540080199
					}
				]
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {}
		if symbol:
			data['symbol'] = symbol
		if side:
			data['side'] = side
		if start:
			data['startAt'] = start
		if end:
			data['endAt'] = end
		if page:
			data['page'] = page
		if limit:
			data['pageSize'] = limit
		return self._get('hist-orders', True, data=data)
	def get_order(self, order_id):
		"""Get order details
		https://docs.kucoin.com/#get-an-order
		:param order_id: orderOid value
		:type order_id: str
		.. code:: python
			order = client.get_order('5c35c02703aa673ceec2a168')
		:returns: ApiResponse
		.. code:: python
			{
				"id": "5c35c02703aa673ceec2a168",
				"symbol": "BTC-USDT",
				"opType": "DEAL",
				"type": "limit",
				"side": "buy",
				"price": "10",
				"size": "2",
				"funds": "0",
				"dealFunds": "0.166",
				"dealSize": "2",
				"fee": "0",
				"feeCurrency": "USDT",
				"stp": "",
				"stop": "",
				"stopTriggered": false,
				"stopPrice": "0",
				"timeInForce": "GTC",
				"postOnly": false,
				"hidden": false,
				"iceberge": false,
				"visibleSize": "0",
				"cancelAfter": 0,
				"channel": "IOS",
				"clientOid": null,
				"remark": null,
				"tags": null,
				"isActive": false,
				"cancelExist": false,
				"createdAt": 1547026471000
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		return self._get('orders/{}'.format(order_id), True)
	# Fill Endpoints
	def get_fills(self, order_id=None, symbol=None, side=None, order_type=None,
				  start=None, end=None, page=None, limit=None):
		"""Get a list of recent fills.
		https://docs.kucoin.com/#list-fills
		:param order_id: (optional) generated order id
		:type order_id: string
		:param symbol: (optional) Name of symbol e.g. KCS-BTC
		:type symbol: string
		:param side: (optional) buy or sell
		:type side: string
		:param order_type: (optional) limit, market, limit_stop or market_stop
		:type order_type: string
		:param start: Start time as unix timestamp (optional)
		:type start: string
		:param end: End time as unix timestamp (optional)
		:type end: string
		:param page: optional - Page to fetch
		:type page: int
		:param limit: optional - Number of orders
		:type limit: int
		.. code:: python
			fills = client.get_fills()
		:returns: ApiResponse
		.. code:: python
			{
				"currentPage":1,
				"pageSize":1,
				"totalNum":251915,
				"totalPage":251915,
				"items":[
					{
						"symbol":"BTC-USDT",
						"tradeId":"5c35c02709e4f67d5266954e",
						"orderId":"5c35c02703aa673ceec2a168",
						"counterOrderId":"5c1ab46003aa676e487fa8e3",
						"side":"buy",
						"liquidity":"taker",
						"forceTaker":true,
						"price":"0.083",
						"size":"0.8424304",
						"funds":"0.0699217232",
						"fee":"0",
						"feeRate":"0",
						"feeCurrency":"USDT",
						"stop":"",
						"type":"limit",
						"createdAt":1547026472000
					}
				]
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {}
		if order_id:
			data['orderId'] = order_id
		if symbol:
			data['symbol'] = symbol
		if side:
			data['side'] = side
		if order_type:
			data['type'] = order_type
		if start:
			data['startAt'] = start
		if end:
			data['endAt'] = end
		if page:
			data['page'] = page
		if limit:
			data['pageSize'] = limit
		return self._get('fills', True, data=data)
	# Market Endpoints

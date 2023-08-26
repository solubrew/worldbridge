class Data(worldbridger.stone):
	''' '''
	def __init__(self, sandbox=False, requests_params=None):
		"""Kucoin API Client constructor
		https://docs.kucoin.com/
		:param api_key: Api Token Id
		:type api_key: string
		:param api_secret: Api Secret
		:type api_secret: string
		:param passphrase: Api Passphrase used to create API
		:type passphrase: string
		:param sandbox: (optional) Use the sandbox endpoint or not (default False)
		:type sandbox: bool
		:param requests_params: (optional) Dictionary of requests params to use for all calls
		:type requests_params: dict.
		.. code:: python
			client = Client(api_key, api_secret, api_passphrase)
		"""
		pxcfg = f'{here}z-data_/kucoin.yaml'#									||use default configuration
		self.config = config.instruct(pxcfg).override(cfg)
		if sandbox == True:
			self.config.select('sandbox')
		else:
			self.config.select('live')
		p = [src, srct, srcn, sink, snkt, snkn, self.config]
		worldbridger.stone.__init__(self, *p)
		self.API_KEY = self.config.dikt['api']['key']
		self.API_SECRET = self.config.dikt['api']['secret']
		self.API_PASSPHRASE = self.config.dikt['api']['passphrase']
		self._requests_params = requests_params
		self.session = self._init_session()
	def _init_session(self):
		session = requests.session()
		headers = {'Accept': 'application/json',
				   'User-Agent': 'python-kucoin',
				   'Content-Type': 'application/json',
				   'KC-API-KEY': self.API_KEY,
				   'KC-API-PASSPHRASE': self.API_PASSPHRASE}
		session.headers.update(headers)
		return session
	@staticmethod
	def _get_params_for_sig(data):
		"""Convert params to ordered string for signature
		:param data:
		:return: ordered parameters like amount=10&price=1.1&type=BUY
		"""
		return '&'.join([f"{key}={data[key]}" for key in data])
	def _generate_signature(self, nonce, method, path, data):
		"""Generate the call signature
		:param path:
		:param data:
		:param nonce:
		:return: signature string
		"""
		data_json = ""
		endpoint = path
		if method == "get":
			if data:
				query_string = self._get_params_for_sig(data)
				endpoint = f"{path}?{query_string}"
		elif data:
			data_json = compact_json_dict(data)
		sig_str = (f"{nonce}{}{endpoint}{data_json}".format(method.upper())).encode('utf-8')
		m = hmac.new(self.API_SECRET.encode('utf-8'), sig_str, hashlib.sha256)
		return base64.b64encode(m.digest())
	def _create_path(self, path):
		return f'/api/{self.API_VERSION}/{path}'
	def _create_uri(self, path):
		return f'{self.API_URL}{path}'
	def get_currencies(self):
		"""List known currencies
		https://docs.kucoin.com/#get-currencies
		.. code:: python
			currencies = client.get_currencies()
		:returns: API Response
		.. code-block:: python
			[
				{
					"currency": "BTC",
					"name": "BTC",
					"fullName": "Bitcoin",
					"precision": 8
				},
				{
					"currency": "ETH",
					"name": "ETH",
					"fullName": "Ethereum",
					"precision": 7
				}
			]
		:raises:  KucoinResponseException, KucoinAPIException
		"""
		return self._get('currencies', False)
	def get_currency(self, currency):
		"""Get single currency detail
		https://docs.kucoin.com/#get-currency-detail
		.. code:: python
			# call with no coins
			currency = client.get_currency('BTC')
		:returns: API Response
		.. code-block:: python
			{
				"currency": "BTC",
				"name": "BTC",
				"fullName": "Bitcoin",
				"precision": 8,
				"withdrawalMinSize": "0.002",
				"withdrawalMinFee": "0.0005",
				"isWithdrawEnabled": true,
				"isDepositEnabled": true
			}
		:raises:  KucoinResponseException, KucoinAPIException
		"""
		return self._get('currencies/{}'.format(currency), False)



	def get_symbols(self):
		"""Get a list of available currency pairs for trading.
		https://docs.kucoin.com/#symbols-amp-ticker
		.. code:: python
			symbols = client.get_symbols()
		:returns: ApiResponse
		.. code:: python
			[
				{
					"symbol": "BTC-USDT",
					"name": "BTC-USDT",
					"baseCurrency": "BTC",
					"quoteCurrency": "USDT",
					"baseMinSize": "0.00000001",
					"quoteMinSize": "0.01",
					"baseMaxSize": "10000",
					"quoteMaxSize": "100000",
					"baseIncrement": "0.00000001",
					"quoteIncrement": "0.01",
					"priceIncrement": "0.00000001",
					"enableTrading": true
				}
			]
		:raises: KucoinResponseException, KucoinAPIException
		"""
		return self._get('symbols', False)
	def get_ticker(self, symbol=None):
		"""Get symbol tick
		https://docs.kucoin.com/#get-ticker
		:param symbol: (optional) Name of symbol e.g. KCS-BTC
		:type symbol: string
		.. code:: python
			all_ticks = client.get_ticker()
			ticker = client.get_ticker('ETH-BTC')
		:returns: ApiResponse
		.. code:: python
			{
				"sequence": "1545825031840",	  # now sequence
				"price": "3494.367783",		   # last trade price
				"size": "0.05027185",			 # last trade size
				"bestBid": "3494.367783",		 # best bid price
				"bestBidSize": "2.60323254",	  # size at best bid price
				"bestAsk": "3499.12",			 # best ask price
				"bestAskSize": "0.01474011"	   # size at best ask price
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {}
		tick_path = 'market/allTickers'
		if symbol is not None:
			tick_path = 'market/orderbook/level1'
			data = {
				'symbol': symbol
			}
		return self._get(tick_path, False, data=data)
	def getPrice(self, symbol=None, base=None):
		"""Get fiat price for currency
		https://docs.kucoin.com/#get-fiat-price
		:param base: (optional) Fiat,eg.USD,EUR, default is USD.
		:type base: string
		:param symbol: (optional) Cryptocurrencies.For multiple cyrptocurrencies, please separate them with
					   comma one by one. default is all
		:type symbol: string
		.. code:: python
			prices = client.get_fiat_prices()
		:returns: ApiResponse
		.. code:: python
			{
				"BTC": "3911.28000000",
				"ETH": "144.55492453",
				"LTC": "48.45888179",
				"KCS": "0.45546856"
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {}
		if base is not None:
			data['base'] = base
		if symbol is not None:
			data['currencies'] = symbol
		return self._get('prices', False, data=data)
	def get_24hr_stats(self, symbol):
		"""Get 24hr stats for a symbol. Volume is in base currency units. open, high, low are in quote currency units.
		:param symbol: (optional) Name of symbol e.g. KCS-BTC
		:type symbol: string
		.. code:: python
			stats = client.get_24hr_stats('ETH-BTC')
		:returns: ApiResponse
		Without a symbol param
		.. code:: python
			{
				"symbol": "BTC-USDT",
				"changeRate": "0.0128",   # 24h change rate
				"changePrice": "0.8",	 # 24h rises and falls in price (if the change rate is a negative number,
										  # the price rises; if the change rate is a positive number, the price falls.)
				"open": 61,			   # Opening price
				"close": 63.6,			# Closing price
				"high": "63.6",		   # Highest price filled
				"low": "61",			  # Lowest price filled
				"vol": "244.78",		  # Transaction quantity
				"volValue": "15252.0127"  # Transaction amount
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {
			'symbol': symbol
		}
		return self._get('market/stats', False, data=data)
	def get_markets(self):
		"""Get supported market list
		https://docs.kucoin.com/#get-market-list
		.. code:: python
			markets = client.get_markets()
		:returns: ApiResponse
		.. code:: python
			{
				"data": [
					"BTC",
					"ETH",
					"USDT"
				]
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		return self._get('markets', False)
	def get_order_book(self, symbol):
		"""Get a list of bids and asks aggregated by price for a symbol.
		Returns up to 100 depth each side. Fastest Order book API
		https://docs.kucoin.com/#get-part-order-book-aggregated
		:param symbol: Name of symbol e.g. KCS-BTC
		:type symbol: string
		.. code:: python
			orders = client.get_order_book('KCS-BTC')
		:returns: ApiResponse
		.. code:: python
			{
				"sequence": "3262786978",
				"bids": [
					["6500.12", "0.45054140"],  # [price, size]
					["6500.11", "0.45054140"]
				],
				"asks": [
					["6500.16", "0.57753524"],
					["6500.15", "0.57753524"]
				]
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {
			'symbol': symbol
		}
		return self._get('market/orderbook/level2_100', False, data=data)
	def get_full_order_book(self, symbol):
		"""Get a list of all bids and asks aggregated by price for a symbol.
		This call is generally used by professional traders because it uses more server resources and traffic,
		and Kucoin has strict access frequency control.
		https://docs.kucoin.com/#get-full-order-book-aggregated
		:param symbol: Name of symbol e.g. KCS-BTC
		:type symbol: string
		.. code:: python
			orders = client.get_order_book('KCS-BTC')
		:returns: ApiResponse
		.. code:: python
			{
				"sequence": "3262786978",
				"bids": [
					["6500.12", "0.45054140"],  # [price size]
					["6500.11", "0.45054140"]
				],
				"asks": [
					["6500.16", "0.57753524"],
					["6500.15", "0.57753524"]
				]
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {
			'symbol': symbol
		}
		return self._get('market/orderbook/level2', False, data=data)
	def get_full_order_book_level3(self, symbol):
		"""Get a list of all bids and asks non-aggregated for a symbol.
		This call is generally used by professional traders because it uses more server resources and traffic,
		and Kucoin has strict access frequency control.
		https://docs.kucoin.com/#get-full-order-book-atomic
		:param symbol: Name of symbol e.g. KCS-BTC
		:type symbol: string
		.. code:: python
			orders = client.get_order_book('KCS-BTC')
		:returns: ApiResponse
		.. code:: python
			{
				"sequence": "1545896707028",
				"bids": [
					[
						"5c2477e503aa671a745c4057",   # orderId
						"6",						  # price
						"0.999"					   # size
					],
					[
						"5c2477e103aa671a745c4054",
						"5",
						"0.999"
					]
				],
				"asks": [
					[
						"5c24736703aa671a745c401e",
						"200",
						"1"
					],
					[
						"5c2475c903aa671a745c4033",
						"201",
						"1"
					]
				]
			}
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {
			'symbol': symbol
		}
		return self._get('market/orderbook/level3', False, data=data)
	def get_trade_histories(self, symbol):
		"""List the latest trades for a symbol
		https://docs.kucoin.com/#get-trade-histories
		:param symbol: Name of symbol e.g. KCS-BTC
		:type symbol: string
		.. code:: python
			orders = client.get_trade_histories('KCS-BTC')
		:returns: ApiResponse
		.. code:: python
			[
				{
					"sequence": "1545896668571",
					"price": "0.07",				# Filled price
					"size": "0.004",				# Filled amount
					"side": "buy",				  # Filled side. The filled side is set to the taker by default.
					"time": 1545904567062140823	 # Transaction time
				},
				{
					"sequence": "1545896668578",
					"price": "0.054",
					"size": "0.066",
					"side": "buy",
					"time": 1545904581619888405
				}
			]
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {
			'symbol': symbol
		}
		return self._get('market/histories', False, data=data)
	def get_kline_data(self, symbol, kline_type='5min', start=None, end=None):
		"""Get kline data
		For each query, the system would return at most 1500 pieces of data.
		To obtain more data, please page the data by time.
		:param symbol: Name of symbol e.g. KCS-BTC
		:type symbol: string
		:param kline_type: type of symbol, type of candlestick patterns: 1min, 3min, 5min, 15min, 30min, 1hour, 2hour,
						   4hour, 6hour, 8hour, 12hour, 1day, 1week
		:type kline_type: string
		:param start: Start time as unix timestamp (optional) default start of day in UTC
		:type start: int
		:param end: End time as unix timestamp (optional) default now in UTC
		:type end: int
		https://docs.kucoin.com/#get-historic-rates
		.. code:: python
			klines = client.get_kline_data('KCS-BTC', '5min', 1507479171, 1510278278)
		:returns: ApiResponse
		.. code:: python
			[
				[
					"1545904980",			 //Start time of the candle cycle
					"0.058",				  //opening price
					"0.049",				  //closing price
					"0.058",				  //highest price
					"0.049",				  //lowest price
					"0.018",				  //Transaction amount
					"0.000945"				//Transaction volume
				],
				[
					"1545904920",
					"0.058",
					"0.072",
					"0.072",
					"0.058",
					"0.103",
					"0.006986"
				]
			]
		:raises: KucoinResponseException, KucoinAPIException
		"""
		data = {
			'symbol': symbol
		}
		if kline_type is not None:
			data['type'] = kline_type
		if start is not None:
			data['startAt'] = start
		else:
			data['startAt'] = calendar.timegm(datetime.utcnow().date().timetuple())
		if end is not None:
			data['endAt'] = end
		else:
			data['endAt'] = int(time.time())
		return self._get('market/candles', False, data=data)
import json
import uuid
def flat_uuid():
	"""create a flat uuid
	:return: uuid with '-' removed
	"""
	return str(uuid.uuid4()).replace('-', '')
def compact_json_dict(data):
	"""convert dict to compact json
	:return: str
	"""
	return json.dumps(data, separators=(',', ':'), ensure_ascii=False)

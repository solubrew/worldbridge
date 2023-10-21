#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: '2572e9f2-4132-463f-bead-4bd51b194733'  #							||
	name: Worldbridge Web3 Protocol Uniswap Python Document  #					||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	path: <[LEXIvrs]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
# ================================Core Modules===================================||
import json as j
import time
from os.path import abspath, dirname, join  # ||
from typing import List, Optional, Union

from condor import condor
# ===============================================================================||
from pandas import DataFrame  # ||
from subtrix import thing

from worldbridge.web3.protocols import evm, addresses

#===============================================================================||
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
where = abspath(join(''))#														||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/uniswap.yaml')
class Data(evm.EVMViewer):
	'''Uniswap Data Source '''
	def __init__(self, network=1, conx=None, store=None, cfg: dict={}) -> None:
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg)
		evm.EVMViewer.__init__(self, network, conx, None, self.config)
		self.version = self.config.dikt['cfg']['version']# TODO: Write tests for slippage
		self.max_slippage = self.config.dikt['cfg']['max_slippage']
		self.protocols = self.config.dikt['protocols']
		factory = self.protocols['factory'][self.version]
		faddr =  addresses.AddrO(factory['networks'][self.network])
		abi = j.loads(factory['abi'])
		self.factory = faddr.initW3(self.w3).getContract(abi)
		if self.version in ('v2', 'v3'):
			router = self.protocols['swap'][self.version]
			raddr = addresses.AddrO(router['networks'][self.network])
			abi = j.loads(router['abi'])
			self.router = raddr.initW3(self.w3).getContract(abi)

	def checkPair(self, token0, token1):
		''' '''
		if log: print('TOKEN', token0, 'TOKEN', token1)
		result = self.factory.functions.getPair(token0, token1).call()
		if log: print('Pair', result)
		if result == '0x0000000000000000000000000000000000000000':
			return False
		return True

	def getTokens(self, how='cache') -> List[dict]:
		'''Get list of tokens for requesting data from uniswap contract'''
		if how == 'cache':
			rdr = sonql.doc(db).read({'view': ['unis_tokens']})
		tokenCount = self.factory.functions.tokenCount().call()
		tokens = []
		for i in range(tokenCount):
			address = self.factory.functions.getTokenWithId(i).call()
			if address == "0x0000000000000000000000000000000000000000":# Token is ETH
				continue
			token = self.get_token(address)
			tokens.append([address, token['name'], token['symbol']])
		df = DataFrame(tokens, columns=['address', 'name', 'symbol'])
		return df

	def getToken(self, address: evm.AddressLike) -> dict:
		''' '''
		token_contract = self._load_contract(abi_name="erc20", address=address)
		try:
			symbol = token_contract.functions.symbol().call()
			symbol = '' if symbol == None else symbol
			name = token_contract.functions.name().call()
			name = '' if name == None else name
		except Exception as e:
			symbol, name = None, None
			print('Get Uniswap Token Failed', e)
		return {"name": name, "symbol": symbol}

	def getExchangeAddressByToken(self, addr: evm.AddressLike) -> evm.AddressLike:
		try:
			ex_addr: evm.AddressLike = self.factory.functions.getExchange(addr).call()
		except Exception as e:
			print('Get Exchange Address Failed', e)
		return ex_addr

	def token_address_from_exchange(self, exchange_addr: evm.AddressLike) -> evm.AddressLike:
		token_addr: Address = (self.exchange_contract(ex_addr=exchange_addr).functions.tokenAddress(exchange_addr).call())
		return token_addr

	def exchange_contract(self, token_addr: evm.AddressLike = None, ex_addr: evm.AddressLike = None) -> evm.Contract:
		if not ex_addr and token_addr:
			ex_addr = self.exchange_address_from_token(token_addr)
		if ex_addr is None:
			raise InvalidToken(token_addr)
		abi_name, asset, version = "exchange", 'uniswap', 'v1'
		params = {'abi_name': abi_name, 'address': ex_addr, 'asset': asset,
															'version': version}
		contract = self._load_contract(**params)
		return contract

	def erc20_contract(self, token_addr: evm.AddressLike) -> evm.Contract:
		return self._load_contract(abi_name="erc20", address=token_addr)

	def getPriceByTokens(self, tokens):
		'''Get price by provided list of tokens'''
		return self

	def get_weth_address(self) -> evm.ChecksumAddress:
		# Contract calls should always return checksummed addresses
		#address: ChecksumAddress = self.router.functions.WETH().call()
		#print('WETH Address', address)
		addr: evm.ChecksumAddress = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
		return addresses.AddrO(addr).str_address

	def get_eth_token_input_price(self, token: evm.AddressLike, qty: evm.Wei) -> evm.Wei:
		"""Public price for ETH to Token trades with an exact input."""
		token = addresses.AddrO(token).address
		price = None
		if self.version == 'v1':
			ex = self.exchange_contract(token)
			call = ex.functions.getEthToTokenInputPrice
			args = [int(qty)]
			price: self.makeCall(call, args)
		elif self.version == 'v2':
			weth = addresses.AddrO(self.get_weth_address()).address
			if weth == token:
				price = 1
			else:
				call = self.router.functions.getAmountsOut
				args = [int(qty), [weth, token]]
				response = self.makeCall(call, args)
				if response:
					price = response[-1]
		return price

	def get_token_eth_input_price(self, token: evm.AddressLike, qty: int) -> int:
		"""Public price for token to ETH trades with an exact input."""
		price = None
		if log: print('VERSION', self.version)
		if self.version == 'v1':
			ex = self.exchange_contract(token)
			call = ex.functions.getTokenToEthInputPrice
			params = {'qty': qty}
			price = self.makeCall(call, params)
		elif self.version == 'v2':
			call = self.router.functions.getAmountsOut
			weth = addresses.AddrO(self.get_weth_address()).str_address
			args = [int(qty), [token, weth]]
			response = self.makeCall(call, args)
			if log: print('Response', response)
			if response:
				price = response[-1]
		else:
			if log: print('Need to work on Uniswap version 3')
		return price

	def get_token_token_input_price(self, token0, token1, qty, prec0=18, prec1=18) -> int:
		"""Public price for token to token trades with an exact input."""
		token0 = addresses.AddrO(token0)
		token1 = addresses.AddrO(token1)
		token0.precision, token1.precision = prec0 , prec1
		weth = self.get_weth_address()
		if evm.is_same_address(token0.str_address, weth):#redirect for WETH/ETH
			if self.checkPair(token1.str_address, weth):
				cqty = int(qty * float(f'1e{token1.precision}'))
				value = self.get_eth_token_input_price(token1.str_address, cqty)
				if value != None:
					return int(value) * float(f'1e-{token0.precision}') / qty
		elif evm.is_same_address(token1.str_address, weth):
			if self.checkPair(token0.str_address, weth):
				cqty = int(qty * float(f'1e{token0.precision}'))
				value = self.get_token_eth_input_price(token0.str_address, cqty)
				if value != None:
					return int(value) * float(f'1e-{token1.precision}') / qty
		else:
			#this price isn't an optimized routing it is routing through ETH which is why prices can be off some times
			#need to create a route multiplexer
			route = [token0.str_address, weth, token1.str_address]
			if self.checkPair(token0.str_address, weth):
				if self.checkPair(weth, token1.str_address):
					cqty = int(qty * float(f'1e{token0.precision}'))
					try:
						data = self.router.functions.getAmountsOut(cqty, route).call()
						price: int = data[-1]
						return price * float(f'1e-{token1.precision}') / qty
					except:
						return 0
		return 0

	def get_eth_token_output_price(self, token: evm.AddressLike, qty: int) -> evm.Wei:
		"""Public price for ETH to Token trades with an exact output."""
		if self.version == 'v1':
			ex = self.exchange_contract(token)
			price: Wei = ex.functions.getEthToTokenOutputPrice(qty).call()
		else:
			price = self.router.functions.getAmountsIn(qty, [self.get_weth_address(), token]).call()[0]
		return price

	def get_token_eth_output_price(self, token: evm.AddressLike, qty: evm.Wei) -> int:
		"""Public price for token to ETH trades with an exact output."""
		if self.version == 'v1':
			ex = self.exchange_contract(token)
			price: int = ex.functions.getTokenToEthOutputPrice(qty).call()
		else:
			price = self.router.functions.getAmountsIn(qty, [token, self.get_weth_address()]).call()[0]
		return price

	def get_token_token_output_price(self, token0: evm.AnyAddress, token1: evm.AnyAddress, qty: int) -> int:
		"""Public price for token to token trades with an exact output."""
		# If one of the tokens are WETH, delegate to appropriate call.
		# See: https://github.com/shanefontaine/uniswap-python/issues/22
		# TODO: Will these equality checks always work? (Address vs ChecksumAddress vs str)
		if evm.is_same_address(token0, self.get_weth_address()):
			return int(self.get_eth_token_output_price(token1, qty))
		elif evm.is_same_address(token1, self.get_weth_address()):
			return int(self.get_token_eth_output_price(token0, qty))
		price: int = self.router.functions.getAmountsIn(qty, [token0, self.get_weth_address(), token1]).call()[0]
		return price

	def getPair(self, token0, token1):
		''' '''
		pair = self.factory.functions.getPair(token0, token1)
		return self

	def getPoolValue(self, t0, t1):
		''' '''
		if t0 == 'ETH':
			vt0 = self.get_ex_eth_balance(t0)
		else:
			vt0 = self.get_ex_token_balance(t0)
		if t1 == 'ETH':
			vt1 = self.get_ex_eth_balance(t1)
		else:
			vt1 = self.get_ex_token_balance(t1)
		self.pair = [vt0, vt1]
		self.rate = float(vt0/vt1)
		return self

	def get_ex_eth_balance(self, token: evm.AddressLike) -> int:
		"""Get the balance of ETH in an exchange contract."""
		ex_addr: evm.AddressLike = self.exchange_address_from_token(token)
		return self.w3.evm.getBalance(ex_addr)

	def get_ex_token_balance(self, token: evm.AddressLike) -> int:
		"""Get the balance of a token in an exchange contract."""
		erc20 = self.erc20_contract(token)
		balance: int = erc20.functions.balanceOf(self.exchange_address_from_token(token)).call()
		return balance

	def processEPinfura_a000(self, qty, bdf, rdr, wrtr, table, terms: dict={}, params: dict={}, actions: list=[]):
		'''need to build this around an endpoint esque request to be more tightly
			integrated with worldbridge.engine
			non functional'''
		print('is this running')
		while True:
			data = next(rdr, None)#												||
			if data == None or data.dfs[table].empty:
				break
			df = data.dfs[table]
			print('Infura EP', df.columns)
			tokens = dict(zip(df['symbol'], df['address']))
			records = []
			bsymbols = list(terms.keys())
			bsymbols.reverse()#why in reverse?  cause i wanted WETH base at the top
			for bsymbol in bsymbols:
				baddress = terms[bsymbol]

				#base_precision = checkPrecision(baddress)

				bprecision = list(bdf.loc[bdf['address'] == baddress]['precision'])
				if bprecision not in ([''], [], [None]):
					bprecision = float(bprecision[0])
				else:
					bprecision = 0
				#this is a hack to get prices to print out properly...need to address correctly
				bsettle = list(bdf.loc[bdf['address'] == baddress]['settle'])
				if bsettle not in ([''], [], [None]):
					bsettle = float(bsettle[0])
				else:
					bsettle = 0
				tsymbols = list(tokens.keys())
				tsymbols.sort()
				for tsymbol in tsymbols:
					taddress = tokens[tsymbol]
					tprecision = list(df.loc[df['address'] == taddress]['precision'])
					if tprecision == [] or tprecision == [None] or tprecision == ['']:
						tprecision = 0
					else:
						tprecision = float(tprecision[0])
					tsettle = list(df.loc[df['address'] == taddress]['settle'])
					if tsettle != [] and tsettle != [None] and tsettle != ['']:
						tsettle = float(tsettle[0])
					else:
						tsettle = 0
					if tsymbol == '':
						tsymbol = taddress
					aqty = int(qty*float('1e'+str(int(bprecision-tprecision))))
#					try:
						#getEP()
					p = self.get_token_token_input_price(taddress,baddress,aqty)#	||
#					except Exception as e:
#						print('Error', e)
#						errortokens.append([taddress, 0])
#						continue
					p = p/(qty*float('1e'+str(int(bsettle-tsettle))))
					#print('STORE PRICE', tsymbol, p)
					# yield p
					# precord[tsymbol].append(p)
					now = thing.when()
					records.append([tsymbol, taddress, bsymbol, baddress, p, '', '',
									next(now.gen('store')), 'uniswap', 'infura'])#	||
			df = DataFrame(records, columns=cols)
			wrtr.write({'unis_quotes': df})

class TRX(Data):
	'''Interface with Uniswap Contracts providing an API for performing
		transactions '''
	def __init__(self, address: Union[str, evm.AddressLike]) -> None:
		''' '''
		self.config = condor.instruct(pxcfg).select('uniswap')
		#self.private_key = encryptor.engine().privatekey()#need to build out a password handling system
		uniswap.Data.__init__(address)

	def Approve(self, token: evm.AddressLike, max_approval: Optional[int] = None) -> None:
		"""Give an exchange/router max approval of a token."""
		max_approval = self.max_approval_int if not max_approval else max_approval
		contract_addr = (self.exchange_address_from_token(token) if self.version == 1 else self.router_address)
		function = self.erc20_contract(token).functions.approve(contract_addr, max_approval)
		tx = self._build_and_send_tx(function)
		self.w3.evm.waitForTransactionReceipt(tx, timeout=6000)
		# Add extra sleep to let tx propogate correctly
		time.sleep(1)

	def Swap(self, input_token, output_token, qty, recipient=None) -> evm.HexBytes:
		"""Make a trade by defining the qty of the input token."""
		if input_token == ETH_ADDRESS:
			return self._eth_to_token_swap_input(output_token, evm.Wei(qty), recipient)
		else:
			balance = self.get_token_balance(input_token)
			if balance < qty:
				raise InsufficientBalance(balance, qty)
			if output_token == ETH_ADDRESS:
				return self._token_to_eth_swap_input(input_token, qty, recipient)
			else:
				return self._token_to_token_swap_input(input_token, qty, output_token, recipient)

	def AddLiquidity(self):
		''' '''
		return self

	def RemoveLiquidity(self):
		''' '''
		return self

	def Revoke(self):
		'''Revoke permissions of Uniswap contract '''
		return self

	def _is_approved(self, token: evm.AddressLike) -> bool:
		"""Check to see if the exchange and token is approved."""
		_validate_address(token)
		if self.version == 1:
			contract_addr = self.exchange_address_from_token(token)
		else:
			contract_addr = self.router_address
		load = [self.address, contract_addr]
		amount = (self.erc20_contract(token).functions.allowance(*load).call())#||
		if amount >= self.max_approval_check_int:
			return True
		else:
			return False

def collectPools(db):
	'''Collect the value of all liquidity pools for a given set of tokens
		use this data to inform the creation of a route optimizer for price
		checking '''

def collectTokens(db: str, table: str):
	''' '''

def collectPricesByTokens(db: str, table: str, tokens: list=[]):
	''' '''
	process = 'getPricesByTokens'
	params = {'tokens': tokens}
	runCollect(process, db, params, table)

def runCollect(process, db, params, table):
	''' '''
	fx = Data(process, 'methodify', 'uniswap', db, 'db', table)
	fx.setReader('uniswap', params).collect({'table': [table]})


#===========================Code Source Examples================================||
'''
https://pypi.org/project/uniswap-python/
https://uniswap.org/docs/v2/smart-contracts/router02/

https://github.com/Uniswap/uniswap-api

https://github.com/Uniswap

https://blocklytics.org/blog/uniswap-api/


https://www.programmableweb.com/sdk/uniswap-python-sdk


https://docs.amberdata.io/reference


https://www.freelancer.com/contest/python-script-getting-data-from-uniswapio-competition-1723802?w=f&ngsw-bypass=

				# For v2 the address is the same on mainnet, Ropsten, Rinkeby, Görli, and Kovan
				# https://uniswap.org/docs/v2/smart-contracts/factory

		# If one of the tokens are WETH, delegate to appropriate call.
		# See: https://github.com/shanefontaine/uniswap-python/issues/22

compute trading pair
https://stackoverflow.com/questions/69940402/compute-the-lp-address-of-a-token-pair-using-web3-py

https://cryptomarketpool.com/use-web3-py-in-python-to-call-uniswap/

https://cryptomarketpool.com/get-market-data-from-uniswap-using-web3-py-in-python/

'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

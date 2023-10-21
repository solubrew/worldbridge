#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:  #																	||
	name:   #																	||
	description: >  #															||
		Aggregate evm compatiable data and functionality from both remote and
		local blockchain nodes and api services

		Interact and generate ERC-20 compliant token contracts
		NFT
		look at integration with NFT licensing project
	expirary: '<[expiration]>'  #												||
	version: '<[version]>'  #													||
	path: '<[LEXIvrs]>'  #														||
	outline: <[outline]>'  #													||
	authority: 'document|this'  #												||
	security: 'sec|lvl2'  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
# ==================================Core Modules=================================||
from os.path import abspath, dirname, join  # ||
from secrets import token_bytes
from typing import List, Union

# ===============================================================================||
from pandas import concat, DataFrame, to_datetime  # ||
# ===============================================================================||
# from web3.contract import ContractFunction
from web3.types import Wei, Address, ChecksumAddress, ENS, Nonce

try:
	from sha3 import keccak_256
except:
	print('No Sha3 import')
import hashlib
from coincurve import PublicKey
#===============================================================================||
from condor import condor#										||
from worldbridge import worldbridge
from worldbridge.web2.blockchain import etherscan
from worldbridge.web3.protocols import protocols, connect, addresses
from worldbridge.web3 import utils
#===============================================================================||
here = join(dirname(__file__),'')#												||
AddressLike = Union[Address, ChecksumAddress, ENS]
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/evm.yaml')

class EVMViewer(worldbridge.stone):
	'''The viewer provides methods to view aspects about the contracts and/or
		addresses loaded into the instance'''

	def __init__(self, network=1, w3=None, store=None, cfg={}):
		''' '''
		self.config = condor.instruct(pxcfg).select('ethereum')#.select('ethereum').override(cfg)
		self.ETH_ADDRESS = self.config.dikt['ETH_ADDRESS']
		self.network = utils.getNetwork(network)
		self.w3 = w3
		self.initW3(self.w3)
		self.addresses, self.balances, self.blockprovider = {}, {}, {}
		self.hasTRXs, self.hasTokens, self.contract = False, False, None
		worldbridge.stone.__init__(self, cfg)
		self.initBlockProvider()
		self.store = store
		self.initStore()

	def getAsset(self, addr=None, symbol=None, name=None):
		''' '''
		if addr:
			return addresses.lookupAddress(addr)
		if symbol:
			return addresses.lookupSymbol(symbol)
		if name:
			return addresses.lookupName(name)

	def getBalance(self, token='ETH', addr=None):
		'''Get Balance of wallet by address or public key'''

	def getBalances(self, addr):
		''' '''
		self.getETHBalance(addr)
		self.getTokensBalance(addr)
		return self

	def getETHBalance(self, addr) -> Wei:
		"""Get the balance of ETH in a wallet."""
		self.balances['ETH'] = self.w3.eth.getBalance(addr)*float(f'1e-18')
		return self

	def getLastBlock(self):
		''' '''
		return 0

	def getNextNonce(self):
		''' '''
		self.last_nonce: Nonce = self.w3.eth.getTransactionCount(self.address)
		return self.last_nonce + 1

	def getPublicKey(self):
		'''Get the Public Key of the address '''

	def getTokenBalance(self, token: AddressLike, address: AddressLike, precision=18) -> int:
		"""Get the balance of a token in a wallet."""
		token = protocols.Token(token)
		if  token.address.str_address == self.ETH_ADDRESS:
			return self.get_eth_balance()
		self.contract = token.initW3(self.w3).loadContract().contract
		try:
			balance: int = self.contract.functions.balanceOf(address).call()
			balance = balance*float(f'1e-{precision}')
		except Exception as e:
			if log: print(f'Get Balance failed {e}')
			return 0
		return balance

	def getTokens(self, addr=None, chain='eth'):
		''' '''
		if not addr:
			addr = self.addresses[list(self.addresses.keys())[0]].str_address
		if not self.hasTRXs:
			self.getTransactions(addr)
		self._extractTokens(chain)
		return self

	def getTokensBalance(self, addr: AddressLike, tokens: List=[]):
		'''Get the balance of each token in a a specific address registered
			with the wallet instance '''
		if tokens == [] and not self.hasTokens:
			self.getTokens(addr)
		df = concat([self.tokens, self.nfts])
		for i, r in df.iterrows():
			taddr = r['contractaddress']
			prec = r['precision']
			self.balances[r['token']] = self.getTokenBalance(taddr, addr, prec)
			self.cache.store['balances'] = self.balances
		self.contract = None
		return self

	def getTransactions(self, addrs, blocknum=0, c='eth'):
		'''This doesnt work as the columns of each calls returned data is
			different currently this works in NchantdMoonBags because of the
			use of the central database and a vw combining each of these tables
			either implement this in the cache or work with the tables
			seperately '''
		if not isinstance(addrs, list):
			addrs = [addrs]
		chains = {'eth': 'etherscan', }#'matic', ''}
		params = {'addresses': addrs, 'startblock': blocknum}
		actions = {f'trxs_{c}': 'txlist', f'erc20trxs_{c}': 'tokentx',
										f'erc721trxs_{c}': 'tokennfttx',
										f'itrxs_{c}': 'txlistinternal'}#	||
		load, cols = ['getTrxsByAddresses', 'methodify', 'etherscan'], []
		self.blockprovider[c].initSource(*load)
		self.blockprovider[c].initCache()
		for table, action in actions.items():
			params['action'] = action
			self.blockprovider[c].setReader(params, chains[c])#
			self.blockprovider[c].initExtract(cols, 'dataframe', table)
			self.blockprovider[c].extract(table)
		trxs = self._combineTransactions()
		trxs['datetime'] = to_datetime(trxs['timestamp'].astype(int), unit='s')
		if log: print('Timestamp', trxs['timestamp'])
		if log: print('Datetime', trxs['datetime'])
		trxs['year'] = trxs['datetime'].dt.year
		trxs['month'] = trxs['datetime'].dt.month
		trxs['day'] = trxs['datetime'].dt.day
		trxs['hour'] = trxs['datetime'].dt.hour
		trxs['minute'] = trxs['datetime'].dt.minute
		self.transactions = trxs
		if log: print('TRXs', trxs)
		self.hasTRXs = True
		return self

	def getTransaction(self, blocknum):
		'''Get Transaction by Transaction id or block number'''
		return self

	def initW3(self, w3=None):
		if self.w3:
			return self
		if not w3:
			if log: print('Initialize EVMViewer for Address Object')
			w3 = connect.connect(self.network)
		self.w3 = w3
		return self

	def initBlockProvider(self):
		''' '''
		self.blockprovider['eth'] = etherscan.Data()
		#self.blockprovider['matic'] = polyscan.Data()
		#self.blockprovider['arb1'] = arbiscan.Data()
		#self.blockprovider['avax'] = snowtrace.Data()
		return self

	def initStore(self):
		''' '''
		if self.store == None:
			self.initCache()
		return self

	def loadTokens(self, tokens):
		''' '''
		self.tokens = tokens
		self.hasTokens = True
		return self

	def loadTrxs(self, trxs):
		self.trxs = trxs
		self.hasTRXs = True

	def makeCall(self, call, args=[], kwargs={}):
		''' '''
		try:
			output = call(*args, **kwargs).call()
		except Exception as e:
			print(f'Call execution {call} failed due to {e}')
			return None
		return output

	def _combineTransactions(self, c='eth'):
		''' '''
		try:
			self.trxs = self.blockprovider[c].cache.store[f'trxs_{c}']
		except Exception as e:
			self.trxs = DataFrame()
		self.itrxs = self.blockprovider[c].cache.store[f'itrxs_{c}']
		self.erc20trxs = self.blockprovider[c].cache.store[f'erc20trxs_{c}']
		self.erc721trxs = self.blockprovider[c].cache.store[f'erc721trxs_{c}']
		df = concat([self.trxs, self.itrxs, self.erc20trxs, self.erc721trxs])
		df.to_csv('/home/solubrew/Downloads/2022_trxs.csv')
		return df

	def _extractTokens(self, c):
		''' '''
		erc20s = self.blockprovider[c].cache.store[f'erc20trxs_{c}']
		cols = list(erc20s.columns)
		cols.pop(cols.index('token'))
		cols.pop(cols.index('contractaddress'))
		cols.pop(cols.index('precision'))
		self.tokens = erc20s.drop(cols, axis=1).drop_duplicates()
		erc721s = self.blockprovider[c].cache.store[f'erc721trxs_{c}']
		cols = list(erc721s.columns)
		cols.pop(cols.index('token'))
		cols.pop(cols.index('contractaddress'))
		cols.pop(cols.index('precision'))
		self.nfts = erc721s.drop(cols, axis=1).drop_duplicates()
		self.cache.store['nfts'] = self.nfts
		self.cache.store['tokens'] = self.tokens
		return self

class EVMReader(EVMViewer):
	'''The reader provides methods to read data from onchain using the contracts
		and/or addresses loaded into the instance'''
	def __init__(self, network=1, w3=None, store=None, cfg={}):
		''' '''
		EVMViewer.__init__(self, network, w3, store, cfg)

	def buildTransaction(self):
		''' '''
		return tx

	def initContractAddress(self, address):
		'''Add a given address to the contracts dictionary attribute '''
		if address not in self.contracts.keys():
			self.contracts[address] = {}
		return self

	def readContract(self):
		''' '''
		return self

	def loadABI(self, abi=[], address=None):
		''' '''
		if address == None:
			self.abi = abi
		else:
			self.initContract(address)
			self.contracts[address]['abi'] = abi
		return self

	def loadContract(self, address, abi={}):
		''' '''
		self.initContract(address)
		self.contracts[address]['address'] = makeAddress(contract)
		if 'abi' not in self.contracts[address].keys():
			self.contracts[address]['abi'] = self.abi
		return self

class EVMWriter(EVMReader):
	'''The writer provides methods to make changes to the chain using the
	contracts and/or addresses loaded into the instance.  These methods will
	require access to a private key in order to minimize errors this class will
	be limited to ineracting with one contract at a time requiring usage of
	muliple contracts to have their own instance'''
	def __init__(self, network=1, w3=None, store=None, cfg={}):
		''' '''
		EVMReader.__init__(self, network, w3, store, cfg)

	def createPrivateKey(self, pword):
		'''Create a private key and encrypt using passed pword'''
		pkey, addr = createPrivateKey()
		return encode(pkey), addr

	def deployContracts(self, path):
		''' '''

	def signTransaction(self, trx):
		''' '''

	def signMessage(self, msg):
		''' '''

	def sendTokens(self, to, frm=''):
		''' '''

	def _genPrivateKey(self):
		''' '''

	def _genRecoveryPhrase(self):
		''' '''

def createPrivateKey():
	'''Generate a Private Key, Address key set'''
	#pkey = keccak_256(token_bytes(32)).digest()
	pkey = hashlib.sha_256(token_bytes(32)).digest()
	public = PublicKey.from_valid_secret(pkey).format(compressed=False)[1:]
	#addr = keccak_256(public).digest()[-20:].hex()
	addr = haslib.sha_256(public).digest()[-20:].hex()
	return pkey.hex(), addr

#===========================Code Source Examples================================||
#================================:::DNA:::======================================||
'''
integrate link price aggregation
https://docs.chain.link/docs/architecture-decentralized-model/
'''

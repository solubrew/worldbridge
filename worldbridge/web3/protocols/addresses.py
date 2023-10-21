#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: '95a312d0-9f71-4f69-979e-121c71466412'  #							||
	name:   #														||
	description: >  #															||
	expirary: '<[expiration]>'  #												||
	version: '<[version]>'  #													||
	path: '<[LEXIvrs]>'  #														||
	authority: 'document|this'  #												||
	security: 'sec|lvl2'  #														||
	<(WT)>: -32  #																||
''' #																			||
import json as j  # ||
# -*- coding: utf-8 -*-#														||
# ==================================Core Modules=================================||
from os.path import abspath, dirname, join  # ||
from typing import Union

# ===============================================================================||
from condor import condor  # ||
from squirl.orgnql import sonql
from web3 import Web3
# ===============================================================================||
# ===============================================================================||
# from web3.contract import ContractFunction
from web3.types import Address, ChecksumAddress, ENS

from worldbridge.web3.protocols.protocols import BASE

AddressLike = Union[Address, ChecksumAddress, ENS]
_netid_to_name = {1: "mainnet", 4: "rinkeby"}
#===============================================================================||
here = join(dirname(__file__),'')#												||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/address.yaml')


class AddrO(BASE):
	'''Addresse Object for supplying various configurations of an address as
		needed'''
	def __init__(self, addr, chainid=1, cfg={}, data=None):
		'''Create basic address object attributes using default configurations
			'''
		self.config = condor.instruct(pxcfg).select('Address').override(cfg)
		str_addr = makeStringAddress(addr, chainid, data)
		addr: AddressLike = makeAddress(str_addr, chainid)
		self.address = addr
		self.str_address = str_addr
		self.balances, self.w3, self.abi = {}, None, None

	def getABI(self, c='eth'):
		'''Retrieve ABI from blockprovider for the given chain'''
		self.connectEVM(1, 0, 0)
		self.evm.blockprovider[c].initCache()
		yldr = self.evm.blockprovider[c].getABIsByAddresses([self.str_address])
		abi = next(yldr)
		return j.loads(self.evm.blockprovider[c].cache.store[None])

	def getContract(self, abi=None):
		'''Any address may have a contract associated with it. attempt to get
			contract from address with known ABI '''
		self.initW3()
		return self.w3.eth.contract(address=self.str_address, abi=abi)

	def getEvents(self):
		''' '''
		return self

	def decodeEvent(self):
		''' '''
		for event in abi_events:
			name = event['name']
			inputs = []
			inputs = [param["type"] for param in event["inputs"]]
			inputs = ",".join(inputs)
			# Hash event signature
			event_signature_text = f"{name}({inputs})"
			event_signature_hex = web3.toHex(web3.keccak(text=event_signature_text))
			# Find match between log's event signature and ABI's event signature
			if event_signature_hex == receipt_event_signature_hex:
				# Decode matching log
				decoded_logs = contract.events[event["name"]]().processReceipt(receipt)


def getAssetData():
	'''Get asset data from local database'''
	spath = 'protocols/_data_/assets.db'#
	db = join(abspath(join(dirname(abspath(__file__)), '..')), spath)
	if log: print('Asset DB', db)
	data = next(sonql.doc(db).read({'view': ['vw_assets']}))
	df = data.dfs['vw_assets']
	return df

def lookupAddress(symbol, chainid=1, assets=None):
	'''Search symbol to get address '''
	if assets == None:
		assets = getAssetData()
	row = assets.loc[(assets['symbol'] == symbol.upper()) &
										(assets['chainid'] == str(chainid))]
	row = row.reset_index(drop = True)
	try:
		addr = row.loc[0]['address']
	except Exception as e:
		if log: print('Lookup failed', e, f'for {symbol}')
		addr = None
	return addr

def lookupName(addr, chainid=1, assets=None):
	'''Search Address to get Name '''
	if assets == None:
		assets = getAssetData()
	row = assets.loc[(assets['address'] == addr) &
										(assets['chainid'] == str(chainid))]
	row = row.reset_index(drop=True)
	try:
		name = row.loc[0]['name'].lower().replace(' ', '')
	except Exception as e:
		if log: print('Lookup failed', e, f'for {addr}')
		name = None
	return name

def lookupSymbol(addr, chainid=1, assets=None):
	'''Search Address to get Symbol'''
	if assets == None:
		assets = getAssetData()
	row = assets.loc[(assets['address'] == addr) &
										(assets['chainid'] == str(chainid))]
	row = row.reset_index(drop=True)
	try:
		symbol = row.loc[0]['symbol'].lower().replace(' ', '')
	except Exception as e:
		if log: print('Lookup failed', e, f'for {symbol}')
		symbol = None
	return name

def makeAddress(s: str, chainid=1) -> AddressLike:
	'''Make Checksum address '''
	if s == None:
		raise Exception(f'Address is None')
	if s.startswith('0x'):
		return Address(bytes.fromhex(s[2:]))
	elif s.endswith('.eth'):
		return ENS(s)
	else:
		raise Exception(f'Couldnt convert string {s} to AddressLike')

def makeStringAddress(a: AddressLike, chainid=1, data=None) -> str:
	'''Make String Address '''
	if isinstance(a, bytes):
		# Address or ChecksumAddress
		addr: str = Web3.to_checksum_address("0x" + bytes(a).hex())
	elif isinstance(a, str):
		if a.endswith(".eth"):
			# Address is ENS
			raise Exception("ENS not supported for this operation")
		elif a.startswith("0x"):
			addr = Web3.to_checksum_address(a)
		elif len(a) < 10:
			addr = lookupAddress(a, chainid, data)
		else:
			raise InvalidToken(a)
	else:
		if log: print(f'Make Address Failed {a}')
	return addr

def _validate_address(a: AddressLike) -> None:
	''' '''
	assert _addr_to_str(a)



#==============================Source Materials=================================||
'''

'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

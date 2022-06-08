#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
	name: #				||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	path: <[LEXIvrs]>  #														||
	outline: <[outline]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#================================Core Modules===================================||
import json, time, logging, functools
from os.path import abspath, dirname, join#										||
from os import listdir
import sys, types#																||
from typing import List, Any, Optional, Callable, Union, Tuple, Dict
#===============================================================================||
from condor import condor
from worldbridge.web3.chains import addresses, evm
from worldbridge import worldbridge
#===============================================================================||
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
where = abspath(join(''))#														||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/protocols.yaml')
class BASE(object):
	'''Base Blockchain Object that provides a connection to an evm interface '''
	def __init__(self, cfg={}):
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg)
		self.evm, self.w3 = None, None
		self.addresses = {}

	def connectEVM(self, view=1, read=0, write=0, network=1):
		'''A veiw connection provides EVM data and metadata about contracts
			a read connection provides EVM data via contract specific functions
			a write connection provides EVM access to write onchain data

			Initialize a web3 connection for the address object by either
			providing one from the requesting function or intializing a new
			one'''
		if write == 1:
			self.evm = evm.EVMWriter(network, None, None, self.config)
		elif read == 1:
			self.evm = evm.EVMReader(network, None, None, self.config)
		elif view == 1:
			self.evm = evm.EVMViewer(network, None, None, self.config)
		self.w3 = self.evm.w3
		return self

	def initAddress(self, addr:str, assets=None):
		''' '''
		self.addresses[addr] = {'obj': addresses.AddrO(addr, assets)}
		return self

	def initAddresses(self, addrs:list, assets=None):
		''' '''
		if not isinstance(addrs, list):
			addrs = [addrs]
		for addr in addrs:
			self.initAddress(addr, assets)
		return self

	def initW3(self, w3=None):
		''' '''
		if self.w3 == None:
			self.w3 = w3
		return self

	def _loadABI(self, name: str=None, asset: str=None, version: str=None) -> str:
		''' '''
		if log: print('Name', name, 'Asset', asset)
		spath = 'protocols/_data_/assets/'
		path = join(abspath(join(dirname(abspath(__file__)), '..')), spath)
		if name == None:
			name, asset, version = 'erc20', 'erc', 'v1'
		#correct this path of assets to the protocols _data_ by protocol
		with open(abspath(f"{path}{asset}-{version}/{name}.abi")) as f:
			abi: str = json.load(f)
		return abi

class Token(BASE):
	''' '''
	def __init__(self, address, symbol=None, asset=None, version='v1', cfg={}):
		''' '''
		self.config = condor.instruct(pxcfg).select('Token').override(cfg)
		BASE.__init__(self, self.config)
		self.symbol = symbol
		self.address = address
		if not isinstance(self.address, addresses.AddrO):
			self.address = addresses.AddrO(self.address)
		#self.asset = self.evm.getAsset(self.address)
		self.abi = json.loads(str(self.config.dikt.get('abi')))

	def buildAttributes(self):
		''' '''
		calls = self.contract.caller.__dir__()
		for call in calls:
			attr(self, call)
		return self

	def loadContract(self):
		''' '''
		self.address.initW3(self.w3)
		self.contract = self.address.getContract(self.abi)
		return self

def checkPrecision(token):
	'''Check for precision stored locally and if not get from chain and store
	locally for futre use'''
	pxcfg = f'{here}z-data_/ethereum.yaml'
	config = condor.instruct(pxcfg).select(['modules', 'checkPrecision'])
	store = store.doc(config.dikt['location'])
	precisiontree = store.read().index('address')
	if token in precisiontree.keys():
		return precisiontree[token]
	precision = getPrecision(token)
	store.write({token: precision})
	return precision

def getPrecision(token):
	'''Get Precision from chain'''

def loadProtocol(address, assets):
	'''Given an address return the appropriate protocol  '''
	#access asset lookup database use address to get information
	#then look for explicit protocol availability
	#if not default to a generic protocol
	#

def loadToken(address, assets=None):
	'''Given token address search database for protocol
		if found check that protocol is defined in the protocols by its
		name bloom filtered on first letter if protocol '''
	if assets == None:
		assets = addresses.getAssetData()

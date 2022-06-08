#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:  #														||
	name:   #														||
	description: >  #															||
		Interact and generate ERC-20 compliant token contracts
	expirary: '<[expiration]>'  #												||
	version: '<[version]>'  #													||
	path: '<[LEXIvrs]>'  #														||
	outline: <[outline]>'  #													||
	authority: 'document|this'  #												||
	security: 'sec|lvl2'  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#==================================Core Modules=================================||
#================================3rd Party Modules==============================||
#===============================================================================||
from worldbridge.web3.ethereum import EthereumBridge
from worldbridge.web3.protocols.protocols import Token
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = join(dirname(__file__))
where = abspath(join('..'))#													||set path at pheonix level
module_path = abspath(join('../../../'))
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/erc20.yaml')
class ERC20(Token):
	''' '''
	def __init__(self, symbol, address, asset=None, cfg={}):
		''' '''
		self.config = condor.instruct(pxcfg).select('ERC20').override(cfg)
		self.address = addresses.AddrO(address)
		if asset == None:
			asset = 'erc20'
		self.asset = asset
		super(ERC20, self).__init__(symbol, self.address, self.asset)
		self.version = version
		abi = self.config.dikt.get('abi')
		if abi:
			self.abi = abi

	def loadTransactions(self):
		'''Get all transactions related to this ERC-20 token '''
		return

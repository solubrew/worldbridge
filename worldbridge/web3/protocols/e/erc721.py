#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:  #														||
	name:   #														||
	description: >  #															||
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

# ================================3rd Party Modules==============================||
# ===============================================================================||
from condor import condor

from worldbridge.web3.protocols import addresses
from worldbridge.web3.protocols.protocols import Token

#===============================================================================||
here = join(dirname(__file__),'')#												||
there = join(dirname(__file__))
where = abspath(join('../..'))  # ||set path at pheonix level
module_path = abspath(join('../../../../'))
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '../_data_/erc721.yaml')


class ERC721(Token):
	''' '''
	def __init__(self, symbol, address, asset=None, cfg={}):
		''' '''
		self.config = condor.instruct(pxcfg).select('ERC721').override(cfg)
		if log: print('ERC721 address')
		self.address = addresses.AddrO(address)
		if log: print('ERC721 address', self.address.__dir__())
		if asset == None:
			asset = 'ERC721'
		self.asset = asset
		super(ERC721, self).__init__(symbol, self.address, self.asset)
		abi = self.config.dikt.get('abi')
		if abi:
			self.abi = abi

	def baseURI(self):
		''' '''
		try:
			return self.contract.caller.baseURI()
		except Exception as e:
			if log: print(f'No Contract URI {e}')
		try:
			return self.contract.caller.contractURI()
		except Exception as e:
			if log: print(f'No Contract URI {e}')
	def name(self):
		''' '''
		return self.contract.caller.name()

	def metadata(self):
		''' '''
		metadata = self.contract.caller.metadata()
		if metadata == None:
			pass

	def symbol(self):
		''' '''
		return self.contract.caller.symbol()

	def tokenURI(self, tokenid=0):
		''' '''
		return self.contract.caller.tokenURI(tokenid)

	def getURIAssets(self):
		''' '''
		return

	def loadTransactions(self):
		'''Get all transactions related to this ERC-721 collection '''
		return

def buildStd(path, name):
	''' '''
	cfg = condor.instruct(path).select(name).dikt
	token = Token()
	return token

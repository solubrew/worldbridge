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

from worldbridge.web3.chains.ethereum import Token

#===============================================================================||
here = join(dirname(__file__),'')#												||
there = join(dirname(__file__))
where = abspath(join('../..'))  # ||set path at pheonix level
module_path = abspath(join('../../../../'))
version = '0.0.0.0.0.0'#														||
page = 200000
#===============================================================================||
pxcfg = f'{here}_data_/erc1155.yaml'
class ERC721(Token):
	''' '''
	def __init__(self, symbol, address, asset=None, cfg={}):
		''' '''
		self.address = address
		if asset == None:
			asset = 'erc1155'
		self.asset = asset
		self.config = condor.instruct(pxcfg).select('ERC1155').override(cfg)
		super(ERC1155, self).__init__(symbol, self.address, self.asset)

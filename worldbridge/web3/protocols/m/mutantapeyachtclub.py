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
from worldbridger.web3.chains import ethereum as eth
from worldbridger.web3.protocols.erc721 import ERC721
from worldbridger import worldbridger
#===============================================================================||
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
where = abspath(join(''))#														||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/mutantapeyachtclub.yaml')
class MAYC(ERC721):
	'''Bored Ape Yacht Club Data Source '''
	def __init__(self, version=1, cfg: dict={}) -> None:
		''' '''
		self.config = condor.instruct(pxcfg).select('MAYC').override(cfg)
		self.version = version
		self.data = self.config.dikt['token'][self.version]
		self.asset = self.data['name'].lower().replace(' ', '')
		self.address = self.data.get('address')
		load = ['MAYC', self.address, self.asset, self.version, self.abi]
		if log: print('Initialize ERC721')
		ERC721.__init__(self, *load)
		abi = self.data.get('abi', None)
		if abi:
			self.abi = abi

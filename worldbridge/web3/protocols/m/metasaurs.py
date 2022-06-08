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
from worldbridger.web3.tokens.erc721 import ERC721
from worldbridger import worldbridger
#===============================================================================||
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
where = abspath(join(''))#														||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = False
#===============================================================================||
class MTS(erc721.ERC721):
	'''Bored Ape Yacht Club Data Source '''
	def __init__(self, cfg: dict={}) -> None:
		''' '''
		self.config = condor.instruct(pxcfg).select('mtsSRC').override(cfg)
		erc721.ERC721.__init__(self, self.config)
		self.token = ERC721('MTS', self.address, self.asset, self.version)
		self.version = self.config.dikt['version']
		self.asset = self.token.name().lower()
		self.address = self.config.dikt['address']

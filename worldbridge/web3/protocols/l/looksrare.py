#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: '7d5e7d47-bcd0-4a51-8f83-b2cb93aac32d'  #							||
	name: Worldbridge Web3 Protocol LooksRare Python Document  #				||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	path: <[LEXIvrs]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#================================Core Modules===================================||
import functools, json as j, logging, sys, time, types
from os.path import abspath, dirname, join#										||
from os import listdir
from typing import List, Any, Optional, Callable, Union, Tuple, Dict
#===============================================================================||
from pandas import DataFrame#													||
from condor import condor, thing
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
pxcfg = join(abspath(here), '_data_/looksrare.yaml')
class Data(evm.EVMViewer):
	'''LooksRare Data Source '''
	def __init__(self, network=1, conx=None, store=None, cfg: dict={}) -> None:
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg)
		evm.EVMViewer.__init__(self, network, conx, None, self.config)
	def getPrice(self):
		''' '''

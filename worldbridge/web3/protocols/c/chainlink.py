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
from worldbridger.bridge import ethereum as eth
from worldbridger import worldbridger
#===============================================================================||
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
where = abspath(join(''))#														||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = False
#===============================================================================||
pxcfg = f'{here}_data_/erc20.yaml'
class Data(eth.EVMViewer):
	'''StrongBlock Data Source '''
	def __init__(self, cfg: dict={}) -> None:
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg)
		eth.EVMViewer.__init__(self, self.config)
def getOraclePrice(price_feed_address):
	'''Get Prices from Link Oracle given the price feed address'''
	price_feed_data = interfaces.link.iAggregatorV3(price_feed_address)
	price = price_feed_data.latestRound()[1]
	return float(Web3.fromWei(price, 'ether'))

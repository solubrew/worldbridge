#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: '6f3098ed-9ce5-4ff2-8554-bdaee787fae2'  #							||
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
pxcfg = join(abspath(here), '_data_/sushiswap.yaml')
class Data(evm.EVMViewer):
	'''Uniswap Data Source '''
	def __init__(self, network=1, conx=None, store=None, cfg: dict={}) -> None:
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg)
		evm.EVMViewer.__init__(self, network, conx, None, self.config)
		self.version = self.config.dikt['cfg']['version']# TODO: Write tests for slippage
		self.max_slippage = self.config.dikt['cfg']['max_slippage']
		self.protocols = self.config.dikt['protocols']
		factory = self.protocols['factory'][self.version]
		faddr =  addresses.AddrO(factory['networks'][self.network])
		abi = j.loads(factory['abi'])
		self.factory = faddr.initW3(self.w3).getContract(abi)
		if self.version in ('v2', 'v3'):
			router = self.protocols['swap'][self.version]
			raddr = addresses.AddrO(router['networks'][self.network])
			abi = j.loads(router['abi'])
			self.router = raddr.initW3(self.w3).getContract(abi)

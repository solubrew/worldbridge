# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:  #														||
	name:   #														||
	description: >  #															||
		Build out a SRC module to interact with the etherscan API to be used in
		extraction of ethereum centric data
		turn endpoint data into dataframes for consumption
		leveraging the worldbridge class there is no need to integrate
		database lookups here as this will act as a deeper component of the data
		repository system that will be accessed by outside systems

	expirary: '<[expiration]>'  #												||
	version: '<[version]>'  #													||
	authority: 'document|this'  #												||
	security: 'sec|lvl2'  #														||
	<(WT)>: -32  #																||
'''  # ||
# -*- coding: utf-8 -*-#														||
# ==================================Core Modules=================================||
from os.path import abspath, dirname, join
from pandas import concat, DataFrame
from requests import get, Request, Session
import json, time, inspect
# ===============================================================================||
from condor import condor
from excalc import tree as calctr
from squirl.orgnql import sonql  # this should be replaced by collector actions
from worldbridge import worldbridge
from worldbridge.web3.chains import ethereum as eth

# ===============================================================================||
here = join(dirname(__file__), '')  # ||
log = True
# ===============================================================================||
pxcfg = join(abspath(here), '_data_/blockchain.yaml')  # ||use default configuration

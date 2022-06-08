#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:  #														||
	name:   #														||
	description: >  #															||
	expirary: '<[expiration]>'  #												||
	version: '<[version]>'  #													||
	authority: 'document|this'  #												||
	security: 'sec|lvl2'  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#==================================Core Modules=================================||
from os.path import abspath, dirname, join#										||
#===============================================================================||
from web3 import Web3, HTTPProvider
#===============================================================================||
from condor import condor#										||
from rhino.ossys import linux
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
where = abspath(join(''))#														||set path at pheonix level
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/http.yaml')

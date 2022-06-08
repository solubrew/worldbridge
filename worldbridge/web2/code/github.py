#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: <^[uuid]^>
	name:
	description: >
	expirary: <[expiration]>
	version: <[version]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
from os.path import abspath, dirname, join
from os import listdir
#=======================================================================||
from fxsquirl import fxsquirl
from rhino.versys import git
#=======================================================================||
here = join(dirname(abspath(__file__)),'')#						||
there = abspath(join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
log = True
#=======================================================================||
pxcfg = join(abspath(here), '_data_/github.yaml')

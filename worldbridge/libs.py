#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid:
	name: Worldbridger Libraries Module Python Document
	description: >
	expirary: <^[expiration]^>
	version: <^[version]^>
	path: <[LEXIvrs]>pheonix/fxsquirlcules/collector/collector.py
	outline: <[outline]>
	authority: document|this
	security: seclvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, join
#===============================================================================||
here = join(dirname(__file__),'')#						||
there = abspath(join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
log = False
#===============================================================================||
try:
	from memory_profiler import profile
except:
	profile = None
	if log: print('No Memory Profiler Module Installed')
#from guppy3 import hpy; hp=hpy()

from pandas import DataFrame#													||

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: ''
	name: Module Python Document
	description: >
	expirary: <[expiration]>
	version: <[version]>
	authority: document|this
	security: seclvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, exists, expanduser, isdir, join#			||
from sys import argv, path#														||
#===============================================================================||
from condor import condor, thing#												||
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
log = True#																		||
#===============================================================================||
pxcfg = join(abspath(here), '_data_/gitlab.yaml')

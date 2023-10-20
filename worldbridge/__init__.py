#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid:
	name:
	description: >
	expirary: <[expiration]>
	Version: <[Version]>
	path: <[LEXIvrs]>panda/LEXI/
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
from os.path import abspath, dirname, join
#===============================================================================||
from subtrix import thing#										||
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
where = abspath(join(''))#														||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = False
#===============================================================================||
#how to deal with this in a distributed package...ideally a switch would
#be made during the release sequence
PRJCFG = {}
PROFILE = False
def runProfile():
	if PROFILE:
		path = '/home/solubrew/Design/SB/Projects/Worldbridger'
		pxcfg = abspath(join(path,'0_Config','cfg.yaml'))#								|
		PRJCFG = thing.what(pxcfg).get().dikt
		if log: print('Worldbridger PRJCFG', PRJCFG)
		uuid = when().credtid()
		fp = open(f"{PRJCFG['project_log']}/cli_{uuid}.memlog", 'w+')
		profile(stream=fp)

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

def release():
	if log: print('Working Directory', f'{self.path}/5_OMEGA/{self.operation}')
	ctrlr.set_working_directory(f'{self.path}/5_OMEGA/{self.operation}')
	msg = 'ERAs Operation Automated Push'
	status = ctrlr.bashr('git add --all')
	if log: print('Git add Status', status)
	status = ctrlr.bashr(f'git commit -m "{msg}"')
	if log: print('Git commit Status', status)
	ctrlr.bashr('git push -u origin main')

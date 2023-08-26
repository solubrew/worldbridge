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
pxcfg = join(abspath(here), '_data_', 'pypi.yaml')

def release():
	if log: print('Working Directory', f'{self.path}/5_OMEGA/{self.operation}')
	ctrlr.set_working_directory(f'{self.path}/5_OMEGA/{self.operation}')
	msg = 'ERAs Operation Automated Push'
	status = ctrlr.bashr('git add --all')
	if log: print('Git add Status', status)
	status = ctrlr.bashr(f'git commit -m "{msg}"')
	if log: print('Git commit Status', status)
	ctrlr.bashr('git push -u origin main')

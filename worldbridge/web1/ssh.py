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
pxcfg = join(abspath(here), '_data_/ssh.yaml')
def portForward(device, user, ip, localport, remoteport):
	'''Create an ssh connection with device specified by .ssh/config name using
		.ssh/config file on linux systems and forward the remote port to the
		local port specified
		expand to allow for this to function on windows and other os'
	'''
	link, cnt = linux.linkage(), 0
	while True:
		if link.checkPort(ip, localport):
			break
		cmd = f'ssh -f {user}@{device} -L {localport}:{device}:{remoteport} -N'
		link.bashr(cmd, False)
		if cnt >= 3:
			return False
		cnt += 1
	return True

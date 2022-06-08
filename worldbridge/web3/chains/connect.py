#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:  #														||
	name:   #														||
	description: >  #															||

	expirary: '<[expiration]>'  #												||
	version: '<[version]>'  #													||
	path: '<[LEXIvrs]>'  #														||
	outline: <[outline]>'  #													||
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
from worldbridge.web1 import ssh
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
where = abspath(join(''))#														||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/connect.yaml')
def setNetwork(id):
	''' '''
	_netid_to_name = {1: "mainnet", 4: "rinkeby", 5: 'arbitrum', 137: 'polygon'}
	if isinstance(id, int):
		return _netid_to_name[id]
	return id

def connect(network=1, provider='erigon', cfg={}):
	'''Create a connection to a blockchain node with failover across all
		options	connection methods of HTTP, RPC, IPC, JSONRPC'''
	config = condor.instruct(pxcfg).override(cfg)
	user = config.session.prime
	#netid = int(self.w3.net.version)
	network = setNetwork(network)
	providers = config.dikt['networks'][network]['providers']
	if provider in ('erigon', 'infura'):
		user = 'solubrew'
		device = 'SBEN0001'
		w3 = connectHTTP(providers, user, device)
	if log: print(f'Provider Used {provider}')
	return w3

def connectHTTP(providers, user=None, device=None):
	''' '''
	w3 = None
	try:
		w3 = connectErigon(providers['erigon'], user, device)
	except Exception as e:
		if log: print(f'Erigon connection failed due to {e}')
		try:
			w3 = connectInfura(providers['infura'])
		except Exception as e:
			if log: print(f'Infura connection failed due to {e}')
	return w3

# def connectIPC():
# 	''' '''
# 	w3 = Web3(Web3.IPCPProvider(''))
# 	return w3
#
# def connectWS():
# 	''' '''
# 	w3 = Web3(Web3.WebsocketProvider(f'ws://{ip}:{port}'))
# 	return w3

def connectErigon(provider, user=None, device=None):#need to push that out sesh
	''' '''
	url = f"{provider['path']}{provider['ip']}:{provider['port']}"
	load = [device, user, provider['ip'], provider['port'], provider['port']]
	if not ssh.portForward(*load):
		raise Exception(f'Local Port Not Connected')
	w3 = Web3(Web3.HTTPProvider(url, request_kwargs={"timeout": 60}))
	return w3

def connectInfura(provider):
	''' '''
	url = provider['path']
	w3 = Web3(Web3.HTTPProvider(url, request_kwargs={"timeout": 60}))
	return w3

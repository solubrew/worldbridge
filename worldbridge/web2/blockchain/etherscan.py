#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
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
''' #																			||
# -*- coding: utf-8 -*-#														||
#==================================Core Modules=================================||
from os.path import abspath, dirname, join
from pandas import concat, DataFrame
from requests import get, Request, Session
import json, time, inspect
#===============================================================================||
from condor import condor
from excalc import tree as calctr
from squirl.orgnql import sonql#this should be replaced by collector actions
from worldbridge import worldbridge
from worldbridge.web3.chains import ethereum as eth
#===============================================================================||
here = join(dirname(__file__),'')#												||
log = False
#===============================================================================||
pxcfg = join(abspath(here), '_data_/blockchain.yaml')#									||use default configuration


class Data(worldbridge.stone):
	'''Etherscan Data Source'''

	def __init__(self, cfg: dict={}):
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg).select('etherscan')
		worldbridge.stone.__init__(self, self.config)

	def getBalancesByAddresses(self, addresses: list):
		'''Get balances for address for eth and tokens '''
		actions = ['balancemulti']
		if len(addresses) < 2:
			actions = ['balance', 'tokenbalance']
		val = ''
		for x in addresses:
			val += f'{x},'
		val = val[:len(val)-1]
		params = {'module': 'account', 'tag': 'latest', 'apikey': self.apikey}
		name = inspect.currentframe().f_code.co_name
		load = [{'address': val}, params, actions, {}, name]
		return self.processEPetherscan(*load)

	def getABIsByAddresses(self, addresses: list):
		''' '''
		bys = {'address': addresses}
		params = {'module': 'contract'}
		action = 'getabi'#														||
		name = inspect.currentframe().f_code.co_name
		return self.processEPetherscan(bys, params, action, name)

	def getContractsByAddresses(self, addresses: list, action='getsourcecode',
																name='base'):#	||
		''' '''
#		print('Get Contract for Addresses', addresses)
		bys = {'address': addresses}
		params = {'module': 'contract', }
		cfgn = inspect.currentframe().f_code.co_name
		return self.processEPetherscan(bys, params, action, cfgn, name)

	def getLastBlock(self, state: str='live'):
		'''Get Last Block of Transactions '''
		self.getTrxsByBlocks([self.getLastBlockNumber(state)])#			||
		return self.df

	def getLastBlockNumber(self, state: str='stale'):
		'''Get the Last Block Number for the appropriate datasource based on
		 	request parameters'''
		self.state = state
		try:
			if state == 'stale':
				data = next(sonql.doc(self.db).read({'views': ['lastblocknumber']}))
				dfn = list(data.dfs.keys())[0]
				self.lastblocknumber = data.dfs[dfn]['blocknumber'][0]#get latest blocknumber from reposoitry system...
				#not sure if this is needed....or should it be provided by the requestor
				#....ties in data source more closely but helps with requests from me
				#shoudl probably be provided
			elif state == 'live':
				params = {'module': 'proxy', 'action': 'eth_blockNumber'}
				process = self.processEPetherscan({'address': addresses}, params, actions)
				self.lastblocknumber = next(process).df['blocknumber']#				||get latest blocknumber from etherscan
			else:
				if self.lastblocknumber == None:
					self.lastblocknumber = 9999999
		except Exception as e:
			print('Last Block retreival failed due to',e)
			self.lastblocknumber = 9999999
		return self

	def getLastBlocks(self, state: str='stale'):
		'''Get the Last Block Number for the appropriate datasource based on
		 	request parameters
			'''
#		self.setReader('etherscan', {'views': ['lastblockbyaddress_a000']})
#		self.extract(['address', 'type', 'max'])
#		self.lastblocks = self.dataset
		data = next(sonql.doc(self.db).read({'views': ['lastblockbyaddress_a000']}))
		dfn = list(data.dfs.keys())[0]
		self.lastblocks = data.dfs[dfn]
		return self

	def getSupplyByTokens(self, tokens: list):
		''' '''
		if len(tokens) > 1 and tokens[0] != 'ETH':
			view = 'tokens'
			params = {'where': {'in': [tokens]}}
			data = next(sonql.doc(db).read({'views': [view]}, params))
		addresses = data.dfs[view]['address']
		addresses = {'contractaddress': addresses}
		params = {'module': 'stats'}
		if 'ETH' in tokens:
			actions = ['ethsupply']
			tokens = tokens.pop(tokens.index('ETH'))
			process = self.processEPetherscan('{}', params, actions)
			while True:
				next(process)
				df = self.df
		else:
			df = DataFrame()
		actions = ['tokensupply']
		if tokens != []:
			bys = {'contractaddress': addresses}
			return self.processEPetherscan(bys, params, actions)

	def getTrxsByAddresses(self, addresses: list, startblock=0, action='txlist',
												name='base', altercols=None):#	||
		'''Get account data from etherscan using the account module by list of
			addresses from a specific block forward'''#		||
		#self.getLastBlocks()
		#lb = self.lastblocks[self.lastblocks['type'] == 'tokentx']#need to work this in with action
		#lastblocks = dict(zip(lb['address'], lb['max']))
		lastblocks = {}
		params = {'module': 'account', 'startblock': startblock}#				||
		bys = {'address': [x for x in addresses if x != '']}# sanitization process
		cfgn = inspect.currentframe().f_code.co_name
		if name == 'base':
			try:
				name = list(self.sink.keys())[0]
			except Exception as e:
				if log: print(f'GetTrxsByAddress Error {e}')
		load = [bys, params, action, cfgn, name, lastblocks, altercols]
		if log: print('TRXS params', params, bys)
		return self.processEPetherscan(*load)

	def getTrxsByBlocks(self, blocks: list, altercols=None):
		''' '''
		params = {'module': 'proxy'}#											||
		actions = ['eth_getBlockByNumber']
		name = inspect.currentframe().f_code.co_name
		bys = {'blocknumber': blocks}
		return self.processEPetherscan(bys, params, actions, name)

	def getTrxByContracts(self, contracts: list, how: list=['full'],
															altercols=None):#	||
		'''Get contract data from etherscan using the contract module'''
		params = {'module': 'contract'}#										||
		actions = []
		bys = {'contract': contracts}
		name = inspect.currentframe().f_code.co_name
		return self.processEPetherscan(bys, params, actions)

	def processEPetherscan(self, pterms: dict, params: dict={}, action: list=[],
						cfgn=None, name=None, lastblocks={}, altercols={}):#	||
		'''Generic process for paging through etherscan data
			make this as generic as possible while maintianing etherscan functionality		'''
		cfg = self.config.dikt['endpoints']
		if cfgn == None:
			cfgn = inspect.currentframe().f_back.f_code.co_name# gets the caller of the method
		#builds the endpoint template that will be used
		self.buildEndPoint(cfg[cfgn][action]['seq'], 'seq')
		params['sort'] = 'asc'
		for category in pterms.keys():
			for term in pterms[category]:#														||Terms represents controlling mechanism
				if log: print('TERM', term)
				params['startblock'] = 0
				params[category] = term
				if log: print('LastBlocks', lastblocks)
				if term in lastblocks.keys():
					params['startblock'] = lastblocks[term]
				if 'endblock' not in params.keys():
					params['endblock'] = int(9e9)
				#********BUG****************merge is not accepting new action paramter override
				params['action'] = action
				#*******************************
				spage, npages, step = 0, 0, 10000
				for key, val in params.items():#this is forcing an override due to some failure in the override function
					self.parameters.it[key] = val
				self.parameters.merge(params, None, ':::ROOT:::', 'override')
				params = self.parameters.it
				self.status = True
				page, params['offset'] = spage, step
				while True:
					params['page'] = page
					load = [params, [cfgn, action], ['result'], name,
															altercols, step]#	||

					self.status = self.getEP(*load)
					if not self.status:
						break
					yield self
					self.status = True
					page += 1
					if page > 5:
						self.status = False
						break
			params.pop(category)
		yield self


def collectABIsByAddresses(db, table, addresses):
	''' '''
	params = {'addresses': addresses}
	runCollector('getABIsByAddresses', db, params, table)


def collectAllTrxs():
	''' '''
	runCollector()


def collectBalancesByAddresses(db, table, addresses):
	''' '''
	params = {'addresses': addresses}
	runCollector('getBalancesByAddresses', db, params, table)


def collectBlocks(db: str, table: str, blocks: list):
	''' '''
	params = {'blocks': blocks}
	runCollector('getTrxsByBlocks', db, params, table)


def collectSupplyByTokens(db: str, table: str, tokens: list):
	''' '''
	params = {}
	runCollector('getSupplyByTokens', db, params, table)


def collectTransactionsByBlocks(db: str, table: str, blocks: list):
	''' '''
	params = {'filters': {'IN': {'blocks', blocks}}}
	runCollector('getTrxsByBlocks', db, params, table)#								||


def collectTransactionsByContracts(db: str, table: str, contracts: list):
	''' '''
	params = {'filters': {'IN': {'contracts': contracts}}}
	runCollector('getTrxsByContracts', db, params, table)


def collectTransactionsByTransactions(db: str, table: str, transactions: list):
	''' '''
	params = {'filters': {'IN': {'transactions': transactions}}}
	runCollector('getTrxsByTransactions', db, params, table)


def runCollector(process, db, params, table, altercols=None):
	'''Run the basic sequence for collecting data from this specific source
		type'''
	fx = Data()
	fx.initCollector(process, 'methodify', 'etherscan', db, 'db', table)
	fx.setReader(params, 'etherscan', altercols).collect(table)


#==============================Source Materials=================================||
'''
https://pypi.org/project/py-etherscan-api/
https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey=YourApiKeyToken
https://pypi.org/project/etherscan/
https://github.com/corpetty/py-etherscan-api
https://sebs.github.io/etherscan-api/
https://etherscan.io/apis
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

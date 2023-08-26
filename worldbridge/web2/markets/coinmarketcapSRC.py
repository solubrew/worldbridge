#@@@@@@@@@@@@Pheonix.Organism.Worldbridger.Markets.CoinMarketCapSRC@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: 'c6e61834-9a71-4107-97b0-6f19abba2c6e'
	name:
	description: >
		Access data through CoinMarketCap official api as well as site scraping
		methods to consume and organize crypto currency data
	expirary: <^[expiration]^>
	version: <^[version]^>
	path:
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, join
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
#===============================================================================||
from pandas import DataFrame, Series
#===============================================================================||
from condor import condor
from excalc import data as calcd
from squirl.orgnql import monql
from subtrix import subtrix
from worldbridge import worldbridge
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
where = abspath(join(''))#														||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = f'{here}_data_/markets.yaml'#									||use default configuration
class Data(worldbridge.stone):#																||
	''' '''#							||
	def __init__(self, cfg={}):#														||
		''' '''#							||
		self.config = condor.instruct(pxcfg).override(cfg)
		self.config.select('coinmarketcap')
		worldbridge.stone.__init__(self, self.config)#							||

	def getAllNow(self):#														||
		'''Get current market data for all tokens'''
		links = ['cryptocurrency', 'listings', 'latest']#											||
		self.buildEndPoint(links)#												||
		next(self.yieldEP({}, links, ['data']))
		yield self.df

	def getTokensLatest(self, tokens):#										||
		'''Get current market data for select tokens'''#						||
		links = ['cryptocurrency', 'quotes', 'latest?',
									'convert={convert}&symbol=', '{symbol}']#	||
		if isinstance(tokens, list):
			tokens = calcd.stuff(tokens).list_2_str().it#						||
			tokens = tokens.replace(' ', '').replace("'", '')
		self.buildEndPoint(links)#												||
		params = {'convert': 'USD', 'symbol': tokens}
		self.getEP(params, links, ['data'])
		if log: print('DF',self.sinkdfs['base'].head())
		yield self

	def getInfo(self, tokens):
		'''Get current info for select tokens'''
		chunksize = 100
		links = ['info']
		if isinstance(tokens, (list, Series)):
			tokens = calcd.stuff(tokens).list_2_str().it#						||
			tokens = tokens.replace(' ', '').replace("'", '')
		params = {'symbol': tokens}#											||
		self.buildEndPoint(links)#												||
		next(self.yieldEP(params))
		yield self

def collectAllNow(db, table):
	''' '''
	src = Data()
	src.process = src.getAllNow
	columns = ['name', 'symbol', 'slug', 'price', 'volume_24h', 'market_cap',
				'last_updated', 'circulating_supply', 'max_supply',
				'total_supply', 'perc_change_1h', 'perc_change_24hr',
				'perc_change_7d']
	cfg = {'columns': columns}
	src.collect(db, table, {}, cfg)

def collectInfo(db, table):
	''' '''
	src = Data()
	src.process = src.getInfo
	src.collect(db, table)

def collectTokensLatest(db: str, table: str, tokens: list):
	''' '''
	src = Data().initSource('getTokensLatest', 'methodify')
	src.initSink(db, 'db', table)
	src.setReader({'tokens': tokens}).collect(table)

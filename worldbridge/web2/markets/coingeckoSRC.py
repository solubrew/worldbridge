#@@@@@@@@@@@@Pheonix.Organism.@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid:
	name:
	description: >
		Access data through CoinGecko official api as well as site scraping
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
import time
#===============================================================================||
from worldbridger.libs import DataFrame, profile
#===============================================================================||
from condor import condor
from condor.thing import what, when
from excalc import data as calcd, ts as calcts
from worldbridger import worldbridger, runProfile
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
where = abspath(join(''))#														||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = f'{here}_data_/markets.yaml'#									||use default configuration
class Data(worldbridger.stone):
	def __init__(self, cfg: dict={}):
		''' '''
		self.config = condor.instruct(pxcfg).select('coingecko')
		worldbridger.stone.__init__(self, self.config)
		self.config.override(cfg)
	def getEvents():
		'''Events doesn't have any data'''
		return self
	def getExchanges(self, spage: int=1, npages: int=0):
		'''Page through list of exchangegs'''
		links = ['exchanges', '?per_page={step}', '&page={page}']
		self.buildEndPoint(links)
		paging = self.pageEP(spage, npages, 250)
		while True:
			status = next(paging, None)
			if status == None:
				break
			yield self.df
		yield None
	def getPricesByExchangesByTokens(self, exchanges: list=[], tokens: list=[],
																name='base'):#	||
		'''Get prices by exchanges paging through tokens or filtering by given
			list of tokens'''
		links = ['exchanges', '{exchange}', 'tickers?page={page}']
		if tokens != []:
			links.append('{tickers}')
		self.buildEndPoint(links)
		if exchanges == []:#													|| No exchanges specified
			exchangesOBJ = self.pageDB('cgk_exchanges', 'exchangeid')#			|| Page through database table of exchanges
		while True:#															||
			if exchanges == []:#												||
				exchanges = next(exchangesOBJ, None)#							|| connect to database for list of exchanges
			for exchange in exchanges:#											|| iterate through select exchanges
				if log: print(f'Exchange {exchange}')
				params = {'exchange': exchange}
				if '{tickers}' in links:#										||specific token specified via list
					step = 100
					s, d = 0, step
					for token in tokens[s:d]:#									|| iterate through select tokens of exchange
						params['{tickers}']=calcd.stuff(token).list_2_str().it#	||
						self.getEP(params)
						s = d
						d += step
						yield self
				else:
					params['page'], params['offset'] = 1, 100
					while True:
						status = self.getEP(params, links, ['tickers'], name)
						if not status:
							break
						if log: print('DFS', self.sinkdfs.keys())
						if self.yieldBreak(self, name, params['offset']):
							break
						yield self
						#self.sinkdfs[name] = DataFrame()
						params['page'] += 1
						time.sleep(5)
				exchanges.pop(exchanges.index(exchange))
			if exchanges == [] or exchanges == None:
				break
		yield self
	def getHistoryByTickerByDate(self, slugs: list=[], sdate: str=None,
											edate: str=None, name: str='base'):
		'''History end point returns 1 day at a time....grab a large portion of
			values from BTC history and use for conversion calculations
			create a seperate table from general history'''
		links = ['coins', '{slug}', 'history?date={date}']
		self.buildEndPoint(links)
		#self.setHandler('HTML', self.)
		if edate == None:
			edate = dt.datetime.now()
		if sdate == None:
			sdate = edate + dt.timedelta(days=-90)
		drange = calcts.stuff(sdate).genSeq(edate,'1D').seq
		for d in drange:
			d = when(d).cast('%Y%m%d').getStr('%d-%m-%Y')
			for slug in slugs:
				params = {'slug': slug, 'date': d, 'page': 1, 'offset': 100}
				while True:
					self.getEP(params, links)
					if self.yieldBreak(self, name, params['offset']):
						if log: print('CoinGecko Break')
						break
					yield self
					self.sinkdfs[name] = DataFrame()
					params['page'] += 1
				time.sleep(5)#limit requests due to api level
		yield self
	def getOHLCByTickerByDate(self, tokens: list=[]):
		''' '''
		links = ['{coinid}', 'ohlc?vs_currency={base}', '&days={days}']
		return self.df
	def getPriceByTicker(tickers: list=[]):
		''' '''
	def getTickers(self, links: list=[], tokens: list=[]):#						||
		'''Get endpoint by suppling various variables to complete the url'''#	||
		self.buildEndPoint(links)#												||
		if tokens == []:#				||
			tokensOBJ = self.pageDB('cgk_tokens', 'slug')#						||
		while True:
			if tokens == []:
				tokens = next(tokensOBJ, [])
			if tokens == []:
				break
			for token in tokens:#											||
				params = {'token': token}
				self.getEP(params)
			tokens = []
def collectPricesByExchangesByTokens(db: str, table: str, exchanges: list=[],
															tokens: list=[]):#	||
	''' '''
	#this is kind of a hack...need to move modifications llike this up the
	#stack from here
	if '{date}' in db:
		date = when().today
		db = db.replace('{date}', date)
		if log: print('DB', db, date)
	src = Data().initSelector('getPricesByExchangesByTokens', 'methodify', table)
	src.initSink(db, 'db', table)
	src.setReader({'exchanges': exchanges, 'tokens': tokens, 'name': table}, table)
	src.collect(table)
#@runProfile()
def collectPriceHistoryByDateByTokens(db: str, table: str, start: str,
													end: str, tokens: list=[]):
	''' '''
	src = Data().initCollector(db, 'db', 'base', db, 'db')
	params = {'WHERE': {'NOT IN': {'slug': [None]},}}
				# 'LESSEREQUAL': {'cgk_tokensid': 100},
				# 'GREATER': {'cgk_tokensid': 0}}}
	if tokens != []:
		params['WHERE']['IN'] = {'symbol': tokens}
	src.setReader({'table': ['cgk_tokens'], 'filters': params})
	src.setExtract('slug', 'set').extract()
#	if log: print(src.sinkdfs)
	slugs = list(src.dataset['slug'])
	slugs.sort()
	src.initSelector('getHistoryByTickerByDate', 'methodify')
	params = {'slugs': slugs, 'sdate': start, 'edate': end}
	src.setReader(params)
	#need to implement a transition of data from source to sink
	src.collect('base')

''''
https://www.coingecko.com/en/api#explore-api
'''

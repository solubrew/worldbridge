#@@@@@@@@@Pheonix.Organisms.Worldbridger.Apes.Everses.yahooSRC@@@@@@@@@@||
'''
---
<(META)>:
	docid: 'e2639466-d1d8-4e2a-b180-acf357ebbec4'
	name:
	description: >
		Build a Yahoo source specific data API for collecting stockmarket data
		to be used through pheonix to allow for easy storage or retreival of
		data
	version: 0.0.0.0.0.0
	path: <[LEXIvrs]>
	outline:
	authority: document|this
	security: seclvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*
#===============================================================================||
import os, datetime as dt, queue as que, threading as thr
import json, requests, time
#===============================================================================||
import yfinance as yf
from pandas import concat, DataFrame
#===============================================================================||
from pheonix.config import config
from pheonix.store.orgnql import monql
from pheonix.store.orgnql import sonql
from pheonix.thing import thing
from pheonix import worker
#===============================================================================||
here = os.path.join(os.path.dirname(__file__),'')#								||
version = '0.0.0.0.0.0'#														||
#===============================================================================||
class src(object):#																||
	def __init__(self, cfg=None, wrtr=None):#									||
		'''Initialize Yahoo financial Data Source Object with configuration
		and optionally a wrtr object'''
		pxcfg = '{0}z-data_/markets.yaml'.format(here)#							||
		self.config = config.instruct(pxcfg).override(cfg).dikt#				||
		if wrtr == None:#														||
			self.wrtr = wrtr#													||
		else:#																	||
			self.wrtr = store#													||
	def getCashflow(self, cfg):#												||
		'''Process stock generator Cashflow data and either store returned data
		 	or yield it to caller'''#											||
		genr = self._proc(cfg, 'cashflow')
		while True:#															||
			done = next(genr, None)#											||
			if done == None:#													||
				break#															||
			yield self#															||
		yield self#																||
	def getDividends(self, cfg):#												||
		'''Process stock generator Dividends data and either store returned data
		 	or yield it to caller'''#											||
		genr = self._proc(cfg, 'dividends')
		while True:#															||
			done = next(genr, None)#											||
			if done == None:#													||
				break#															||
			yield self#															||
		yield self#																||
	def getEarnings(self, cfg):#												||
		'''Process Stock Generator Calendar data and either store returned data
			or yield it to caller'''#											||
		genr = self._proc(cfg, 'calendar')
		while True:#															||
			done = next(genr, None)#											||
			if done == None:#													||
				break#															||
			yield self#															||
		yield self#																||
	def getEarningsHistory(self, cfg):
		''' '''
		pass
	def getFinancials(self, cfg):#												||
		'''Process stock generator Financials data and either store returned
			data or yield it to caller'''#										||
		genr = self._proc(cfg, 'financials')
		while True:#															||
			done = next(genr, None)#											||
			if done == None:#													||
				break#															||
			yield self#															||
		yield self#																||
	def getFinancialsQuarterly(self, cfg):#										||
		'''Process stock generator Quarterly Financials data and either store
			returned data or yield it to caller'''#								||
		genr = self._proc(cfg, 'quarterly_financials')
		while True:#															||
			done = next(genr, None)#											||
			if done == None:#													||
				break#															||
			yield self#															||
		yield self#																||
	def getInstitutionalHolders(self, cfg):#									||
		'''Process stock generator Institutional Holders data and either store
			returned data or yield it to caller'''#								||
		genr = self._proc(cfg, 'institutional_holders')
		while True:#															||
			done = next(genr, None)#											||
			if done == None:#													||
				break#															||
			yield self#															||
		yield self#																||
	def getMajorHolders(self, cfg):#											||
		'''Process stock generator Major Holders data and either store returned
			data or yield it to caller'''#										||
		genr = self._proc(cfg, 'major_holders')
		while True:#															||
			done = next(genr, None)#											||
			if done == None:#													||
				break#															||
			yield self#															||
		yield self#																||
	def getOptions(self, cfg):#													||
		''' '''#																||
		out = 'options'#														||set get attribute
		stocksRDR = self.getStocks(cfg)#										||
		while True:#															||
			data = next(proc(stocksRDR, out), None)#							||Process Stock Reader and Get Stock Objects from generator
			if not isinstance(data, DataFrame):#								||
				print('No More Stocks')
				break
			self.options = None
			for ticker in self.tickers:#										||loop thru tickers
				try:#															||
					odates = getattr(self.stocks.tickers, ticker).options#		||get options attribute return date list
				except Exception as e:#											||
					continue#													||
				for odate in odates:#											||loop date list
					try:
						t = self.stocks.tickers
						chain = getattr(t, ticker).option_chain(odate)#			||
					except Exception as e:
						continue
					calls, puts = chain[0], chain[1]#							||
					calls['type'] = ['call' for x in range(calls.shape[0])]#	||
					calls['ticker'] = [ticker for x in range(calls.shape[0])]#	||
					fill = [odate for x in range(calls.shape[0])]#			||
					calls['expirary_date'] = fill#								||
					puts['type'] = ['put' for x in range(puts.shape[0])]#		||
					puts['ticker'] = [ticker for x in range(puts.shape[0])]#	||
					fill = [odate for x in range(puts.shape[0])]#				||
					puts['expirary_date'] = fill#								||
					if isinstance(self.options, DataFrame):#					||
						o = [self.options, calls, puts]#						||
						self.options = concat(o, sort=True)#					||
					else:#														||
						self.options = concat([calls, puts], sort=True)#		||
			if self.wrtr != None:
				self.wrtr(self.options, self.config['sink'])
				yield True
			else:
				yield self
		yield None
	def getQuoteLatest(self, ticker, sdate, edate):
		''' '''
		if '/' in ticker:
			with sonql.doc(cfg['db']) as doc:
				doc.write({'badtickers': {'records': [[ticker]],
											'columns': ['ticker']}})#	||
			return self
		try:
			df = yf.download(ticker, start=sdate, end=edate, interval='1d',
																prepost=True)#	||
			if df.empty:
				with sonql.doc(cfg['db']) as doc:
					doc.write({'badtickers': {'records': [[ticker]],
													'columns': ['ticker']}})#	||
				return self
			print('data',ticker,df.head())
		except:
			with sonql.doc(cfg['db']) as doc:
				doc.write({'badtickers': {'records': [[ticker]],
													'columns': ['ticker']}})#	||
			return self
		fill = [ticker for x in range(df.shape[0])]
		df['ticker'] = fill
		if isinstance(self.quotes, DataFrame):
			self.quotes = concat([self.quotes, df])
		else:
			self.quotes = df
		return self
	def getQuotesLatest(self, cfg):
		'''Request data 1 ticker at a time and then retrieve latest quote used
		 	to work through troublesome ticker values'''
		while True:
			tickers = next(self.tickers, None)
			if tickers == None:
				break
			tickers = list(tickers.dfs[self.tickertable]['ticker'])
			self.quotes = None
			db = self.config['sink']['dargs']['db']
			sdate, edate = '2017-05-05', thing.when().today_dashed
			for ticker in tickers:
				self.getQuoteLatest(self, ticker, sdate, edate)
			yield self
	def getQuotesHistory(self, tickers=None):
		''' '''
		if tickers != None:
			self.tickers = tickers
		while True:
			tickers = next(self.tickers, None)
			if tickers == None:
				break
			tickers = list(tickers.dfs[self.tickertable]['ticker'])
			self.quotes = None
			sdate, edate = '2017-05-05', thing.when().today_dashed
			quotes = yf.download(tickers, start=sdate, end=edate,
												interval='1d', prepost=True)#	||
			for ticker in tickers:
				df = quotes.iloc[:, quotes.columns.get_level_values(1) == ticker]
				df.reset_index(inplace=True)
				if df['Close'].empty:
					continue
				df = DataFrame(df.values.tolist(), columns = [x[0] for x in df.columns])
				fill = [ticker for x in range(df.shape[0])]
				df['ticker'] = fill
				if isinstance(self.quotes, DataFrame):
					self.quotes = concat([self.quotes, df])
				else:
					self.quotes = df
			if self.wrtr != None:
				self.wrtr(self.quotes, self.config['sink'])
				yield True
			else:
				yield self
	def getQuotesLatest(self, tickers=None):
		''' '''
		while True:
			tickers = next(self.tickers, None)
			if tickers == None:
				break
			tickers = list(tickers.dfs[self.tickertable]['ticker'])
			self.quotes = None
			db = self.config['sink']['dargs']['db']
			quotes = yf.download(tickers, period='60m', interval='1m',
																prepost=True)#	||
			for ticker in tickers:
				df = quotes.iloc[:, quotes.columns.get_level_values(1) == ticker]
				df.reset_index(inplace=True)
				if df['Close'].empty:
					continue
				columns = [x[0] for x in df.columns]
				df = DataFrame(df.values.tolist(), columns=columns)
				fill = [ticker for x in range(df.shape[0])]
				df['ticker'] = fill
				if isinstance(self.quotes, DataFrame):
					self.quotes = concat([self.quotes, df])
				else:
					self.quotes = df
			if self.wrtr != None:
				self.wrtr(self.quotes, self.config['sink'])
				yield True
			else:
				yield self
	def getQuotesToday(self, tickers=None):
		'''Get Ticker Quote '''
		self.getTickers(tickers)
		while True:
			self.quotes = None
			tickers = next(self.tickersRDR, None)
			if tickers == None:
				break
			tickers = list(tickers.dfs[self.tickertable]['ticker'])
			db = self.config['sink']['dargs']['db']
			quotes = yf.download(tickers, period='1d', interval='1m',
																prepost=True)#	||
			for ticker in tickers:
				df = quotes.iloc[:, quotes.columns.get_level_values(1) == ticker]
				df.reset_index(inplace=True)
				if df['Close'].empty:
					continue
				columns = [x[0] for x in df.columns]
				if 'index' in columns:
					idx = columns.index('index')
					columns.pop(idx)
					columns.insert(idx, 'datetime')
				df = DataFrame(df.values.tolist(), columns=columns)
				df['ticker'] = [ticker for x in range(df.shape[0])]
				if isinstance(self.quotes, DataFrame):
					self.quotes = concat([self.quotes, df], sort=True)
				else:
					self.quotes = df
			if self.wrtr != None:
				self.wrtr(self.quotes, self.config['sink'])
				yield True
			else:
				yield self
	def getRecommendations(self, cfg):
		''' '''
		genr = self._proc(cfg, 'recommendations')
		while True:
			done = next(genr, None)
			if done == None:
				break
			yield self#															||
		yield self#																||
	def getSplits(self, cfg):
		''' '''
		genr = self._proc(cfg, 'splits')
		while True:
			done = next(genr, None)
			if done == None:
				break
			yield self
		yield self
	def getSustainability(self, cfg):
		'''Create Sustainability data generator'''
		genr = self._proc(cfg, 'sustainability')
		while True:
			done = next(genr, None)
			if done == None:
				break
			yield self#															||
		yield self#																||
	def getStocks(self, cfg):
		'''Get Stocks from Yahoo source as multiple object attributes '''
		cfg['page'] = 254
		self.getTickers(cfg)
		while True:
			tickers = next(self.tickersRDR, None)
			if tickers == None:
				print('No More Tickers')
				break
			self.tickers = list(tickers.dfs[self.tickertable]['ticker'])
			self.stocks = yf.Tickers(self.tickers)
			yield self
	def getTickers(self, cfg):
		'''Get Tickers Generator Object connected to configured database'''
		if 'page' not in cfg.keys():
			cfg['page'] = 1000
		try:
			self.tickertable = cfg['dargs']['table']
			self.tickersRDR = sonql.doc(cfg['dargs']['db']).read(
							{'views': [cfg['dargs']['table']], 'page': cfg['page']})
		except Exception as e:
			self.tickertable = cfg['oargs']['table']
			self.tickersRDR = sonql.doc(cfg['oargs']['db']).read(
							{'views': [cfg['oargs']['table']], 'page': cfg['page']})
		return self
	def _proc(self, cfg, out):
		'''Process stocks data retrieved as multiple object attributes'''
		stocksRDR = self.getStocks(cfg)
		while True:
			df = next(proc(stocksRDR, out), None)
			if not isinstance(df, DataFrame):
				break
			if self.wrtr != None:
				self.wrtr(df, self.config['sink'])
				return True
			else:
				setattr(self, out, data)
				yield self
		yield None
#@worker.threadsafe_generator
def proc(rdr, out):
	'''Process Stock Objects generated from paging thru tickers data'''
	while True:
		results = None
		data = next(rdr, None)
		if data == None:
			print('No Stocks')
			break
		for ticker in data.tickers:
			try:
				stock = getattr(data.stocks.tickers, ticker)
				df = DataFrame(getattr(stock, out))
			except Exception as e:
				print(out, 'Error', e)
				continue
			if df.empty:
				continue
			df = reshape(df, out)
			if df.empty:
				continue
			df['ticker'] = [ticker for x in range(df.shape[0])]
			if isinstance(results, DataFrame):
				results = concat([results, df], sort=True)
			else:
				results =  df
		yield results
	yield results
def reshape(df, how):
	''' '''
	if how == 'calendar':
		df = df.transpose()
		df['Earnings Date'] = df['Earnings Date'].astype(str)
		now = thing.when().today_dashed
		df['onDate'] = [now for x in range(df.shape[0])]
		if 'NaT' in df['Earnings Average']:
			df = DataFrame()
	elif how == 'sustainability':
		df = df
	elif how == 'major_holders':
		df = df.transpose()
		df.columns = df.iloc[1,:]
		df = df.drop(df.index[1])
	elif how in ('dividends', 'recommendations', 'splits'):
		df.reset_index(inplace=True)
	elif how == 'options':
		pass
	return df
def store(df, cfg):
	'''	replace with a communication channel to send data to rabbitmq to be
		written when possible to the database need a priority system that
		can override FIFO
		replace with a utilty within the store element.....increase robustness of
		failover store '''
	try:#																||
		db0 = cfg['dargs']['db']#								||
		table0 = cfg['dargs']['table']#							||
		print('Write JobMarketsTLs Aquire')
		with sonql.doc(db0) as doc:#									||
			doc.write({table0: {'dataframe': df}})#	||
	except Exception as e:#														||
		db1 = cfg['oargs']['db']#								||
		table1 = cfg['oargs']['table']#							||
		with sonql.doc(db1) as doc:#									||
			doc.write({table1: {'dataframe': df}})#	||

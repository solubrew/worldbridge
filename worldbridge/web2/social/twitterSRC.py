#@@@@@@@@@Pheonix.Organisms.Worldbridger.Apes.Everses.yahooSRC@@@@@@@@@@||
'''
---
<(META)>:
	docid: ''
	name:
	description: >
		Build a Twitter source specific data API for collecting sentiment and
		trend data to be used through pheonix to allow for easy storage or
		retrevial of data
	version: 0.0.0.0.0.0
	path: <[LEXIvrs]>
	outline:
	authority: document|this
	security: seclvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*
#===============================================================================||
import os, datetime as dt, queue as que, threading as thr#						||
#===============================================================================||
import twitter#																	||
from pandas import concat, DataFrame#											||
#===============================================================================||
from pheonix.elements.calcgen import data as calcd#								||
from pheonix.elements.config import config#										||
from pheonix.elements.store.orgnql import monql#								||
from pheonix.elements.store.orgnql import sonql#								||
from pheonix.elements.thing import thing#										||
#===============================================================================||
here = os.path.join(os.path.dirname(__file__),'')#								||
version = '0.0.0.0.0.0'#														||
#===============================================================================||
class src(object):
	def __init__(self, cfg, wrtr=None):
		'''Initialize Yahoo financial Data Source Object with configuration
		and optionally a wrtr object'''
		pxcfg = '{0}z-data_/markets.yaml'.format(here)
		self.config = config.instruct(pxcfg).override(cfg)
		self.session = self.config.session
		entgls = self.session['entanglements']['twitter']
		self.api = twitter.API(**entgls)
		if wrtr == None:
			self.wrtr = wrtr
		else:
			self.wrtr = store

	def buildSearchRequest(self):
		''' '''
		return self

	def buildTweetDataTable(self):
		''' '''
		return self

	def getTweets(self, cfg):#												||
		'''Process Stock Generator Calendar data and either store returned data
			or yield it to caller'''
		while True:
			done = next(self._proc(cfg, 'calendar'), None)
			if done == None:
				break
			yield self
		yield self

	def getUsers(self):
		''' '''
		return self

	def getTerms(self, cfg):
		'''Get Search Terms from database defined by configuration dictionary'''
		if 'page' not in cfg.keys():
			cfg['page'] = 1000
		try:
			self.termstable = cfg['dargs']['table']
			self.termsRDR = sonql.doc(cfg['dargs']['db']).read(
							{'views': [cfg['dargs']['table']], 'page': cfg['page']})
		except Exception as e:
			self.termstable = cfg['oargs']['table']
			self.termsRDR = sonql.doc(cfg['oargs']['db']).read(
							{'views': [cfg['oargs']['table']], 'page': cfg['page']})
		return self
	def _proc(self, cfg, out):
		''' '''
		stocksRDR = self.getTweets(cfg)
		while True:
			df = next(proc(stocksRDR, out), None)
			if not isinstance(df, DataFrame):
				break
			print('DF', df)
			if self.wrtr != None:
				self.wrtr(df, self.config['sink'])
				yield True
			else:
				setattr(self, out, data)
				yield self
		yield self

def proc(rdr, out):
	'''Process Stock Objects generated from paging thru tickers data'''
	columns = ['searchterm', 'date', 'full_text', 'hashtags', 'user', 'media',
				'text', 'retweeted', 'urls', 'coordinates', 'location',
				'language', 'sensitive', 'place', 'geo']
	while True:
		data = next(rdr, None)
		if data == None:
			print('No More Tweets')
			break
		results = []
		for tweet in data.tweets:
			urls = [x.expanded_url for x in tweet.urls]
			urls = calcd.stuff(urls).list_2_str().it
			hashtags = [x for x in tweet.hashtags]
			hashtags = calcd.stuff(urls).list_2_str().it
			results.append([searchterm, tweet.created_at, tweet.full_text,
			 				hashtags, tweet.user, tweet.media,
							tweet.text, tweet.retweeted, urls,
							tweet.coordinates, tweet.location, tweet.lang,
							tweet.possibly_sensitive, tweet.place, tweet.geo])
		yield DataFrame(results, columns=columns)
	yield data

def store(df, cfg):
	''' '''
	try:#																||
		db0 = cfg['dargs']['db']#								||
		table0 = cfg['dargs']['table']#							||
		print('Write JobMarketsTLs Aquire')
		with sonql.doc(db0) as doc:#									||
			doc.write({table0: {'records': df.values.tolist(),#					||
													'columns': df.columns}})#	||
	except Exception as e:#														||
		db1 = cfg['oargs']['db']#								||
		table1 = cfg['oargs']['table']#							||
		with sonql.doc(db1) as doc:#									||
			doc.write({table1: {'records': df.values.tolist(),#					||
													'columns': df.columns}})#	||

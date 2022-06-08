#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: 6b55525a-59d6-4a14-a092-363509b1ca6d
	name: Molecules Level Languager Module Gmail Extension Python Document
	description: >
	version: 0.0.0.0.0.0
	path: <[LEXIvrs]>/panda/LEXI/LEXI.yaml
	outline:
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
#=======================================================================||
from __future__ import print_function
import pickle
import os.path
try:
	from googleapiclient.discovery import build
	from google_auth_oauthlib.flow import InstalledAppFlow
	from google.auth.transport.requests import Request
except:
	pass

import datetime as dt, os, pickle
from pytrends.request import TrendReq
#===========================3rd Party Modules===========================||
try:
	import simplejson as j
	from google_auth_oauthlib.flow import InstalledAppFlow as IAF
	from google.auth.transport.requests import Request
except:
	pass
#=======================================================================||
from pheonix.elements.config import config#								||
from pheonix.elements.comm import comm#								||
from pheonix.elements.subtrix import subtrix
#=======================================================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
there = os.path.abspath(os.path.join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
#=======================================================================||
class client:
	version='0.0.0.0.0.0'#												||
	def __init__(self, uid, SCOPES, cfg=None):#							||
		pxcfg = here+'/z-data_/google.yaml'#							||use default configuration
		self.config = config.instruct(pxcfg).load().override(cfg).dikt#	||
		#should be using monk....
		self.connect(SCOPES)
	def connect(self, SCOPES):
		self.getCreds(SCOPES)
		return self
	def getCreds(self, SCOPES):
		self.creds = None
		data = {'username': ''}
		pklf = subtrix.mechanism(self.config['picklejar'], data)
		pklf = here+'/z-data_/token.pickle'
		if os.path.exists(pklf):
			with open(pklf, 'rb') as token:
				self.creds = pickle.load(token)
		lock = 0
		if not self.creds or not self.creds.valid:
			if self.creds and self.creds.expired:
				if self.creds.refresh_token:#	||
					self.creds.refresh(Request())
					lock = 1
		if lock == 0:
			secsf = (self.config['apikey'], SCOPES)
			flow = IAF.from_client_config(*secsf)
			self.creds = flow.run_local_server()
			lock = 1
		try:
			with open(pklf, 'wb') as token:
				pickle.dump(self.creds, token)
		except:
			pass
		return self

class src(object):
	def __init__(self, terms, store=None):
		''
		cfg = '{0}/z-data_/google.yaml'.format(here)
		self.config = config.instruct(cfg).select('trendsSRC').dikt
		params = self.config['request']['parameters']
		self.dfs = {}
		self.trends = TrendReq()
		print('Trends', self.trends)
		self.terms = terms
		self.nuid = thing.what().gen()
	def getTerms(self, terms=None):
		'''Setup terms in data payload'''
		if terms == None:
			terms = self.terms
		self.trends.build_payload(kw_list=terms)
		return self
	def getInterstOverTime(self):
		''' '''
		return self
	def getHistoricalData(self, terms=None, table=None):
		''' '''
		if terms == None:
			terms = self.terms
		if table == None:
			table = next(self.nuid)
		self.dfs[table] = self.trends.get_historical_interest(self.terms)
		return self
	def getInterestByRegion(self, table=None):
		''' '''
		if table == None:
			table = next(self.nuid)
		self.dfs[table] = self.trends.interest_by_region()
		return self
	def getRealTimeTrending(self, table=None):
		''' '''
		if table == None:
			table = next(self.nuid)
		self.dfs[table] = self.trends.trending_searches(pn='united_states')
		return self
	def getTopCharts(self, date, table=None):
		'''' '''
		if table == None:
			table = next(self.nuid)
		self.dfs[table] = self.trends.top_charts(date, hl='en-US', tz=300, geo='GLOBAL')
		return self
	def getTables(self):
		''' '''
		return self





#print(InstalledAppFlow.__dict__)
#print(InstalledAppFlow.from_client_config.__dir__())
#==========================Source Materials=============================||
'''
https://developers.google.com/gmail/api/quickstart/python
http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
http://stackoverflow.com/questions/5193707/use-imaplib-and-oauth-for-connection-with-gmail
http://stackoverflow.com/questions/8561739/how-to-use-google-oauth2-access-token?lq=1
http://stackoverflow.com/questions/17708141/connecting-to-gmail-from-python
http://libgmail.sourceforge.net/
https://github.com/google/gdata-python-client
'''
#============================:::DNA:::==================================||
'''
<(DNA)>:
	<@[datetime]@>:
		<[class]>:
			version: <[active:.version]>
			test:
			description: >
				<[description]>
			work:
				- <@[work_datetime]@>
	<[datetime]>:
		here:
			version: <[active:.version]>
			test:
			description: >
				<[description]>
			work:
				- <@[work_datetime]@>
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

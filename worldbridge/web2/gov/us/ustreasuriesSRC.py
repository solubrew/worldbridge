#@@@@@@@@@@@@Pheonix.Organism.@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid:
	name:
	description: >
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
from pheonix.config import config
from pheonix.store.orgnql import monql
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
where = abspath(join(''))#														||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
class Data(worldbridger.stone):#												||
	''' '''#							||
	def __init__(self):#														||
		''' '''#							||
		pxcfg = '{0}z-data_/markets.yaml'.format(here)#							||
		worldbridger.stone.__init__(self, pxcfg, 'ustreasuries')
		self.config.override(cfg)#		||
		self.link = self.config.dikt['api']['url']#									||
		self.parameters = self.config.dikt['api']['parameters']#						||
		self.headers = self.config.dikt['api']['headers']#							||
		self.session = Session()#												||
		self.session.headers.update(self.headers)#								||
	def buildEndPoint(self):
		''' '''
		return url
	def getHistory(self):
		''' '''
	def getLatest(self):
		''' '''




https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=
month%28NEW_DATE%29%20eq%205%20and%20year%28NEW_DATE%29%20eq%202020
https://fred.stlouisfed.org/series/DRTSCILM

url =

start_day = ''
start_month = ''
start_year = ''

end_day = ''
end_month = ''
end_start = ''



parameters = '$filter=





month%2
8

NEW_DATE%2

9%2

0eq%2

05%2

0and%2

0year%2

8

NEW_DATE%2

9%2

0eq%2

02013'

getxmlendpoint
parse tree

['feed']['entry']['content']['m']['d'].child

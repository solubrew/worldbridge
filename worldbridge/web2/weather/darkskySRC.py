#@@@@@@@@@@@@@@@@@@@Pheonix.Molecule.Store.Test@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(meta)>:
	DOCid:
	name: Operations Outline Configuration Document
	description: >
		Test Store Module
	expirary: <^[expiration]^>
	version: <^[version]^>
	path: <[LEXIvrs]>panda/LEXI/RESRCs/ops/outlineOPs.py
	outline: <[outline]>
	authority: document|this
	security: seclvl2
	<(wt)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
import datetime as dt, os#								||
#=======================================================================||
from .forecast import Forecast
#=======================================================================||

#=======================================================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
there = os.path.abspath(os.path.join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
#=======================================================================||
class client:
	def __init__(self, latitude=38.5112, longitude=-86.176, time=None):
		''
#		future build out
#		self.apikey = equip.safe().getKey('darksky|lexi').key
		self.apikey = '8d36c21210d2df654e5be63d78f51713'
		self.lat = latitude
		self.lng = longitude
		self.time = time
		self.timeout = None
		self.queries = None
	def getCurrent(self):
		''
		self.time = thing.when().today
		self.data = self._api(self.apikey, self.lat, self.lng,
											self.time, self.timeout)#	||
		return self
	def getForecast(self):
		''
		self.data = self._api(self.apikey, self.lat, self.lng,
											self.time, self.timeout)#	||
		return self
	def getHistory(self, start=None, end=None):
		''
		if start == None:
			start = self.time
		if end == None:
			end = self.time
		self.data = self._api(self.apikey, self.lat, self.lng, start,#	||
														self.timeout)#	||
		return self
	def _api(self, key, lat, lng, t, to):
		''
		return Forecast(key,lat,lng,t,to)



'''
---
<(meta)>:
	DOCid: <^[uuid]^>
	name: Organism Level Oraculum Module YAML Configuration Document
	description: >
	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>pheonix/organism/oraculum/z-data_/oraculum.yaml
	outline: <[outline]>
	authority: document|this
	security: seclvl2
	<(wt)>: -32
'''

# data.py
class DataPoint(object):
	def __init__(self, data):
		self._data = data
		if isinstance(self._data, dict):
			for name, val in self._data.items():
				setattr(self, name, val)
		if isinstance(self._data, list):
			setattr(self, 'data', self._data)

	def __setattr__(self, name, val):
		def setval(new_val=None):
			return object.__setattr__(self, name, new_val if new_val else val)
		# regular value
		if not isinstance(val, (list, dict)) or name == '_data':
			return setval()
		# set specific data handlers
		if name in ('alerts', 'flags'):
			return setval(eval(name.capitalize())(val))
		# data
		if isinstance(val, list):
			val = [DataPoint(v) if isinstance(v, dict) else v for v in val]
			return setval(val)
		# set general data handlers
		setval(DataBlock(val) if 'data' in val.keys() else DataPoint(val))

	def __getitem__(self, key):
		return self._data[key]

	def __len__(self):
		return len(self._data)

class DataBlock(DataPoint):
	def __iter__(self):
		return self.data.__iter__()
	def __getitem__(self, index):
		# keys in darksky API datablocks are always str
		if isinstance(index, str):
			return self._data[index]
		return self.data.__getitem__(index)
	def __len__(self):
		return self.data.__len__()

class Flags(DataPoint):
	def __setattr__(self, name, value):
		return object.__setattr__(self, name.replace('-', '_'), value)

class Alerts(DataBlock):
	pass
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(meta)>:
	DOCid: <^[uuid]^>
	name: Organism Level Oraculum Module YAML Configuration Document
	description: >
	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>pheonix/organism/oraculum/z-data_/oraculum.yaml
	outline: <[outline]>
	authority: document|this
	security: seclvl2
	<(wt)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
# forecast.py
from __future__ import print_function
from builtins import super
import json
import sys
import requests
from .data import DataPoint
_API_URL = 'https://api.darksky.net/forecast'
class Forecast(DataPoint):
	def __init__(self, key, latitude, longitude, time=None, timeout=None, **queries):
		self._parameters = dict(key=key, latitude=latitude, longitude=longitude, time=time)
		self.refresh(timeout, **queries)
#this two functions are what turns the dictionary into a callable object use this
#with in the monk functionality to increase the usefulness of Configuration files
	def __setattr__(self, key, value):
		if key in ('_queries', '_parameters', '_data'):
			return object.__setattr__(self, key, value)
		return super().__setattr__(key, value)
	def __getattr__(self, key):
		if key in self.currently._data.keys():
			return self.currently._data[key]
		return object.__getattribute__(self, key)
#this may have something to do with use of the "with" statement
	def __enter__(self):
		return self
	def __exit__(self, type, value, tb):
		del self
	@property#not sure what this really does
	def url(self):
		time = self._parameters['time']
		timestr = ',{}'.format(time) if time else ''
		uri_format = '{url}/{key}/{latitude},{longitude}{timestr}'
		return uri_format.format(url=_API_URL, timestr=timestr, **self._parameters)
	def refresh(self, timeout=None, **queries):
		self._queries = queries
		self.timeout = timeout
		request_params = {
			'params': self._queries,
			'headers': {'Accept-Encoding': 'gzip'},
			'timeout': timeout}
		response = requests.get(self.url, **request_params)
		self.response_headers = response.headers
		if response.status_code is not 200:
			raise requests.exceptions.HTTPError('Bad response')
		return super().__init__(json.loads(response.text))

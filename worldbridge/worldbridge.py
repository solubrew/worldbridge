#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: 91438485-b6d5-44fc-a85b-3dba751b0a85
	name:
	description: >

	expirary: <[expiration]>
	Version: <[Version]>
	path: <[LEXIvrs]>panda/LEXI/
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
# from __future__ import print_function
# from builtins import super
from os.path import abspath, dirname, join

# import datetime as dt, errno, json, logging, queue as q, requests, time, sys#	||
#
# from subprocess import Popen, PIPE#										||
# from requests import Request, Session
# import shutil#			||
# import ctypes, select, socket, random, string, time#						||
# try:#																	||
# 	import _winreg, serial#												||
# except:#																||
# 	print('No module _winreg')#											||
#===============================================================================||
from worldbridge.libs import DataFrame
#===============================================================================||
from condor import condor
from fxsquirl import collector
#===============================================================================||
here = join(dirname(__file__),'')#								||
there = abspath(join('../../..'))#								||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
pxcfg = join(abspath(here), '_data_/worldbridger.yaml')#								||use default configuration
class stone(collector.engine):#
	'Object controlling the groups of devices'
	def __init__(self, cfg={}):#	||
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg)
		collector.engine.__init__(self, self.config)
	def loadAPIKeys(self, keys):
		'''Supply users API keys for the various services through the user
			session configuration allow applications building on top of
			worldbridger to supply these keys'''
		self.apikeys = keys
		return self
	def fetchWebPage(self):
		''' '''
		self.html = monql.doc(path).read()
		return self
	def getAsset(self, url: str, mods: dict={}):
		'''Download a specific asset..integrate video downloading tool...primarily
			youtube_dl not sure if i need other tools for video....also integrate
			html and image saving tools'''
		if mods != {}:
			mods = self._modAssetDownload(url, mods)
		if mods['pdf'] == True:
			pdf = monql.doc(url).pdf()
		if mods['doc'] == True:
			doc = ''
		if mods['video'] == True:
			vid = ''
		if mods['image'] == True:
			img = ''
		if mods ['audio'] == True:
			aud = ''
		return self
	def _crawltag(self, dikt):
		'''Crawl through links to assign branch data to a column'''
		for key in dikt:
			if isinstance(dict, dikt[key]):
				self._crawltag(dikt[key])
			else:
				return dikt[key]
#==============================Source Materials=================================||
'''
https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=YOUR_API_KEY
https://superuser.com/questions/632979/if-i-know-the-pid-number-of-a-process-how-can-i-get-its-name
https://stackoverflow.com/questions/17440585/how-to-get-pid-of-process-by-specifying-process-name-and-store-it-in-a-variable
http://pubs.opengroup.org/onlinepubs/009696799/utilities/ps.html
http://snipplr.com/view/14807/
'''
#================================:::DNA:::======================================||
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
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

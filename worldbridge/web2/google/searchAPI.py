'''
---
<(meta)>:
	DOCid: <^[uuid]^>
	name:
	description: >

	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>/pheonix/organisms/djynn/z-data_/djynn.yaml
	outline: <[outline]>
	authority: document|this
	security: seclvl2
	<(wt)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from __future__ import print_function
from os.path import abspath, dirname, join
import re, sys, traceback
from random import choice
#===============================================================================||
from urllib import request
from html.parser import HTMLParser # keep it to avoid warning
from urllib.parse import quote, unquote
from html import unescape  # Python 3.4+
#===============================================================================||
from pheonix.elements.comm import comm#											||
from pheonix.elements.config import config#										||
from pheonix.elements.store import store#										||
from pheonix.elements.store.orgnql import monql
from pheonix.molecules.collector import collector
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
class api(object):
	def __init__(self, cfg={}):
		''' '''
		pxcfg = '{0}z-data_/google.yaml'.format(here)
		self.config = config.instruct(pxcfg).select('searchAPI').override(cfg)
	def download(self, query, num_results):
		"""downloads HTML after google search"""
		name = quote(query)
		url = 'http://www.google.com/search?q={0}'.format(name.replace(' ','+'))
		url += '&num={0}'.format(str(num_results))  # adding this param might hint Google towards a bot
		user_agents = self.config.dikt['user_agents']
		req = request.Request(url, headers={'User-Agent' : choice(user_agents),})
		response = request.urlopen(req)
		return str(response.read(), 'utf-8', errors='ignore')
	def is_url(self, url):
		"""checks if :url is a url"""
		regex = r'((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)'
		return re.match(regex, url) is not None
	def prune_html(self, text):
		""""""
		text = re.sub(r'<.*?>', '', text)
		return text
	def convert_unicode(self, text):
		"""converts unicode HTML to real Unicode"""
		try:
			s = unescape(text)
		except Exception:
			# Python 3.3 and below
			# https://stackoverflow.com/a/2360639/2295672
			s = HTMLParser().unescape(text)
		return s
	def search(self, term, num_results=10):
		"""searches google for :query and returns a list of tuples of the
			format (name, url)"""
		data = self.download(term, num_results)
#		print('Search Data', data)
		results = next(monql.doc(data, {'orgnql': {'code': 'HTML'}}).read())
		links = results.links().links
#		print('Results', results)
#		results = re.findall(r'\<h3.*?\>.*?\<\/h3\>', data, re.IGNORECASE)
#		if results is None or len(results) == 0:
#			print('No results where found. Did the rate limit exceed?')
#			return []
		# results = data
		# print('RESULTS', results)
		# links = []
		# for r in results:
		# 	mtch = re.match(r'.*?a\s*?href=\"(.*?)\".*?\>(.*?)\<\/a\>.*$', r, flags=re.IGNORECASE)
		# 	mtch = re.match(r'*href*', r, flags=re.IGNORECASE)
		# 	if mtch is None:
		# 		print('No match')
		# 		continue# parse url
		# 	url = mtch.group(1)# clean url
		# 	url = re.sub(r'^.*?=', '', url, count=1) # prefixed over urls \url=q?
		# 	url = re.sub(r'\&amp.*$', '', url, count=1) # suffixed google things
		# 	url = unquote(url)# url = re.sub(r'\%.*$', '', url) # NOT SAFE, causes issues with Youtube watch url# parse name
		# 	name = self.prune_html(mtch.group(2))
		# 	print('name', name)
		# 	name = self.convert_unicode(name)
		# 	# append to links
		# 	if self.is_url(url): # can be google images result
		# 		links.append((name, url))
		return links

def run():
	"""CLI endpoint to run the program	"""
	results = search(sys.argv[1])


'''
https://stackoverflow.com/a/42461722/2295672
https://stackoverflow.com/questions/11818362/how-to-deal-with-unicode-string-in-url-in-python3
https://github.com/aviaryan/pythons/blob/master/Others/GoogleSearchLinks.py
'''

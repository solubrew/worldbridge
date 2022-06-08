#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: <^[uuid]^>
	name: Molecules Level Worldbridger Module Wikipedia Library Python Document
	description: >
	version: 0.0.0.0.0.0
	path: <[LEXIvrs]>/panda/LEXI/LEXI.yaml
	outline:
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, join
import datetime as dt#															||
#===============================================================================||
import wikipedia
#===============================================================================||
from pheonix.elements.calcgen import tree as calctr
from pheonix.elements.config import config
from pheonix.elements.store.orgnql import monql
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
class src(object):#																||
	''' '''
	def __init__(self):
		''' '''
		self.data = {}
		self.actvterm = None
	def search(self, term, how='first'):#										||
		'''Utilize Wikipedia API to search topic returns list of suggestions#	||
			use a suggestion to return object'''
		if term != self.actvterm:
			self.actvterm = term
		else:
			print('Search Not Ran', self.actvterm)#								||
			return self
		try:
			results = wikipedia.search(term)#									||
			if not isinstance(results, list):
				results = [results]
			print('Results', results)
		except Exception as e:
			print('Wikipedia Search Failed due to',e)#							||
			return self#														||
		try:
			self.data[term] = {}
			if len(results) < 2:
#				print('less than 2')
				self.data[term][results[0]] = wikipedia.suggest(results[0])#	||
			elif how == 'first':#												||
#				print('first', results[0])
				entry = wikipedia.suggest(results[0])
#				print('ENTRY', entry)
				self.data[term][results[0]] = wikipedia.suggest(results[0])#	||
			elif how == 'random':#												||
#				print('random')
				pos = thing.random(0, len(results))#							||
				self.data[term][results[pos]] = wikipedia.suggest(results[pos])#||
			else: #how == 'all':#													||
				for result in results:#											||
#					print('loop', result)
					entry = wikipedia.suggest(result)
#					print('ENTRY', entry)
					self.data[term][result] = wikipedia.suggest(result)#		||
		except Exception as e:
			print('Wikipedia Results Extraction Failed due to',e)#				||
		print('Return search')
		return self
	def getEntries(self, term, how='first'):
		''' '''
		self.search(term, how)
		print('Search Returned')
		results = list(self.data[term].keys())
		print('Result', results)
		while True:
			result = results.pop()
			try:
				yield wikipedia.page(result)
			except Exception as e:
				print('Exception1', e.title)
				try:
					try:
						e.options.pop(e.options.index(result.lower()))
					except:
						pass
					results += e.options
				except Exception as e:
					print('Exception2', e)
					results = []
				results = [x.lower() for x in results if x.lower() not in results]
				print('END Results', results)
				if results == []:
					break
		yield None
	def getImages(self, term, how='simple'):
		'''Crawl html page and collect images from links and embed'''
		self.search(term, how)
		return images
	def getLinks(self, term, how='simple'):
		'''Crawl html page and collect url links'''
		self.search(term, how)
		return links
	def getTables(self, term, how='first'):
		'''Crawl html page and collect data tables'''
		kind = {'ognql': {'code': 'HTML'}}
		atables = calctr.stuff({})
		entries = self.getEntries(term, how)
		while True:
			page = next(entries, None)
			print('PAGE', page)
			if page == None:
				break
			tables = next(monql.doc(page.html(), kind).read()).getTables().dfs
			for key in tables.keys():
				print('Table Keys', key)
			atables.merge(tables)
		return atables.it
#===============================Source Materials================================||
'''

'''
#=================================:::DNA:::=====================================||
'''
<(DNA)>:
	administer:
		version: <[active:.version]>
		test:
		description: >
			<[description]>
		work:
	here:
		version: <[active:.version]>
		test:
		description: >
			<[description]>
		work:
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

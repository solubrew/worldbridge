#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: <^[uuid]^>
	name:
	description: >
	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
from os.path import abspath, dirname, join, realpath
from os import listdir
from pathlib import Path
from sys import argv
from os import chdir, getcwd
import json as j

from pandas import DataFrame
#=======================================================================||
from condor import condor
from fxsquirl.orgnql import sonql, fonql, yonql
from fxsquirl import selector
from rhino.versys import git
#=======================================================================||
here = join(dirname(abspath(__file__)),'')#						||
there = abspath(join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
log = True
#=======================================================================||
pxcfg = f'{here}_data_/utils.yaml'
def getCryptoAssets(to):
	'''Collect crypto assets from known web2 sources '''
	gitsrcs = ['trustwallet', ]
	gitter = git.linkage(pxcfg)
	for gitsrc in gitsrcs:
		path = gitter.config.dikt['repos'][gitsrc]['endpoints']['assets']
		gitter.os.set_working_directory(to)
		gitter.clone(path['url'], to)
	#need to add moonbags service

def loadCryptoAssets(frm, db='assets.db'):
	'''Load downloaded directories of assest into a database and also use
		to augment web3 protocols structure '''
	path = realpath(join(here, '../..', 'web3/protocols/'))
	db = join(abspath(f'{path}'), f'{db}'
	wrtr = sonql.doc(db)
	wrtr.drop(table, 3369)
	chains, records = {'arbitrum': 42161, 'ethereum': 1, 'polygon': 137, 'avalanchec': 43114}, []
	fpath = realpath(join(frm, 'assets/blockchains/'))
	for chain in listdir(fpath):
		print('Chain',chain)
		if chain in chains:
			print('path', f'{fpath}/{chain}/tokenlist.json')
			#tokens = next(yonql.doc(f'{fpath}/{chain}/tokenlist.json').read()).dikt
			with open(f'{fpath}/{chain}/tokenlist.json', 'r') as doc:
				tokens = j.loads(doc.read())
			print(tokens)
			for token in tokens['tokens']:
				if log:print(f'Token {token["name"]}')
				token['chainId'] = chains[chain]
				cid = token['chainId']
				try:
					record = [token['name'], token['chainId'], token['symbol'],
											token['address'], token['decimals'],
																token['type']]
					records.append(record)
				except:
					if log:print(f'Token {token["name"]} failed')
					continue
				bloom = token['name'][:1].lower()
				bloom_path = f'{path}/{bloom}'
				tmplt = ''
				name = token["name"].lower().replace(' ', '').replace('.', '')
				name = name.replace('_', '').replace('-', '')
				protocol_path = f'{bloom_path}/{name}.py'
				fonql.touch(protocol_path)
				image_path = f'{bloom_path}/_data_/img/{cid}{name}.png'
				selector.webImageGrab(token['logoURI'], image_path)
				tmplt = ''
				config_path = f'{bloom_path}/_data_/{name}.yaml'
				fonql.touch(config_path)
				doc = yonql.doc(config_path)
				data = next(doc.read()).dikt
				if data == None:
					data = {}
				try:
					data.pop('token')
				except:
					pass
				token['logoURI'] = image_path
				token.pop('asset')
				token.pop('pairs')
				data['token'] = {cid: token}
				doc.write(data)
				tmplt = ''
	columns = ['name', 'chainid', 'symbol', 'address', 'precision',
																'basecontract']
	if log: print('Records', records)
	df = DataFrame(records, columns=columns)
	wrtr.write({'assets': df})

def runAssetCollection():
	'''Collect known crypto assets from various web2 sources'''
	path = join(abspath(here), '_data_', 'temp')
	fonql.touch(path)
	utils.getCryptoAssets(path)
	utils.loadCryptoAssets(path)
	fonql.kill(path)

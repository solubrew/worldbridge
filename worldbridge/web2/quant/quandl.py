	# -*- coding: utf-8 -*-

import quandl
quandl.ApiConfig.api_key = 'xuDyU3g7wixWRaREWfRQ'

class src(object):
	def __init__(self):
		pass
	def check(data):
		if isinstance(data, dict):
			print('Data is dict')
		elif isinstance(data, list):
			print('Data is List')
		elif isinstance(data, tuple):
			print('Data is Tuple')
		elif isinstance(data, str):
			print('Data is string')
		else:
			print('Data unknown')
	def view(data):
		for key, lines in data.items():
			print(key,line)
			print('This is the key ',data[key])
			print('This is the key ',key, lines)
		for key0, line in lines.items():
			check(lines.key)
			print(key0, line)
			for line in lines:
				print('This is the line ',line)
	#quandl.bulkdownload("LMBA/SILVER", filename="./LMBA_Silver.zip")
	#data = quandl.get("WIKI/FB")
	#data = quandl.get_table("COM/WLD_SILVER")
	#data = quandl.get("COM/WLD_SILVER")
	#data = quandl.get("COM/AG_FAB")
	#data = quandl.get("COM/AG_EFP")#
	data = quandl.get("COM/AG_USD")#London Fixing Silver Price
	#data = quandl.get("COM/WLD_SILVER", authtoken="xuDyU3g7wixWRaREWfRQ")

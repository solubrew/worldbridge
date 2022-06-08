#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: <^[uuid]^>
	name: Molecules Level Languager Module Gmail Extension Python Document
	description: >
		Script to count messages by user posted to a channel for a given date range.
		Install:
		# sudo pip install slackclient
		Also you will need to obtain a slack API token:
			https://api.slack.com/docs/oauth-test-tokens
		Usage Example:
		# python SLACK_SEARCH_FROM=2016-11-01 SLACK_SEARCH_TO=2016-12-01 \
			SLACK_CHANNEL_NAME=general SLACK_API_TOKEN=<token> \
			slack-messages-by-user.py
	version: 0.0.0.0.0.0
	path: <[LEXIvrs]>/panda/LEXI/LEXI.yaml
	outline:
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
#=======================================================================||
import datetime as dt, os

#=======================================================================||
try:
	from httplib2 import Http
except Exception as e:
	print('slackAPI',e)
try:
	from oauth2client import file, client, tools
except Exception as e:
	print('slackAPI',e)
try:
	from slackclient import SlackClient
except Exception as e:
	print('slackAPI',e)
#=======================================================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
there = os.path.abspath(os.path.join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
#=======================================================================||

class client:
	''
	version='0.0.0.0.0.0'#														||
	def __init__(self, uid, cfg=None):#											||
		pxcfg = '{0}z-data_/slack.yaml'.format(here)#							||use default configuration
		self.config = config.instruct(pxcfg).load().override(cfg).dikt#	||
		slack_token = self.config['solutionsbrewer']['lexi']['token']
	def timebox(self):
		#change to use tmapr
		slack_token = os.environ["SLACK_API_TOKEN"]
		channel_name = os.environ["SLACK_CHANNEL_NAME"]
		date_from = os.environ["SLACK_SEARCH_FROM"]
		date_to = os.environ["SLACK_SEARCH_TO"]
		self.oldest = (datetime.strptime(date_from, "%Y-%m-%d") - datetime(1970, 1, 1)).total_seconds()
		self.latest = (datetime.strptime(date_to, "%Y-%m-%d") - datetime(1970, 1, 1)).total_seconds()
		return self
	def connectAPI(self):
		''
		self.sc = SlackClient(slack_token)
		return self
	def getChannels(self):
		''
		#output list of channels to the correct POV
		channel_name = os.environ["SLACK_CHANNEL_NAME"]
		channels = sc.api_call("channels.list")
		channel_id = None
		for channel in channels['channels']:
			if channel['name'] == channel_name:
				channel_id = channel['id']
		if channel_id == None:
			raise Exception("cannot find channel " + channel_name)
		return self
	def getMessages(self, channel=None):
		''
		history = self.sc.api_call("channels.history", channel=channel_id, oldest=oldest, latest=latest)
		posts_by_user = {}
		for message in history['messages']:
			if message['user'] in posts_by_user:
				posts_by_user[users[message['user']]] += 1
			else:
				posts_by_user[users[message['user']]] = 1
		for user, count in posts_by_user.items():
			print(user, 'posted', count, 'messages')
	def getUsers(self):
		''
		users_list = self.sc.api_call("users.list")
		users = {}
		for user in users_list['members']:
			users[user['id']] = user['profile']['first_name'] + ' ' + user['profile']['last_name']
		return self
#==========================Source Materials=============================||
'''
https://gist.github.com/demmer/617afb2575c445ba25afc432eb37583b


Script to count messages by user posted to a channel for a given date range.
Install:
# sudo pip install slackclient
Also you will need to obtain a slack API token:
    https://api.slack.com/docs/oauth-test-tokens
Usage Example:
# python SLACK_SEARCH_FROM=2016-11-01 SLACK_SEARCH_TO=2016-12-01 \
         SLACK_CHANNEL_NAME=general SLACK_API_TOKEN=<token> \
         slack-messages-by-user.py

import os
from datetime import datetime
from slackclient import SlackClient
slack_token = os.environ["SLACK_API_TOKEN"]
channel_name = os.environ["SLACK_CHANNEL_NAME"]
date_from = os.environ["SLACK_SEARCH_FROM"]
date_to = os.environ["SLACK_SEARCH_TO"]
oldest = (datetime.strptime(date_from, "%Y-%m-%d") - datetime(1970, 1, 1)).total_seconds()
latest = (datetime.strptime(date_to, "%Y-%m-%d") - datetime(1970, 1, 1)).total_seconds()
sc = SlackClient(slack_token)
users_list = sc.api_call("users.list")
users = {}
for user in users_list['members']:
    users[user['id']] = user['profile']['first_name'] + ' ' + user['profile']['last_name']
channels = sc.api_call("channels.list")
channel_id = None
for channel in channels['channels']:
    if channel['name'] == channel_name:
        channel_id = channel['id']
if channel_id == None:
    raise Exception("cannot find channel " + channel_name)
history = sc.api_call("channels.history", channel=channel_id, oldest=oldest, latest=latest)
posts_by_user = {}
for message in history['messages']:
    if message['user'] in posts_by_user:
        posts_by_user[users[message['user']]] += 1
    else:
        posts_by_user[users[message['user']]] = 1
for user, count in posts_by_user.items():
print user, 'posted', count, 'messages'



'''
#============================:::DNA:::==================================||
'''
<(dna)>:
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

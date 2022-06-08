#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: 5f3184b2-fdbc-478f-ab2c-c68fead2956d
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
import pickle, base64 as b64
import os.path
#===========================3rd Party Modules===========================||
try:
	from googleapiclient.discovery import build
	from google_auth_oauthlib.flow import InstalledAppFlow
	from google.auth.transport.requests import Request
except:
	pass
#=======================================================================||
from pheonix.elements.comm import comm#									||
from worldbridger.social.google import googleAPI#			||
#=======================================================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
there = os.path.abspath(os.path.join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
#=======================================================================||
class rclient(googleAPI.client):
	''
	version='0.0.0.0.0.0'
	def __init__(self):
		#service: Authorized Gmail API service instance.
		#user_id: User email value "me" can be used for authenticated user
		self.uid = 'me'
		self.pull, self.tokn = True, None
		SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
		google.client.__init__(self, self.uid, SCOPES)
		self.buildService(self.creds)
	def buildService(self, creds):
		self.srv = build('gmail', 'v1', credentials=self.creds)#	||need to use https
		return self
	def getLabels(self):
		'Get All Labels from Account'
		lblserv = self.srv.users().labels()
		labels = self.pullMessages(lblserv)
		self.labels = labels.get('labels', [])
		return self
	def getMessages(self, lvl=0, by=None, this={}):#use by for label, and other filtering
		''
		if by == 'Label':
			labels = [this.values()]
		elif by == 'Query':
			query = 'from:<[user]>@<[doamin]>'
			params = {'q': query}
		if by == 'History':
			msgsrv = self.srv.users().history()
		else:
			msgsrv = self.srv.users().messages()
		self.messages, messages = [], True
		while messages:
			messages = next(self.pullMessages(msgsrv))
			if lvl == 0:# Get Message IDs
				if messages:
					self.messages.extend(messages['messages'])
			elif lvl == 1:# Get Message Headers
				pass
			elif lvl == 2:# Get Message Headers & Snippet
				pass
			elif lvl == 3:# Get Common Message Data
				pass#from, to, recieved, sent, subject, body, labels
			elif lvl == 4:# Get Body Messages Only
				for m in messages:
					msg = self.getMessage(m['id'])
					body = msg['payload']['parts'][1]['body']#	||
					body = b64.urlsafe_b64decode(body['data'])#	||
					self.messages.append(m['id'], body)
			elif lvl == 5:# Get Full Messages
				pass
			yield self
	def getMessage(self, msgid):
		'Get Message with ID. Args: msg_id: The ID of the Message required.Returns: A Message.'''
		msgsrv = self.srv.users().messages()
		msg = msgsrv.get(userId=self.uid, id=msgid).execute()#	||
#		print(msg['payload']['parts'][0]['body'])
#		msg = base64.urlsafe_b64decode(msg['payload']['parts'][1]['body']['data'])
#		print(msg)
		return msg
	def GetMimeMessage(self, msgid):
		msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
		msg = email.message_from_string(msg_str)
		return msg
	def pullMessages(self, serv, how='list', i=None, f=None):
		while self.pull == True:
			if self.tokn != None:
				params = {'userId': self.uid, 'pageToken': self.tokn}
			else:
				params = {'userId': self.uid}
			if f != None:
				params['format'] = f
			try:
				if how == 'list':
					r = serv.list(**params).execute()
					if 'nextPageToken' in r:
						if self.tokn == r['nextPageToken']:
							self.pull = False
						else:
							self.pull = True
						self.tokn = r['nextPageToken']
				elif how == 'get':
					r = self.get(**params, id=i).execute()
			except Exception as e:
				comm.see(['An error occurred: %s' % e])
				self.pull = False
				r = False
			yield r
class wclient(googleAPI.client):
	'Use to Write eMails and Apply Labels/Move to Folders'
	version='0.0.0.0.0.0'
	def __init__(self):
		#service: Authorized Gmail API service instance.
		#user_id: User email value "me" can be used for authenticated user
		self.srv = build('gmail', 'v3', http=http, credentials=creds)#	||need to use https
		self.uid = 'me'
		SCOPES = ['https://www.googleapis.com/auth/gmail.readwrite']
		google.client.__init__()
	def writeMessage(self):
		''
		return self
	def saveMessage(self):
		''
		return self
	def sendMessage(self):
		''
		return self
	def addLabels(self):
		''
		return self
	def rmvLables(self):
		''
		return self
class aclient(googleAPI.client):
	'Uset to Adminstrate email Entanglement'
	version='0.0.0.0.0.0'
	def __init__(self):
		#service: Authorized Gmail API service instance.
		#user_id: User email value "me" can be used for authenticated user
		self.srv = build('gmail', 'v3', http=http, credentials=creds)#	||need to use https
		SCOPES = ['https://www.googleapis.com/auth/gmail.readwrite']
		self.uid = 'me'
		google.client.__init__()
	def makeLabel(self):
		''
		return self
	def makeRule(self):
		''
		return self
class backup:
	def __init__(self, service):
		self.roster = []
		self.getMessages(service)
	def getMessages(self, service=None):
		if service == 'gmail':
			self.rclient = gmail.rclient()
			cnt, msgs = 0, True
			while msgs:
				msgs = next(self.rclient.getMessages()).messages
				self.storMessages(msgs, cnt)
				cnt += 1
				comm.see(['Page Count ',cnt])
	def storMessages(self, msgs, cnt):
		for m in msgs:
			mid = m['id']
#			if mid not in self.roster:
#				self.roster.append(mid)
			msg = self.rclient.getMessage(mid)
			entgl = '/0/solubrew/JDB/brewer.joe/'
			name = '<[VEINvrs.UserVein]>'+entgl+'commdata/'+service
			name = '/home/solubrew/verse-a/UserVein/0/solubrew/JDB/brewer.joe/commdata/gmail'
			name +='/p'+str(cnt)
			if not os.path.exists(name):
				os.makedirs(name)
			name += '/'+msg['id']+'.yaml'
			with open(name, 'w') as doc:
				dump(msg, doc, Dumper=Dumper)
			doc.close()
		return self
#==========================Source Materials=============================||
'''











#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
from __future__ import print_function
import httplib2, os, datetime as dt
import apiclient
#import apiclient.discovery as discovery
#from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
#from apiclient import errors
import base64
import email
import pheonix
#=======================================================================||
#=======================================================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
there = os.path.abspath(os.path.join('../../..'))#						||set path at pheonix level
o = obs.focus().messages().outs# 										||
version = '0.0.0.0.0.0'#												||
#=======================================================================||
def monitor():
	pass#gmail = need an on recieve function to connect to
def scan():
	pass
def process(messages):
	log(messages)
	tag(messages)
	distribute(messages)
def tag(messages):
	pass#apply tags based on conversation tags, contacts in the email,
def distribute(messages):
	pass#based on tags
def log(messages):
	dump = ''
	pheonix.log.log.raw(dump)
#Get a list of Messages from the user's mailbox
def ListMessagesMatchingQuery(service, user_id, query=''):
#List all Messages of the user's mailbox matching the query.
#	Args:	service: Authorized Gmail API service instance.
#		user_id: User's email address. The special value "me"
#		can be used to indicate the authenticated user.
#		query: String used to filter messages returned.
#		Eg.- 'from:user@some_domain.com' for Messages from a particular sender.
#	Returns:
#		List of Messages that match the criteria of the query. Note that the
#		returned list contains Message IDs, you must use get with the
#		appropriate ID to get the details of a Message."""
	try:
		response = service.users().messages().list(userId=user_id,q=query).execute()
		messages = []
		if 'messages' in response:
			messages.extend(response['messages'])
		while 'nextPageToken' in response:
			page_token = response['nextPageToken']
			response = service.users().messages().list(userId=user_id, q=query,pageToken=page_token).execute()
			messages.extend(response['messages'])
		return messages
	except:#(errors.HttpError, errors):
#		print('An error occurred: %s' % errors)
		print('e')
def ListMessagesWithLabels(service, user_id, label_ids=[]):
	"""List all Messages of the user's mailbox with label_ids applied.
	Args:
		service: Authorized Gmail API service instance.
		user_id: User's email address. The special value "me"
		can be used to indicate the authenticated user.
		label_ids: Only return Messages with these labelIds applied.
	Returns:
		List of Messages that have all required Labels applied. Note that the
		returned list contains Message IDs, you must use get with the
		appropriate id to get the details of a Message."""
	try:
		response = service.users().messages().list(userId=user_id,labelIds=label_ids).execute()
		messages = []
		if 'messages' in response:
			messages.extend(response['messages'])
		while 'nextPageToken' in response:
			page_token = response['nextPageToken']
			response = service.users().messages().list(userId=user_id,labelIds=label_ids,pageToken=page_token).execute()
			messages.extend(response['messages'])
		return messages
	except(errors.HttpError, errors):
		print ('An error occurred: %s' % errors)
#-----------------------give list of messages to iterator and create a list of email addresses------
#-----------------------Get a current list of filters and create a new list of filters
"""Get Message with given ID."""
def GetMessage(service, user_id, msg_id):
	"""Get a Message with given ID.
	Args: service: Authorized Gmail API service instance.
		user_id: User's email address. The special value "me"
		can be used to indicate the authenticated user.
		msg_id: The ID of the Message required.
	Returns: A Message."""
	try:
		message = service.users().messages().get(userId=user_id, id=msg_id).execute()
		print('Message snippet: %s' % message['snippet'])
		return message
	except (errors.HttpError, errors):
		print('An error occurred: %s' % errors)
def GetMimeMessage(service, user_id, msg_id):
	"""Get a Message and use it to create a MIME Message.
	Args: service: Authorized Gmail API service instance.
		user_id: User's email address. The special value "me"
		can be used to indicate the authenticated user.
		msg_id: The ID of the Message required.
	Returns: A MIME Message, consisting of data from Message."""
	try:
		message = service.users().messages().get(userId=user_id, id=msg_id,format='raw').execute()
		print('Message snippet: %s' % message['snippet'])
		msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
		mime_msg = email.message_from_string(msg_str)
		return mime_msg
	except (errors.HttpError, errors):
		print('An error occurred: %s' % errors)
def get_credentials():
	"""Gets valid user credentials from storage.
	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.
	Returns: Credentials, the obtained credential. """
	try:
		import argparse
		flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
	except ImportError:
		flags = None
	SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
	CLIENT_SECRET_FILE = 'client_secret.json'
	APPLICATION_NAME = 'Gmail API Python Quickstart'
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,'gmail-python-quickstart.json')
	store = oauth2client.file.Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatability with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials
def connect():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)
	return service
def get_labels():
	"""Shows basic usage of the Gmail API.Creates a Gmail API service object and
	outputs a list of label names of the user's Gmail account."""
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)
#	results = service.users().labels().list(userId='me').execute()
	results = service.users().messages().list(userId='me').execute()
	labels = results.get('labels', [])
	if not labels:
		print('No labels found.')
	else:
		print('Labels:')
		for label in labels:
			print(label['name'])
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
#Python Quick Start https://developers.google.com/gmail/api/quickstart/python
#http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#imaplib & oauth
#	http://stackoverflow.com/questions/5193707/use-imaplib-and-oauth-for-connection-with-gmail
#Google oauth2
#	http://stackoverflow.com/questions/8561739/how-to-use-google-oauth2-access-token?lq=1
#Gmail python
#	http://stackoverflow.com/questions/17708141/connecting-to-gmail-from-python
#libgmail
#	http://libgmail.sourceforge.net/
#gdata python client
#https://github.com/google/gdata-python-client
#https://developers.google.com/google-apps/calendar/v3/reference/
#Google-Calendar-API
#	https://developers.google.com/google-apps/calendar/quickstart/python
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||





















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

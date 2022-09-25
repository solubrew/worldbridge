#@@@@@@@@@@@@@@Pheonix.Organelle.Collector.Collector@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid:
	name:	Level	Module Python Document
	description: >
		Leverage monql module to read and webpage and extract video specializing
		on youtube sourced video
	expirary: <^[expiration]^>
	version: <^[version]^>
	path: <[LEXIvrs]>pheonix/.py
	outline: <[outline]>
	authority: document|this
	security: seclvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
import os, datetime as dt, time, random, sys, httplib, httplib2#		||
#===========================3rd Party Modules===========================||
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from youtube_dl import YoutubeDL
from youtube_dl.compat import compat_http_server
from youtube_dl.downloader.http import HttpFD
from youtube_dl.utils import encodeFilename
import threading

#=======================================================================||
from pheonix.elements.config import config#								||
#=======================================================================||
here = join(dirname(__file__),'')#								||
there = abspath(join('../../..'))#								||set path at pheonix level
home = expanduser('~')
version = '0.0.0.0.0.0'#														||
#===============================================================================||

class api(object):
	def __init__(self):
		''
		cfg = here+'/z-data_/google.yaml'
		self.config = config.instruct(cfg).select('youtubeAPI').dikt
	def variables(self):
		self.retry = self.config['upload']['retry']['options']
		self.client = self.config['oalth']['client']
		httplib2.RETRIES = self.retry['num']#							||set HTTP transport library not to retry
		RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError,#		||
						httplib.NotConnected, httplib.IncompleteRead,#	||
			httplib.ImproperConnectionState,httplib.CannotSendRequest,#	||
				httplib.CannotSendHeader, httplib.ResponseNotReady,#	||
												httplib.BadStatusLine)#	||
		path = os.path.abspath(os.path.join(os.path.dirname(__file__),
										self.client['secrets_file']))#	||
		self.msg = oath['client']['missing_secret']['msg'].format(path)#||
		return self
	def get_authenticated_service(args):#								||
		flow = flow_from_clientsecrets(self.client['secrets_file'],#	||
									scope=self.client['upload_scope'],#	||
													message=self.msg)#	||
		storage = Storage('{0}-oauth2.json'.format(sys.argv[0]))
		credentials = storage.get()
		if credentials is None or credentials.invalid:
			credentials = run_flow(flow, storage, args)
		return build(self.client['service_name'],
										self.client['api_version'],#	||
						http=credentials.authorize(httplib2.Http()))#	||
	def initialize_upload(youtube, options):
		tags = None
		if options.keywords:
			tags = options.keywords.split(",")
		body=dict(snippet=dict(
						title=options.title,
						description=options.description,
						tags=tags,
						categoryId=options.category),
		status=dict(privacyStatus=options.privacyStatus))
		# Call the API's videos.insert method to create and upload the video.
		insert_request = youtube.videos().insert(
							part=",".join(body.keys()), body=body,
							media_body=MediaFileUpload(options.file,
														chunksize=-1,
														resumable=True))
		resumable_upload(insert_request)
		# This method implements an exponential backoff strategy to resume a
		# failed upload.
	def resumable_upload(insert_request):
		response, error, retry = None, None, 0
		while response is None:
			try:
				print("Uploading file...")
				status, response = insert_request.next_chunk()
				if 'id' in response:
					print("Video id '{0}' was successfully uploaded.".format(response['id']))
				else:
					exit("The upload failed with an unexpected response: {0}".format(response))
			except HttpError, e:
				if e.resp.status in self.retry['codes']:
					error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
				else:
					raise
			except RETRIABLE_EXCEPTIONS, e:
				error = "A retriable error occurred: %s" % e
			if error is not None:
				print(error)
				retry += 1
				if retry > self.retry['max']:
					exit("No longer attempting to retry.")
				max_sleep = 2 ** retry
				sleep_seconds = random.random() * max_sleep
				print("Sleeping {0} seconds and then retrying...".format(sleep_seconds))
				time.sleep(sleep_seconds)


class Data(worldbridger.stone, YoutubeDL):
	def __init__(self, paths: list=[], loci: str=f'{home}/DataWorkRepo', cfg={}):
		''' '''
		pxcfg = f'{here}z-data_/source.yaml'
		self.config = condor.instruct(pxcfg).select('youtube').override(cfg)
		worldbridger.stone.__init__(self, self.config)
		YoutubeDL.__init__(self)
		if not isinstance(paths, list):
			paths = [paths,]
		self.paths = paths
		self.loci = loci
	def getList(self):
		for path in self.paths:
			self.get(path)
		return self
	def get(self, path: list=[]):
		'''
			need to review YoutubeDL api...this implementation fails
		'''
		YoutubeDL().download(path)
		# self.paths.append(path)
		# for path in self.paths:
		# 	videoSTREAMs = YouTube(path).streams
		# 	stream = self.selectVideo(videoSTREAMs)
		# 	itag = stream.itag
		# 	videoSTREAM = videoSTREAMs.get_by_itag(itag)
		# 	videoSTREAM.download(self.loci)
		return self

	def getVidID(self, url):
		''' '''
		return regex_search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url, group=1)
	def selectVideo(self, videoSTREAMs):
		''
		prefs = self.config['preferences']
		for seq, res in prefs['res'].items():
			streams = videoSTREAMs.filter(res=res).all()
			if streams !=[]:
				break
		if len(streams) > 1:
			for seq, fmat in prefs['format'].items():
				streams = videoSTREAMs.filter(mime_type=fmat, res=res).all()
				if streams != []:
					break
		return streams[0]
	def _modAssetDownload(self, url: str, mods: dict):
		'''Modify asset download to limit things like saving the HTML of generic
			youtube pages'''
		if 'youtube' in url:
			mods['video'] == True
			mods['pdf'] == False
		return mods




if __name__ == '__main__':
	argparser.add_argument("--file", required=True, help="Video file to upload")
	argparser.add_argument("--title", help="Video title", default="Test Title")
	argparser.add_argument("--description", help="Video description", default="Test Description")
	argparser.add_argument("--category", default="22", help="Numeric video category. " "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
	argparser.add_argument("--keywords", help="Video keywords, comma separated", default="")
	argparser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES, default=VALID_PRIVACY_STATUSES[0], help="Video privacy status.")
	args = argparser.parse_args()
	if not os.path.exists(args.file):
		exit("Please specify a valid file using the --file= parameter.")
	youtube = get_authenticated_service(args)
	try:
		initialize_upload(youtube, args)
	except HttpError, e:
		print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
'''
https://developers.google.com/youtube/v3/guides/uploading_a_video
'''

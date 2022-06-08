#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:  #														||
	name:   #														||
	description: >  #															||
	expirary: '<[expiration]>'  #												||
	version: '<[version]>'  #													||
	path: '<[LEXIvrs]>'  #														||
	outline: <[outline]>'  #													||
	authority: 'document|this'  #												||
	security: 'sec|lvl2'  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#==================================Core Modules=================================||
from os.path import abspath, dirname, join#										||
#================================3rd Party Modules==============================||
import binascii, random, time
from hashlib import sha256, sha512
from socket import AF_INET, inet_aton, SOCK_STREAM, socket
from struct import pack
#===============================================================================||
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = join(dirname(__file__))
where = abspath(join('..'))#													||set path at pheonix level
module_path = abspath(join('../../../'))
version = '0.0.0.0.0.0'#														||
page = 200000
#===============================================================================||
class BitcoinBridge(object):
	'''Bitcoin Bridge allows for communication between the bitcoin network and
		organism and higher level pheonix modules'''
	def __init__(self):
		''' '''
		pxcfg =  '{0}z-data_/bitcoin.yaml'.format(here)
		self.config = config.instruct(pxcfg).load()
	def handshake(self):
		''' '''
		# Send message "version"
		s.send(version_message)
		response_data = s.recv(buffer_size)
		# Send message "verack"
		s.send(verack_message)
		response_data = s.recv(buffer_size)
		return self
	def create_sub_version():
		'''Binary encode the sub-version'''
		return b'\x0F{0}'.format(self.config.dikt['sub_version'].encode())
	def create_network_address(ip, port):
		'''Binary encode the network addresses'''
		fhex = self.config.dikt['network']['hex']
		hex = bytearray.fromhex(fhex) + net_aton(ip)
		address = pack('>8s16sH', b'\x01', hex, port)
		return address
	def create_message(self, command, payload):
		'''Create the TCP request object'''
		checksum = sha256(sha256(payload).digest()).digest()[0:4]
		magic = self.config.dikt['magic']
		pack = pack('L12sL4s', magic, command.encode(), len(payload), checksum)
		self.message = pack + payload
		return self
	# Create the "version" request payload
	def create_payload_version(self):
		''' '''
		version = 60002
		services = 1
		timestamp = int(time.time())
		local_addr = create_network_address("127.0.0.1", self.peer_port)
		peer_addr = create_network_address(self.peer_ip, self.peer_port)
		nonce = random.getrandbits(64)
		start_height = 0
		self.payload = struct.pack('<LQQ26s26sQ16sL', version, services,
									timestamp, addr_peer, addr_local, nonce,
									create_sub_version(), start_height)
		return self
	def create_message_verack(self):
		'''Create the "verack" request message'''
		self.verack = bytearray.fromhex(self.config.dikt['verack']['hex'])
		return self
	def create_payload_getdata(tx_id):
		'''Create the "getdata" request payload'''
		count = 1
		type = 1
		hash = bytearray.fromhex(tx_id)
		payload = struct.pack('<bb32s', count, type, hash)
		return(payload)
	def print_response(command, request_data, response_data):
		'''Print request/response data'''
		print("Command: ", command)
		print("Request:", binascii.hexlify(request_data))
		print("Response:", binascii.hexlify(response_data))
	def _conx(self):
		'''Establish TCP Connection'''
		self.peer_ip = self.config.dikt['peers'][0]['ip']
		self.peer_port = self.conifg.dikt['peers'][0]['port']
		self.conx = socket(AF_INET, SOCK_STREAM)
		self.conx.connect((self.peer_ip, self.peer_port))
		return self
class Wallet(object):
	'''Leverage external wallets and limit interaction with private keys from
	 	this application'''
	def __init__(self):
		''' '''



if __name__ == '__main__':
	# Set constants
	tx_id = "fc57704eff327aecfadb2cf3774edc919ba69aba624b836461ce2be9c00a0c20"
	peer_ip_address = '104.198.92.164'  #https://bitnodes.io/nodes/
	peer_tcp_port = 8333
	buffer_size = 1024

	# Create Request Objects
	version_payload = create_payload_version(peer_ip_address)
	version_message = create_message(magic_value, 'version', version_payload)
	verack_message = create_message_verack()
	getdata_payload = create_payload_getdata(tx_id)
	getdata_message = create_message(magic_value, 'getdata', getdata_payload)





	# Send message "getdata"
	s.send(getdata_message)
	response_data = s.recv(buffer_size)
	print_response("getdata", getdata_message, response_data)

	# Close the TCP connection
	s.close()

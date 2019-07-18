import socket
import re
import string
import ipaddress
import requests
import device
from PIL import Image
from io import BytesIO


# Class responsible for holding IP addresses of Roku devices on a network.
class Connection:

	def __init__(self, lookfordevices = True):

		# Initialize the set of ip addresses
		self._ips = set()

		if lookfordevices:
			self.get_device_ips()

	def get_device_ips(self):
		self._ips = find_roku_devices()

	# Get a set of devices, NOT ips
	def get_devices(self):
		return self._ips
		# devs = []
		# for ip in self._ips:
		# 	devs.append(device.Device(ip))

		# return devs

	# activedevice = current roku device
	# command = eg: keypress/volume_up
	def parse_command(self, activedevice, command, get = False):
		response = self.send_command(activedevice.ip, command, get)
		return response

	def send_command(self, ip, path, get = False):
		print("Sending Command: " + str(ip) + str(path))
		if get:
			response = requests.get(ip + path)
			print("Raw response to " + ip + path + ":")
			print(response)
			return response.content.decode('utf-8')
		else:
			requests.post(ip + path)
			return ""

	# Gets an icon (should be a .png)
	def get_icon(self, ip, path):
		response = requests.get(ip + path)
		img = Image.open(BytesIO(response.content))
		print("Image from connector class:")
		print(img)
		return img
		# return response



"""
Available GET commands:
	query/apps
	query/active-app
	query/device-info

Available POST commands:
	keydown/key
	keyup/key
	keypress/key
	launch/appID
	install/appID

Available key values:
	Home
	Rev
	Fwd
	Play
	Select
	Left
	Right
	Down
	Up
	Back
	InstantReplay
	Info
	Backspace
	Search
	Enter
	VolumeDown
	VolumeMute
	VolumeUp
	PowerOff
"""


"""
Everything below this is designed to search for and return
Roku devices on a network.

Call find_roku_devices() to get a set() of devices back.
"""

# Simple abstraction of the "M-SEARCH" message
def __getmessage__():
	"""
	This is just a convenient way to abstract the M-SEARCH method
	"""
	msg = \
		    'M-SEARCH * HTTP/1.1\r\n' \
		    'HOST:239.255.255.250:1900\r\n' \
		    'ST:upnp:rootdevice\r\n' \
		    'MX:2\r\n' \
		    'MAN:"ssdp:discover"\r\n' \
		    '\r\n'

	return msg

# Returns a set() of device IPs found (Roku only)
# Make sure to check for empty sets
def find_roku_devices():
	"""
	This finds all roku devices on a network and returns them
	"""

	found_devices = set()

	# The UPD M-SEARCH message
	msg = __getmessage__()

	# Set up UDP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	s.settimeout(2)
	s.sendto(msg.encode('utf-8'), ('239.255.255.250', 1900) )

	# Counter for the total number of UPnP devices found on the network
	total_devices_found = 0
	# Flag for whether or not any Roku devices have been found
	roku_device_found = False

	try:
		while True:
			data, addr = s.recvfrom(65507)
			data_list = data.decode('utf-8').splitlines()
			ip = parse_input_for_device(data_list)
			if ip:
				found_devices.add(ip)
			total_devices_found += 1

	except socket.timeout:
			print("\n\nFound: " + str(len(found_devices)))

	return found_devices

# Looks for a Roku device
# Returns the ip of the device, if found
def parse_input_for_device(data):
	for line in data:
		print(line)
	for line in data:
		if line.startswith("Server"):
			if "Roku" in line:
				print ("Found a Roku device!")
				# self.debugprintall(data)
				return get_ip(data)

	return None

# Looks for and returns the ip of the device passed
def get_ip(data):
	for line in data:
		if line.startswith("LOCATION"):
			ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
			astring = str(line)
			result = "".join(i for i in astring if i in (string.digits +".:")).strip(":").split(":")
			# print("")
			# print("result: " + str(result))
			ip_addr = "http://" + result[0] + ":" + result[1] + "/"
			print("Combined: " + ip_addr)

			return ip_addr
import Global
import connection
import keyboard_parser
import device
import appgetter

class Controller:
	"""
	Responsible for handling interactions between the GUI and the Rokus.
	This is the controller.
	"""
	def __init__(self, getdevicesonwake = True, makeonlydevicecurrent = True):

		# The connection that will be used to communicate with the Roku devices
		# on the network.
		# Unless "False" is passed, this will automatically find and hold a list
		# of Roku device IP addresses.  To get the addresses, call
		# self.connection.get_devices() -- returns a list
		self.connection = connection.Connection(getdevicesonwake)
		self.current_device = None
		if getdevicesonwake:
			self.gather_roku_devices(makeonlydevicecurrent)
			if makeonlydevicecurrent:
				if len(self.devices) > 0:
					self.current_device = self.devices[0]
		else:
			self.devices = []

		# The keyboard parser
		self.keyboard = keyboard_parser.KBoard()


	# Gets Roku devices, if there is an active connection to a network.
	# If second argument is true, the only device found becomes the active one.
	def gather_roku_devices(self, makeonlydevicecurrent):
		print("Looking for Roku devices...")
		if self.connection:
			ips = self.connection.get_devices()
			self.devices = []

			# Create devices
			# send each device its most recent state and apps
			if len(ips) == 0:
				self.current_device = None
				return
				
			for i in ips:

				# Get device info
				apps = appgetter.doparse(self.connection.send_command(i, "query/apps", True))
				info = appgetter.doparsedeviceinfo(self.connection.send_command(i, "query/device-info", True))

				# Create a Device
				self.devices.append(device.Device(i, apps, info))


				# d.set_state(state)
				# d.set_apps(apps)

				# print(info)
				# print(apps)

			if makeonlydevicecurrent:
				if len(self.devices) == 1:
					self.select_roku_device(self.devices[0])

	def get_current_device_info(self):
		info = appgetter.doparsedeviceinfo(self.connection.send_command(self.current_device.ip, "query/device-info", True))
		return info

	# Pick a roku to be the active device
	def select_roku_device(self, dev):
		for d in self.devices:
			if d.ip == dev:
				self.current_device = d
				return self.current_device


	# Get the active app
	def get_active_app(self):
		if self.current_device:
			_active_app = self.connection.parse_command(self.current_device, ("query/active-app", True))
			return _active_app


	# Track which keys are down
	def register_key_down(self, keycode):
		self.keyboard.add_key(keycode)
	def register_key_up(self, keycode):
		self.keyboard.remove_key(keycode)

	# Gets the keycode, generates the message, and sends it to the device.
	# Also returns a response.
	def execute_keystroke(self, keycode, requireresponse = True, *args):

		command, requiresroku = self.keyboard.parse_key_press(keycode)
		print("Command: " + command)
		# return

		if command == "":
			return command
		if requiresroku:
			if self.current_device == None:
				print("There is no active device to receive the command %s, aborting" % str(command))
				return ""
		else:
			response = self.send_command(command)
			return response


	def send_command(self, command, get = False, *args):
		print("send_command Command: " + command)
		if self.current_device == None:
			print("There is no active device, aborting...")
			return ""

		# cmd = self.parse_keyboard_command(self.current_device, command)
		response = self.connection.parse_command(self.current_device, command, get)
		return response

	def get_icon(self, command):
		if self.current_device == None:
			print("There is no active device, aborting...")
			return

		response = self.connection.get_icon(self.current_device.ip, command)
		return response

	# Parse keyboard commands
	# def parse_keyboard_command(self, active_device, command, *args):
	# 	if active_device == None:
	# 		print("There is no active device, aborting")
	# 		return ""
	# 	response = self.keyboard.parse_command(active_device, command)
	# 	if response != "":
	# 		return response
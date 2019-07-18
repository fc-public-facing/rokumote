import time

class Device:

	def __init__(self, ip, apps, info):
		self.ip = ip
		self.apps = apps
		self.info = info
		self.device_name = self.__getdevicename__(info)
		print("Found: " + str(self.device_name))
		# self.last_state = {}
		# self.apps = {}
		self.__markupdatetime__()

	def update_apps(self, apps):
		self.apps = apps
		self.__markupdatetime__()

	def update_device_info(self, info):
		self.info = info
		self.device_name = self.__getdevicename__(info)
		self.__markupdatetime__()

	def __getdevicename__(self, info):
		if info.get("user-device-name") == None:
			return info.get("friendly-model-name")
		else:
			return info.get("user-device-name")

	# def set_state(self, state):
	# 	self.last_state = {}
	# 	self.__markupdatetime__()

	# def set_apps(self, apps):
	# 	self.apps = {}
	# 	self.__markupdatetime__()

	def __markupdatetime__(self):
		self.last_update = time.time()
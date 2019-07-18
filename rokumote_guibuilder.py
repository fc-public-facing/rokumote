import kivy
from kivy.app import App
from kivy.config import Config
Config.set('graphics','width',800)
Config.set('graphics','height',600)
# Config.set('graphics', 'resizable', False)
# from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from functools import partial

import math
import Global

"""

"""

class MainLayout(Widget):

	def __init__(self, **kwargs):
		super(MainLayout, self).__init__(**kwargs)
		# print ("MainLayout IDs: ", self.ids)

		# Set up the keyboard bindings
		self._keyboard = Window.request_keyboard(
			self._on_keyboard_closed, self, 'text')
		if self._keyboard.widget:
			pass
		self._keyboard.bind(on_key_down = self._on_keyboard_down)
		self._keyboard.bind(on_key_up = self._on_keyboard_up)

		# Register this with Global
		Global.main_layout = self


	# Method for refreshing the devices layout
	def refresh_devices_layout(self, devs = None):
		# Step 1: remove existing devices layout (if it exists)
		if 'devices_layout' in self.__dict__:
			# Remove it!
			self.ids.devices_tab.remove_widget(self.devices_layout)


		height = 0
		if devs == None:
			height = 1
		else:
			height = len(devs)

		self.devices_layout = GridLayout(
			cols = 1)

		if devs == None:
			button = Button(text = "No device found.  Retry?",
				id = "retry")
			# button.bind to search
			self.devices_layout.add_widget(button)
			self.ids.devices_tab.add_widget(self.devices_layout)

		else:
			for dev in devs:
				button = Button(text = "Device at: " + dev.device_name,
					size_hint_y = None,
					id = dev.ip,
					height = 100)
				# button.bind(on_press = partial(self.do_select_device, dev))
				# button.bind to some method in app class
				button.bind(on_press = partial(Global.main_app.do_select_device, dev.ip))
				self.devices_layout.add_widget(button)

			self.ids.devices_tab.add_widget(self.devices_layout)


	# Method for refreshing the apps
	def refresh_apps_layout(self, apps = None, devicename = "Device"):
		# Step 1: remove existing apps layout (if it exists)
		if 'apps_layout' in self.__dict__:
			# Remove it!
			self.ids.app_scroll.remove_widget(self.apps_layout)

		height = 0
		if apps == None:
			height = 1
		else:
			height = len(apps)

		self.apps_layout = GridLayout(
			cols = 3,
			size_hint_y = None,
			height = math.ceil(height / 3) * 100)

		if apps == None:
			label = Label(
				text = "Please connect to a device in the \"Devices\" tab (one tab to the right).",
				size_hint_y = None,
				height = 100)
			self.apps_layout.add_widget(label)
			self.ids.app_scroll.add_widget(self.apps_layout)
			self.ids.app_tab_label.text = "No device connected"

		else:
			for app in apps:
				button = Button(text = apps.get(app),
					size_hint_y = None,
					id = app,
					height = 100)
				button.bind(on_press = partial(Global.main_app.do_select_app, app))
				self.apps_layout.add_widget(button)

			self.ids.app_scroll.add_widget(self.apps_layout)
			self.ids.app_tab_label.text = "Apps on " + devicename

	# Method for refreshing the device info for the current Roku
	def refresh_device_info_layout(self, info):
		pass


	def print_test(self):
		print("MainLayout print was called.")

	# Selects a device.
	# 'dev' = ip address, ex: http://192.168.1.23:8060/
	def do_select_device(self, dev, *args):
		apps = Global.set_device(dev)
		self.populate_app_list(apps)


	def do_get_channel(self, channel, *args):
		for app in Global.interface._apps:

			if channel == app:
				Global.control.__launchchannel__(app)
				return;

		print("Could not find channel: " + channel)

	def do_send_channel(self, chid):
		print(str(chid))
		Global.control.__launchchannel__(chid)


	# Keyboard Handling
	"""
	Doing keyboard stuff in this class because I can't figure out how to do it
	in the "App" class.
	"""



	# Unbind the keyboard
	def _on_keyboard_closed(self):
		print("Keyboard may have been closed!")
		self._keyboard.unbind(on_key_down = self._on_keyboard_down)
		self._keyboard = None

	# Do when keys are pressed
	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):

		Global.controller.register_key_down(keycode)
		Global.controller.execute_keystroke(keycode)


	def _on_keyboard_up(self, keyboard, keycode):

		Global.controller.register_key_up(keycode)




class GuiBuilderApp(App):
	def build(self):
		Global.main_app = self

		_mainlayout = MainLayout()

		Global.main_layout.print_test()
		self.do_refresh_connection()
		# Global.main_layout.refresh_devices_layout(Global.controller.devices)
		# Global.main_layout.refresh_apps_layout(Global.controller.current_device.apps)

		# Global.__setmainapp__(self)

		# img = Global.controller.get_icon("query/icon/12")
		# print("icon data: ")
		# print(img)

		self.do_get_chananel_info()

		return _mainlayout

	# def get_app_icon(self, id):
	# 	img = Global.controller.get_icon("query/icon/" + id)
	# 	return img

	def print_connection_test(self):
		print("This method was called.")

	def do_refresh_connection(self):
		print("Refresh called")
		Global.controller.gather_roku_devices(True)
		Global.main_layout.refresh_devices_layout(Global.controller.devices)
		if Global.controller.current_device != None:
			Global.main_layout.refresh_apps_layout(Global.controller.current_device.apps,
				Global.controller.current_device.device_name)


	def do_toggle_power(self):
		response = Global.controller.get_current_device_info()
		if response["power-mode"] == "PowerOn":
			self.do_basic_command("keypress/PowerOff")
		else:
			self.do_basic_command("keypress/PowerOn")
	# Commands that do not generate responses
	# This includes: volume, arrow, home
	def do_basic_command(self, cmd):
		Global.controller.send_command(cmd)

	def do_get_command(self, cmd):
		return Global.controller.send_command(cmd, True)

	def do_get_chananel_info(self):
		response = self.do_get_command("query/tv-active-channel")
		print(response)

	# Get the device-info for the current Roku.
	def do_get_device_info(self, updatelayout = True):
		response = Global.controller.send_command("query/device-info")
		if response != "":
			if updatelayout:
				Global.main_layout.refresh_device_info_layout(response)
		return response

	# Select an app
	def do_select_app(self, appid, *args):
		Global.controller.send_command("launch/" + appid)

	# Select a device
	def do_select_device(self, deviceip, *args):
		for dev in Global.controller.devices:
			if dev.ip == deviceip:
				Global.controller.select_roku_device(dev.ip)
				Global.main_layout.refresh_apps_layout(Global.controller.current_device.apps)



if __name__ == "__main__":
	Global.__start__()
	GuiBuilderApp().run()
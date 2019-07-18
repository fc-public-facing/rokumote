class KBoard:
	def __init__(self):
		self.shift = False
		self.ctrl = False
		self.current = set()

	def add_key(self, keycode):
		if keycode[1] == 'shift' or keycode[1] == 'rshift':
			self.shift = True
		elif keycode[1] == 'lctrl':
			self.ctrl = True

	def remove_key(self, keycode):
		if keycode[1] == 'shift' or keycode[1] == 'rshift':
			self.shift = False
		elif keycode[1] == 'lctrl':
			self.ctrl = False

	# The True in the tuple indicates whether a Roku needs to be connected
	# for the command to work
	def parse_key_press(self, keycode):
		print("Keycode: " + keycode[1])
		if self.shift:
			if keycode[1] == "up":
				return "keypress/VolumeUp", False
			elif keycode[1] == "down":
				return "keypress/VolumeDown", False
			elif keycode[1] == "spacebar":
				return "keypress/home", False
			else:
				return "keypress/Lit_" + keycode[1], False
		elif self.ctrl:
			if keycode[1] == "m":
				return "keypress/VolumeMute", False
			elif keycode[1] == "spacebar":
				return "keypress/Play", False
			elif keycode[1] == ",":
				return "keypress/Rev", False
			elif keycode[1] == ".":
				return "keypress/Fwd", False
			else:
				return "", False
		else:
			if keycode[1] == "up":
				return "keypress/up", False
			elif keycode[1] == "down":
				return "keypress/down", False
			elif keycode[1] == "left":
				return "keypress/left", False
			elif keycode[1] == "right":
				return "keypress/right", False
			elif keycode[1] == "enter":
				return "keypress/select", False
			elif keycode[1] == "spacebar":
				return "keypress/Lit_ ", False
			elif keycode[1] == "backspace":
				return "keypress/Backspace", False
			else:
				return "keypress/Lit_" + keycode[1], False

		return "", False
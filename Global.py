import keyboard_parser
import rokuhandler


global controller
global main_app
global main_layout


def __start__():
	global controller
	controller = rokuhandler.Controller()

def set_main_app(mainapp):
	global main_app
	main_app = mainapp

def set_main_layout(mainlayout):
	global main_layout
	main_layout = mainlayout
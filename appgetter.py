import xml.etree.ElementTree as ET

def doparse(xml):
	root = ET.fromstring(xml)
	# print("XML ==============================")
	# print(xml)
	# print("XML root:")
	# print(root.tag)
	apps = {}
	for child in root:
		name = child.text
		appid = child.get('id')
		# print(appid + ": " + name)
		apps[appid] = name

	# print(apps)
	return apps

def doparsedeviceinfo(xml):
	root = ET.fromstring(xml)
	# print("XML ==============================")
	# print(xml)
	# print("XML root:")
	# print(root.tag)
	info = {}
	info["serial-number"] = root.find("serial-number").text
	info["device-id"] = root.find("device-id").text
	info["vendor-name"] = root.find("vendor-name").text
	info["model-number"] = root.find("model-number").text
	info["screen-size"] = root.find("screen-size").text
	info["user-device-name"] = root.find("user-device-name").text
	info["friendly-model-name"] = root.find("friendly-model-name").text
	info["power-mode"] = root.find("power-mode").text

	return info
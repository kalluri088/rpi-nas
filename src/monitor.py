import psutil

def ram_usage():
	return psutil.virtual_memory()._asdict()
	
def cpu_usage():
	return {"cpu_percent": psutil.cpu_percent(interval = 1)}

def disk_usage():
	return psutil.disk_usage("/")._asdict()

def cpu_temp():

	try:
		with open("/sys/class/thermal/thermal_zone0/temp") as f:
			temp = int(f.read()) / 1000

		return {"temperature_c": temp}

	except Exception:
		return {"temperature_c": None}

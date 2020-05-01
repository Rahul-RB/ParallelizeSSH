import multiprocessing

class SSHConn(object):
	def __init__(self,hostConfig):
		self.hostConfig = hostConfig
		self.procList = []

	def setupHostDict(self):
		self.procList = [
			multiprocessing.Process(
				target = config["processTarget"],
				kwargs = {**config["processTargetKwArgs"]}
			)
			for host,config in self.hostConfig.items()
		]

	def run(self,waitToExit=False):
		for process in self.procList:
			process.start()

		if waitToExit:
			for process in self.procList:
				process.join()
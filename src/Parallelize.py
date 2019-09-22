from src.Targets import procTarget
from src.Command import Command
import multiprocessing

class Parallelize(object):
	def __init__(self,hostConfig):
		self.hostConfig = hostConfig
		self._procList = []
		# hostConfig = {
		# 	IP:{
		# 		uname:<str>,
		# 		passwd:<str>,
		# 		sshPort:<int>,
		# 		cmds:<tuple>,
		# 		cmdCallbacks:<tuple>,
		# 	}
		# }

		# cmd in cmds can be:
		# <str> or
		# <Command object>

		# callback in cmdCallbacks should be:
		# function name
	
	def setup(self):
		self._procList = [
			multiprocessing.Process(
				target = procTarget,
				kwargs = {
					"IP":host,
					"config":config
				}
			)
			for host,config in self.hostConfig.items()
		]
	
	def run(self,waitToExit=False):
		for process in self._procList:
			process.start()
			# Store process PIDs somewhere.

		if waitToExit:
			for process in self._procList:
				process.join()

	def close(self):
		# Kill all processes (and subprocesses) in self._procList
		pass
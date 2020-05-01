import json
import multiprocessing
import psutil

from ParallelizeSSH.Targets import procTarget
from ParallelizeSSH.Command import Command
from ParallelizeSSH import config

class SSH(object):
	def __init__(self,hostConfig):
		self.hostConfig = hostConfig
		self._procList = []
		# hostConfig = {
		# 	IP:{
		# 		uname:<str>,
		# 		passwd:<str>,
		# 		sshPort:<int>,
		# 		cmds:<tuple>,
		# 	}
		# }

		# cmd in cmds have:
		# 	cmd string - mandatory
		# 	callback - optional
		# 	isThreaded - optional


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
		self.setup()
		pids = []
		for process in self._procList:
			process.start()
			# Store process PIDs somewhere.
			if process.is_alive():
				pids.append(process.pid)

		with open(config.PID_FILE_PATH,"w") as fp:
			json.dump(pids,fp)

		if waitToExit:
			for process in self._procList:
				process.join()

	def close(self):
		timeout = 5

		def onTerminate(proc):
			print("process {} terminated with exit code {}".format(proc, proc.returncode))

		# Kill all processes (and subprocesses) in self._procList
		pids = []
		with open(config.PID_FILE_PATH) as fp:
			pids = json.load(fp)

		for pid in pids:
			proc = psutil.Process(pid)
			procStat = proc.status()

			# Kill the children first
			if procStat not in [psutil.STATUS_ZOMBIE,psutil.STATUS_DEAD,psutil.STATUS_STOPPED]:
				children = proc.children(recursive=True)
				for child in children:
					try:
						child.terminate()
					except psutil.NoSuchProcess:
						pass
				gone, alive = psutil.wait_procs(children, timeout=timeout, callback=onTerminate)
				if alive:
					# send SIGKILL
					for p in alive:
						print("process {} survived SIGTERM; trying SIGKILL".format(p))
						try:
							p.kill()
						except psutil.NoSuchProcess:
							pass
					gone, alive = psutil.wait_procs(alive, timeout=timeout, callback=onTerminate)
					if alive:
						# give up
						for p in alive:
							print("process {} survived SIGKILL; giving up".format(p))

			# Kill the parent first
			proc.terminate()
			gone, alive = psutil.wait_procs([proc], timeout=timeout, callback=onTerminate)
			if alive:
				print("process {} survived SIGTERM; trying SIGKILL".format(p))
				try:
					proc.kill()
				except psutil.NoSuchProcess:
					pass
				gone, alive = psutil.wait_procs([proc],timeout=timeout,callback=onTerminate)
				if alive:
					print("process {} survived SIGKILL; giving up".format(p))
		pass

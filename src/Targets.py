import paramiko
import logging
import threading

logging.basicConfig(
	format="%(levelname)s AT %(asctime)s IN %(filename)s AT %(funcName)s Process %(processName)s with PID %(process)s: %(message)s",
	datefmt="%d/%m/%Y %I:%M:%S %p"
)

def _threadTarget(ssh,cmd,callback):
	stdin,stdout,stderr = ssh.exec_command(cmd.getCommand(),get_pty=True)
	callback(
		stdin = stdin,
		stdout = stdout,
		stderr = stderr
	)

def procTarget(IP,config):
	uname = config["uname"]
	passwd = config["passwd"]
	cmds = config["cmds"]
	cmdCallbacks = config["cmdCallbacks"]
	_parallelCmdList = []

	ssh = None

	try:
		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(IP,SSHPort,uname,passwd)

	except paramiko.ssh_exception.BadHostKeyException as e:
		logging.critical("Bad Host Key given, SSH failed at: {0}".format(IP))

	except paramiko.ssh_exception.AuthenticationException as e:
		logging.critical("SSH Authentication failed at: {0} check credentials and try again.".format(IP))

	except paramiko.ssh_exception.SSHException as e:
		logging.critical("SSH Exception at: {0} check credentials and try again.".format(IP))

	except Exception as e:
		logging.critical("Error while connecting via SSH at: {0} check credentails and try again.".format(IP))

	logging.info("SSH Succeded at: {0}".format(IP))


	for cmd,callback in zip(cmd,cmdCallbacks):
		# Check if cmd is string or Command object
		# if cmd, exec_command and call callback.
		# if Command object:
		# 	store for end of exec
		if type(cmd) == "str":
			stdin,stdout,stderr = ssh.exec_command(cmd,get_pty=True)
			callback(
				stdin = stdin,
				stdout = stdout,
				stderr = stderr
			)
		else:
			_parallelCmdList.append((cmd,callback))

	for cmd,callback in _parallelCmdList:
		# create thread
		# start thread
		# join threads

		thread = threading.Thread(
					target = _threadTarget,
					kwargs = {
						"ssh":ssh,
						"cmd":cmd,
						"callback":callback
					}
				)
		_threadList.append(thread)
		thread.start()

	for thread in _threadList:
		thread.join()

	ssh.close()

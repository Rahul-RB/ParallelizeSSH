import paramiko
import logging
import threading

logging.basicConfig(
	format="[%(levelname)s] %(asctime)s IN %(filename)s AT %(funcName)s Process %(processName)s with PID %(process)s: %(message)s",
	datefmt="%d/%m/%Y %I:%M:%S %p"
)

def _threadTarget(ssh,cmd):
	stdin,stdout,stderr = ssh.exec_command(cmd.getCommand(),get_pty=True)
	cmd.getCallBack()(
		stdin = stdin,
		stdout = stdout,
		stderr = stderr
	)

def procTarget(IP,config):
	uname = config["uname"]
	passwd = config["passwd"]
	sshPort = config["sshPort"] if "sshPort" in config else 22
	cmds = config["cmds"]
	_parallelCmdList = []
	_threadList = []


	try:
		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(IP,sshPort,uname,passwd)

	except paramiko.ssh_exception.BadHostKeyException as e:
		logging.critical("Bad Host Key given, SSH failed at: {0}".format(IP))

	except paramiko.ssh_exception.AuthenticationException as e:
		logging.critical("SSH Authentication failed at: {0} check credentials and try again.".format(IP))

	except paramiko.ssh_exception.SSHException as e:
		logging.critical("SSH Exception at: {0} check credentials and try again.".format(IP))

	except Exception as e:
		print(e)
		logging.critical("Error while connecting via SSH at: {0} check credentials and try again.".format(IP))

	else:
		logging.info("SSH Succeded at: {0}".format(IP))

		for cmd in cmds:
			# Check if cmd isThreaded
			# if yes, append it to parallelCmdList and exec later
			# if no, then exec it right away

			if cmd.isThreaded:
				_parallelCmdList.append(cmd)
			else:
				stdin,stdout,stderr = ssh.exec_command(cmd.getCommand(),get_pty=True)
				cmd.getCallBack()(
					stdin = stdin,
					stdout = stdout,
					stderr = stderr
				)

		for cmd in _parallelCmdList:
			# create thread for each command
			# start thread
			# join threads

			thread = threading.Thread(
						target = _threadTarget,
						kwargs = {
							"ssh":ssh,
							"cmd":cmd
						}
					)
			_threadList.append(thread)
			thread.start()

		for thread in _threadList:
			thread.join()

		ssh.close()

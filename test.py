import os
import threading
from ParallelizeSSH import Command
from ParallelizeSSH import SSH

def closeConns(ssh):
	ssh.close()

def lsCallback(stdin,stdout,stderr):
    for line in iter(lambda: stdout.readline(),""):
        print(line)

hosts = {
    "127.0.0.1":{
        "uname":os.getenv("PSSH_UNAME"),
        "passwd":os.getenv("PSSH_PASSWD"),
        "cmds":[
        	Command("python3 runLong.py")
        ]
    }
}

ssh = SSH(hosts)
ssh.run(waitToExit=False)
t = threading.Timer(5,closeConns,kwargs={
		"ssh":ssh
	})
t.start()

import os
import threading
from Parallelize.Parallelize import Command
from Parallelize.Parallelize import Parallelize

def closeConns(ssh):
	ssh.close()

def lsCallback(stdin,stdout,stderr):
    for line in iter(lambda: stdout.readline(),""):
        print(line)

hosts = {
    "127.0.0.1":{
        "uname":os.getenv("PSSH_UNAME"),
        "passwd":os.getenv("PSSH_PASSWD"),
        "cmds":[Command("./some-long-script.py",isThreaded=True)],
        "callbacks":[lsCallback]
    }
}

ssh = Parallelize(hosts)
ssh.run(waitToExit=False)
t = threading.Timer(5,closeConns,kwargs={
		"ssh":ssh
	})
t.start()
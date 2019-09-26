from Parallelize.Parallelize import Command
from Parallelize.Parallelize import Parallelize

def lsCallback(stdin,stdout,stderr):
    for line in iter(lambda: stdout.readline(),""):
        print(line)

hosts = {
    "192.168.247.128":{
        "uname":os.getenv("PSSH_UNAME"),
        "passwd":os.getenv("PSSH_PASSWD"),
        "cmds":[Command("ls -l",isThreaded=True)],
        "callbacks":[lsCallback]
    }
}

ssh = Parallelize(hosts)
ssh.setup()
ssh.run(waitToExit=True)


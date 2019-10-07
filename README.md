# ParallelizeSSH
Simple Parallel SSH module using Paramiko.

### Dependencies:
- Paramiko 2.6
- Python 3.6+

### Installation:
Coming soon on pip

### Get Started:

    import os
    from Parallelize.Parallelize import Command
    from Parallelize.Parallelize import Parallelize
     
    hosts = {
        "127.0.0.1":{
            "uname":os.getenv("PSSH_UNAME"),
            "passwd":os.getenv("PSSH_PASSWD"),
            "cmds":[
                Command("ls -l")
            ]
        }
    }
     
    ssh = Parallelize(hosts)
    ssh.run(waitToExit=False)
    ssh.close()

#### An example with custom callback:

    import os
    import threading
    from Parallelize.Parallelize import Command
    from Parallelize.Parallelize import Parallelize
     
    def myCallback(stdin,stdout,stderr):
        print("In My Callback")
        for line in iter(lambda: stdout.readline(),""):
            print(line)
     
    hosts = {
        "127.0.0.1":{
            "uname":os.getenv("PSSH_UNAME"),
            "passwd":os.getenv("PSSH_PASSWD"),
            "cmds":[
                Command("ls -l",callback=myCallback)
            ]
        }
    }
     
    ssh = Parallelize(hosts)
    ssh.run(waitToExit=False)
    ssh.close()

#### Using isThreaded for inifinitely running commands:

    from Parallelize.Parallelize import Command
    from Parallelize.Parallelize import Parallelize
       
    def lsCallback(stdin,stdout,stderr):
        for line in iter(lambda: stdout.readline(),""):
            print(line)
     
    hosts = {
        "192.168.247.128":{
            "uname":"rahulrb",
            "passwd":"rahulrb",
            "cmds":[Command("ls -l",isThreaded=True,callback=lsCallback)]
        }
    }
     
    ssh = Parallelize(hosts)
    ssh.run(waitToExit=False)
    ssh.close()

`cmd` should be:
- A Command object (explained below).

`Command` object accepts:
- A mandatory `string` which is the command to be executed.
- An optional `callback` which is called after command is executed. (callbacks explained below). ParallelizeSSH provides a default callback which just prints stdout.
- An optional `isThreaded` which allows commands to executed parallely in same system.

About `callback`:
- It can be a simple python function or callable classes (__call__ if needed).
- All callbacks are called with three predefined arguments: `stdin,stdout,stderr` (in no particular order)
- An example callback is shown in example above.

## Want to pass more parameters to callback?
Use the `partial` module of `functools` library to create partially binded functions. Usage can be found [here](https://docs.python.org/3.6/library/functools.html#functools.partial).

## Things to note:
- Commands are processed in the order of the list. I.e. Command at index 0 is processed first.

## Parallelize allows commands to be executed parallelly:
**Warning**: All parallelized commands are run at end. Use this option for commands which never end unless terminated by another program/user.

To do so, use the `Command` class to create your command. Then set the `isThreaded` argument to `True`. Eg:

    from Parallelize import Command
    parallelCmd1 = Command("./longRunningScript.sh",isThreaded=True)
    parallelCmd2 = Command("./anotherLongRunningScript.sh",isThreaded=True)
    
    hosts = {
      "IP":{
        ...
        cmds:[parallelCmd1,parallelCmd2]
      }
    }


# ParallelizeSSH
Simple Parallel SSH module using Paramiko.

Dependencies:
- Paramiko 2.6
- Python 3.6+

Installation:
<To be updated soon>

Usage:

    from Parallelize import Parallelize
    hosts = {
      "IP1":{
        "uname":"Username as a string",
        "passwd":"Password as a string",
        "sshPort":OPTIONAL, Port as a number, else defaults to 22,
        "cmds":[A list of commands, format and types explained below],
        "callbacks":[Callback functions for each command, explained below]
      },
      "IP2":{
        ...
      }
    }

    ssh = Parallelize(hosts)
    ssh.setup()
    ssh.run()
    ssh.close()
    
`cmd` can be:
- Either a string (str)
- Or a special Command object (explained below).

`callbacks` are callable objects:
- Either a simple function.
- Callable classes (__call__ if needed).
- All callbacks are called with three predefined arguments: `stdin,stdout,stderr` (in no particular order)
- An example callback is show in full example below.
        
## Things to note:
- Commands are processed in the order of the list. I.e. Command at index 0 is processed first.
- For each command, the corresponding callback must be provided at the same index. 
- So for some command `cmd1` at index 1 of `cmds` list, the callback for it should be at index 1 of `callbacks` list.

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

A full example usage is as below:

    from Parallelize.Parallelize import Command
    from Parallelize.Parallelize import Parallelize
    
    def dummyCB(stdin,stdout,stderr):
        pass
        
    def lsCallback(stdin,stdout,stderr):
        for line in iter(lambda: stdout.readline(),""):
            print(line)

    hosts = {
        "192.168.247.128":{
            "uname":"rahulrb",
            "passwd":"rahulrb",
            "cmds":[Command("ls -l",isThreaded=True),"ps aux"],
            "callbacks":[lsCallback,dummyCB]
        }
    }

    ssh = Parallelize(hosts)
    ssh.setup()
    ssh.run(waitToExit=True)

def defaultCB(stdin,stdout,stderr):
    for line in iter(lambda: stdout.readline(),""):
        print(line)

class Command(object):
	def __init__(self,command,isThreaded=False,callBack=defaultCB):
		self.command = command
		self.isThreaded = isThreaded
		self.callBack = callBack

	def getCommand(self):
		return self.command

	def getCallBack(self):
		return self.callBack

	def __str__(self):
		return "Command: {0} \t isThreaded:{1} \n Callback:{2}".format(self.command,self.isThreaded,callBack)
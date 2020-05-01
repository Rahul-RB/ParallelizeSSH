def defaultCB(stdin,stdout,stderr):
    for line in iter(lambda: stdout.readline(),""):
        print(line)

class Command(object):
	def __init__(self,command,isThreaded=False,callback=defaultCB):
		self.command = command
		self.isThreaded = isThreaded
		self.callback = callback

	def getCommand(self):
		return self.command

	def getCallBack(self):
		return self.callback

	def __str__(self):
		return "Command: {0} \t isThreaded:{1} \n Callback:{2}".format(self.command,self.isThreaded,callback)

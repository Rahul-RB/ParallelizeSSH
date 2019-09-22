class Command(object):
	def __init__(self,command,isThreaded,callBack=None):
		self.command = command
		self.isThreaded = True
		self.callBack = callBack

	def getCommand(self):
		return self.command

	def getCallBack(self):
		return self.callBack

	def __str__(self):
		return "Command: {0} \t isThreaded:{1} \n Callback:{2}".format(self.command,self.isThreaded,callBack)
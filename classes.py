class Resource:
	def __init__(self, name):
		self.name = name
		self.availableHours = []
		self.maxAvailableHourInProject = {}
		self.costInProject = {}
		
	def setAvailableHours(self,ah):
		self.availableHours = ah
		
	def addMaxAvailableHourInProject(self,prj,h):
		self.maxAvailableHourInProject[prj] = h
		
	def addCostInProject(self,prj,c):
		self.costInProject[prj] = c
		

class Project:
	def __init__(self, name):
		self.name = name
		self.contractMonthlyPayments = []
		
	def setContractMonthlyPayments(self,cmpay):
		self.contractMonthlyPayments = cmpay


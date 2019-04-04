from pulp import *
from classes import *

leg = Resource('Luna')
leg.setAvailableHours([120, 120, 130, 130, 90, 100, 120, 120, 125, 110, 115, 80])
leg.addMaxAvailableHourInProject('Copel',150)
leg.addCostInProject('Copel',200.0)

leg.addMaxAvailableHourInProject('Enel21',120)
leg.addCostInProject('Enel21',180.0)

lmt = Resource('Lucas')
lmt.setAvailableHours([80, 75, 90, 55, 90, 160, 115, 90, 125, 40, 130, 160])
lmt.addMaxAvailableHourInProject('Copel',160)
lmt.addCostInProject('Copel',160.0)

lmt.addMaxAvailableHourInProject('Enel21',160)
lmt.addCostInProject('Enel21',100.0)

vsz = Resource('Vitor')
vsz.setAvailableHours([90, 110, 70, 130, 90, 90, 55, 90, 160, 110, 115, 80])
vsz.addMaxAvailableHourInProject('Copel',80)
vsz.addCostInProject('Copel',300.0)

vsz.addMaxAvailableHourInProject('Enel21',80)
vsz.addCostInProject('Enel21',220.0)

copel = Project('Copel')
copel.setContractMonthlyPayments([5000 6000 8000 5000 3000 2800 1550 8000 7500 5000 10000 12000])

enel21 = Project('Enel21')
enel21.setContractMonthlyPayments([15000 8000 5000 3000 4000 8800 3500 9000 7500 12000 3000 5000])

projectList = []
projectList.append(copel)
projectList.append(enel21)

resourceList = []
resourceList.append(leg)
resourceList.append(lmt)
resourceList.append(vsz)











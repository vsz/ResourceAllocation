from pulp import *
from classes import *

leg = Resource('Luna')
leg.setAvailableHours([120, 120, 130, 130, 90, 100, 120, 120, 125, 110, 115, 80])
leg.addMaxAvailableHourInProject('Copel',150)
leg.addCostInProject('Copel',201.55)

leg.addMaxAvailableHourInProject('Enel21',120)
leg.addCostInProject('Enel21',185.23)

lmt = Resource('Lucas')
lmt.setAvailableHours([80, 75, 90, 55, 90, 160, 115, 90, 125, 40, 130, 160])
lmt.addMaxAvailableHourInProject('Copel',160)
lmt.addCostInProject('Copel',166.23)

lmt.addMaxAvailableHourInProject('Enel21',160)
lmt.addCostInProject('Enel21',125.32)

vsz = Resource('Vitor')
vsz.setAvailableHours([90, 110, 70, 130, 90, 90, 55, 90, 160, 110, 115, 80])
vsz.addMaxAvailableHourInProject('Copel',80)
vsz.addCostInProject('Copel',302.66)

vsz.addMaxAvailableHourInProject('Enel21',80)
vsz.addCostInProject('Enel21',223.45)

copel = Project('Copel')
copel.setContractMonthlyPayments([5000, 6000, 8000, 5000, 3000, 2800, 1550, 8000, 7500, 5000, 10000, 12000])

enel21 = Project('Enel21')
enel21.setContractMonthlyPayments([15000, 8000, 5000, 3000, 4000, 8800, 3500, 9000, 7500, 12000, 3000, 5000])

projectList = []
projectList.append(copel)
projectList.append(enel21)

resourceList = []
resourceList.append(leg)
resourceList.append(lmt)
resourceList.append(vsz)

n_months = 12

# Create lists and dictionaries
RESOURCES = [r.name for r in resourceList]
PROJECTS = [p.name for p in projectList]
MONTHS = list(range(1,n_months+1))

# Resource Costs/hour
COSTS = {}
for r in resourceList:
	COSTS[r.name] = r.costInProject
	
print('costs=',COSTS)

# Maximum allocation (in projects)
MAX_ALLOC_PROJ = {}
for r in resourceList:
	MAX_ALLOC_PROJ[r.name] = r.maxAvailableHourInProject
print('max allocation in each project=',MAX_ALLOC_PROJ)

# Maximum allocation (global)
MAX_ALLOC = {}
for r in resourceList:
	MAX_ALLOC[r.name] = r.availableHours

print('max allocation=',MAX_ALLOC)

# Project Monthly Payment
PROJECTS_MONTHLY_PAYMENTS = {}
for p in projectList:
	PROJECTS_MONTHLY_PAYMENTS[p.name] = p.contractMonthlyPayments

print('project monthly payments=',PROJECTS_MONTHLY_PAYMENTS)

# Create the 'prob' variable to contain the problem data
prob = LpProblem('Resource Allocation Problem', LpMinimize)

# Create variables
difference_contract_up = pulp.LpVariable.dicts('Difference Payment Up',
												((p,m) for p in PROJECTS for m in MONTHS),
												lowBound=0,
												cat='Continuous')

difference_contract_down = pulp.LpVariable.dicts('Difference Payment Down',
												((p,m) for p in PROJECTS for m in MONTHS),
												lowBound=0,
												cat='Continuous')

allocations = pulp.LpVariable.dicts('Monthly Resource Allocations',
									((r,p,m) for r in RESOURCES for p in PROJECTS for m in MONTHS),
									lowBound = 0,
									upBound = 160,
									cat = 'Integer')


# Objective Function
prob += lpSum([difference_contract_up[p,m] + difference_contract_down[p,m] for p in PROJECTS for m in MONTHS]), 'Difference between contract payment and costs'

# Constraints
# Difference between contract and costs aux vars
for m in MONTHS:
	for p in PROJECTS:
		prob += lpSum([allocations[r,p,m]*COSTS[r][p] - PROJECTS_MONTHLY_PAYMENTS[p][m-1] - difference_contract_up[p,m] + difference_contract_down[p,m] for r in RESOURCES]) == 0

# Maximum allocation (global) each month
for m in MONTHS:
	prob += lpSum([allocations[r,p,m] - MAX_ALLOC[r][m-1] for r in RESOURCES for p in PROJECTS]) <= 0

# Maximum allocation (in individual projects) each month
for m in MONTHS:
	for p in PROJECTS:
		for r in RESOURCES:
			prob += allocations[r,p,m] - MAX_ALLOC_PROJ[r][p] <= 0


prob.writeLP('ra.lp')
prob.solve(GLPK(options=['--mipgap', '1.0']))

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print("Total difference contract/allocation cost = ", value(prob.objective))


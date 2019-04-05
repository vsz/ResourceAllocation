from pulp import *
from classes import *

"""
# Creates a list of the Ingredients
Ingredients = ['CHICKEN', 'BEEF', 'MUTTON', 'RICE', 'WHEAT', 'GEL']

# A dictionary of the costs of each of the Ingredients is created
costs = {'CHICKEN': 0.013, 
         'BEEF': 0.008, 
         'MUTTON': 0.010, 
         'RICE': 0.002, 
         'WHEAT': 0.005, 
         'GEL': 0.001}

# A dictionary of the protein percent in each of the Ingredients is created
proteinPercent = {'CHICKEN': 0.100, 
                  'BEEF': 0.200, 
                  'MUTTON': 0.150, 
                  'RICE': 0.000, 
                  'WHEAT': 0.040, 
                  'GEL': 0.000}

# A dictionary of the fat percent in each of the Ingredients is created
fatPercent = {'CHICKEN': 0.080, 
              'BEEF': 0.100, 
              'MUTTON': 0.110, 
              'RICE': 0.010, 
              'WHEAT': 0.010, 
              'GEL': 0.000}

# A dictionary of the fibre percent in each of the Ingredients is created
fibrePercent = {'CHICKEN': 0.001, 
                'BEEF': 0.005, 
                'MUTTON': 0.003, 
                'RICE': 0.100, 
                'WHEAT': 0.150, 
                'GEL': 0.000}

# A dictionary of the salt percent in each of the Ingredients is created
saltPercent = {'CHICKEN': 0.002, 
               'BEEF': 0.005, 
               'MUTTON': 0.007, 
               'RICE': 0.002, 
               'WHEAT': 0.008, 
               'GEL': 0.000}
               
# Create the 'prob' variable to contain the problem data
prob = LpProblem("The Whiskas Problem", LpMinimize)

# A dictionary called 'ingredient_vars' is created to contain the referenced Variables
ingredient_vars = LpVariable.dicts("Ingr",Ingredients,0)

# The objective function is added to 'prob' first
prob += lpSum([costs[i]*ingredient_vars[i] for i in Ingredients]), "Total Cost of Ingredients per can"

# The five constraints are added to 'prob'
prob += lpSum([ingredient_vars[i] for i in Ingredients]) == 100, "PercentagesSum"
prob += lpSum([proteinPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 8.0, "ProteinRequirement"
prob += lpSum([fatPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 6.0, "FatRequirement"
prob += lpSum([fibrePercent[i] * ingredient_vars[i] for i in Ingredients]) <= 2.0, "FibreRequirement"
prob += lpSum([saltPercent[i] * ingredient_vars[i] for i in Ingredients]) <= 0.4, "SaltRequirement"


prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print("Total Cost of Ingredients per can = ", value(prob.objective))
"""

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

allocations = pulp.LpVariable.dicts('Monthly Rsource Allocations',
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
		prob += lpSum([allocations[r,p,m]*COSTS[r][p] - difference_contract_up[p,m] - PROJECTS_MONTHLY_PAYMENTS[p][m-1] for r in RESOURCES]) <= 0
		prob += lpSum([allocations[r,p,m]*COSTS[r][p] + difference_contract_down[p,m] - PROJECTS_MONTHLY_PAYMENTS[p][m-1] for r in RESOURCES]) >= 0

# Maximum allocation (global) each month
for m in MONTHS:
	prob += lpSum([allocations[r,p,m] - MAX_ALLOC[r][m-1] for r in RESOURCES for p in PROJECTS]) <= 0

# Maximum allocation (in individual projects) each month
for m in MONTHS:
	for p in PROJECTS:
		for r in RESOURCES:
			prob += allocations[r,p,m] - MAX_ALLOC_PROJ[r][p] <= 0



prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print("Total difference contract/allocation cost = ", value(prob.objective))


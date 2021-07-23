'''
Created on 20th July 2021

Energy Planning Scenario in Pyomo

This script presents the mathematical formulation for an energy planning 
scenario in a specific geographical region or district. Renewable energy 
sources and fossil-based source such as coal, oil and natural gas, 
each with its respectively energy contribution and carbon intensity make up 
the power generation in a specific region or district. Each period consists 
of its respective energy demand and carbon emission limit. 
NETs are utilised to achieve the emission limit.

@author: Purusothmn, Dr Michael Short

'''
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import pandas as pd
import matplotlib.pyplot as plt
import os
from openpyxl import load_workbook

path = os.chdir(r'C:/Users/LENOVO/OneDrive - University of Nottingham Malaysia/The University of Nottingham/BC COP26 Trilateral Research Initiative/BCCOP26TrilateralProject') 

cwd = os.getcwd()

file = r'Energy_Planning_User_Interface.xlsx'
plant_data = pd.read_excel(file, sheet_name = 'PLANT_DATA', index_col = 0, header = 26).to_dict()
EP_data = pd.read_excel(file, sheet_name = 'EP_DATA', header = 20)

s = plant_data.keys()

wb = load_workbook(file)
sheet = wb['PLANT_DATA']
energy_unit = sheet['B21'].value
CI_unit = sheet['B22'].value
carbon_load_unit = sheet['B23'].value
cost_unit = sheet['B24'].value

#Period number
prd = list(EP_data['Period'])

#Energy demand for each period
Demand = list(EP_data['Energy Demand'])

#Emission limit for each period
Limit = list(EP_data['Emission Limit'])

#Carbon intensity of first choice of EP-NET for each period
EP_NET_1_CI = list(EP_data['CI EP-NET(1)'])

#Carbon intensity of second choice of EP-NET for each period
EP_NET_2_CI = list(EP_data['CI EP-NET(2)'])

#Carbon intensity of third choice of EP-NET for each period
EP_NET_3_CI = list(EP_data['CI EP-NET(3)'])

#Cost of first choice of EP-NET for each period
Cost_EP_NET_1 = list(EP_data['Cost EP-NET(1)'])

#Cost of second choice of EP-NET for each period
Cost_EP_NET_2 = list(EP_data['Cost EP-NET(2)'])

#Cost of third choice of EP-NET for each period
Cost_EP_NET_3 = list(EP_data['Cost EP-NET(3)'])

#Carbon intensity of first choice of EC-NET for each period
EC_NET_1_CI = list(EP_data['CI EC-NET(1)'])

#Carbon intensity of second choice of EC-NET for each period
EC_NET_2_CI = list(EP_data['CI EC-NET(2)'])

#Carbon intensity of third choice of EC-NET for each period
EC_NET_3_CI = list(EP_data['CI EC-NET(3)'])

#Cost of first choice EC-NET for each period
Cost_EC_NET_1 = list(EP_data['Cost EC-NET(1)'])

#Cost of second choice EC-NET for each period
Cost_EC_NET_2 = list(EP_data['Cost EC-NET(2)'])

#Cost of third choice EC-NET for each period
Cost_EC_NET_3 = list(EP_data['Cost EC-NET(3)'])

#Carbon intensity of compensatory energy for each period
Comp_CI = list(EP_data['CI Compensatory'])

#Cost of compensatory energy for each period
Cost_Comp = list(EP_data['Cost Compensatory'])

numperiods = len(prd) + 1
period_data_dict = {}

for (i,D,L,EP1I,EP2I,EP3I,CEP1,CEP2,CEP3,EC1I,EC2I,EC3I,CEC1,CEC2,CEC3,CI,CC) in zip(prd, Demand, Limit, EP_NET_1_CI, EP_NET_2_CI, EP_NET_3_CI, Cost_EP_NET_1, Cost_EP_NET_2, Cost_EP_NET_2, EC_NET_1_CI, EC_NET_2_CI, EC_NET_3_CI, Cost_EC_NET_1, Cost_EC_NET_2, Cost_EC_NET_2, Comp_CI, Cost_Comp):    
    period_data_dict[i]= {'Demand' : D, 
                          'Emission_Limit' : L,
                          'EP_NET_1_CI' : EP1I,
                          'EP_NET_2_CI' : EP2I,
                          'EP_NET_3_CI' : EP3I,
                          'Cost_EP_NET_1' : CEP1,
                          'Cost_EP_NET_2' : CEP2,
                          'Cost_EP_NET_3' : CEP3,
                          'EC_NET_1_CI' : EC1I,
                          'EC_NET_2_CI' : EC2I,
                          'EC_NET_3_CI' : EC3I,
                          'Cost_EC_NET_1' : CEC1,
                          'Cost_EC_NET_2' : CEC2,
                          'Cost_EC_NET_3' : CEC3,
                          'Comp_CI' : CI,
                          'Cost_Comp' : CC}
    
def EP_Period(plant_data,period_data): 
    model = pyo.ConcreteModel()
    model.S = plant_data.keys()
    model.plant_data = plant_data
    model.period_data = period_data
       
    #LIST OF VARIABLES
    
    #This variable determines the deployment of energy sources in power plant s
    model.energy = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the carbon intensity of power plant s with CCS deployment for each period
    model.CI_RET = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #Binary variable for CCS deployment in power plant s for each period
    model.B = pyo.Var(model.S, domain = pyo.Binary)
    
    #This variable represents the extent of CCS retrofit in power plant s for each period
    model.CCS = pyo.Var(model.S, domain = pyo.NonNegativeReals) 
    
    #This variable determines the net energy available from power plant s without CCS deployment for each period
    model.net_energy = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the net energy available from power plant s with CCS deployment for each period
    model.net_energy_CCS = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of the first choice of EP_NETs for each period 
    model.EP_NET_1 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of the second choice of EP_NETs for each period 
    model.EP_NET_2 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of the third choice of EP_NETs for each period 
    model.EP_NET_3 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of the first choice of EC_NETs for each period 
    model.EC_NET_1 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of the second choice of EC_NETs for each period 
    model.EC_NET_2 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of the third choice of EC_NETs for each period 
    model.EC_NET_3 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of renewable compensatory energy for each period
    model.comp = pyo.Var(domain = pyo.NonNegativeReals)

    #This variable determines the final total CO2 emission after energy planning for each period
    model.new_emission = pyo.Var(domain = pyo.NonNegativeReals)

    #This variable determines the total energy cost for each period
    model.sum_cost = pyo.Var(domain = pyo.NonNegativeReals)    
          
    #OBJECTIVE FUNCTION
    
    #The objective function minimises the cumulative extent of CCS retrofit, thus minimising the NET requirement
    model.obj = pyo.Objective(expr = model.sum_cost, sense = pyo.minimize)
   
    #CONSTRAINTS
    
    model.cons = pyo.ConstraintList()

    model.cons.add(sum(model.energy[s] for s in model.S) == model.period_data['Demand'])
    
    for s in model.S:
        #Calculation of carbon intensity for CCS retrofitted fossil-based sources
        model.cons.add((model.plant_data[s]['CI'] * (1 - model.plant_data[s]['RR']) / (1 - model.plant_data[s]['X'])) == model.CI_RET[s])
        
        #The deployment of energy source in power plant s should at least satisfy the lower bound
        model.cons.add(model.energy[s] >= model.plant_data[s]['LB'])
        
        #The deployment of energy source in power plant s should at most satisfy the upper bound
        model.cons.add(model.energy[s] <= model.plant_data[s]['UB'])
    
        #The extent of CCS retrofit on fossil-based sources should never exceed the available energy
        model.cons.add(model.CCS[s] <= model.energy[s])
        
        #Determine the net energy available from fossil-based sources with CCS retrofit
        model.cons.add(model.CCS[s] * (1 - model.plant_data[s]['X']) * model.B[s] == model.net_energy_CCS[s])
        
        #The summation of energy contribution from each source with and without CCS retrofit must equal to individual energy contribution
        model.cons.add(model.net_energy[s] + (model.CCS[s] * model.B[s]) == model.energy[s]) 
    
        if 'REN' in model.plant_data[s].values():
            model.CCS[s].fix(0)
   
    #Total energy contribution from all energy sources to satisfy the total demand
    model.cons.add(sum(((model.net_energy[s]) + (model.net_energy_CCS[s] * model.B[s])) for s in model.S) + model.comp + model.EP_NET_1 + model.EP_NET_2 + model.EP_NET_3 == model.period_data['Demand'] + model.EC_NET_1 + model.EC_NET_2 + model.EC_NET_3) 
    
    #The total CO2 load contribution from all energy sources must satisfy most the CO2 emission limit after energy planning 
    model.cons.add(sum((model.net_energy[s] * model.plant_data[s]['CI']) + (model.net_energy_CCS[s] * model.CI_RET[s]) for s in model.S)
               + (model.EC_NET_1 * model.period_data['EC_NET_1_CI'])
               + (model.EC_NET_2 * model.period_data['EC_NET_2_CI'])
               + (model.EC_NET_3 * model.period_data['EC_NET_3_CI'])
               + (model.EP_NET_1 * model.period_data['EP_NET_1_CI'])
               + (model.EP_NET_2 * model.period_data['EP_NET_2_CI'])
               + (model.EP_NET_3 * model.period_data['EP_NET_3_CI'])
               + (model.comp * model.period_data['Comp_CI']) == model.new_emission)

    #The summation of cost for each power plant s should equal to the total cost of each period
    model.cons.add(sum((model.net_energy[s] * model.plant_data[s]['Cost']) + (model.net_energy_CCS[s] * model.plant_data[s]['Cost_CCS'] * model.B[s]) for s in model.S)
               + (model.EC_NET_1 * model.period_data['Cost_EC_NET_1'])
               + (model.EC_NET_2 * model.period_data['Cost_EC_NET_2'])
               + (model.EC_NET_3 * model.period_data['Cost_EC_NET_3'])
               + (model.EP_NET_1 * model.period_data['Cost_EP_NET_1'])
               + (model.EP_NET_2 * model.period_data['Cost_EP_NET_2'])
               + (model.EP_NET_3 * model.period_data['Cost_EP_NET_3'])
               + (model.comp * model.period_data['Cost_Comp']) == model.sum_cost) 
    
    #Total CO2 load contribution from all energy sources to satisfy the emission limit
    model.cons.add(model.new_emission == model.period_data['Emission_Limit'])  
        
    return model

#Creating a list with 3 strings
block_sets = list(range(1, numperiods, 1))

#Adding the models to a dictionary to be accessed inside the function
EP = dict()
for i in range(1, numperiods, 1):
    EP[block_sets[i-1]] = EP_Period(plant_data, period_data_dict[i])

Full_model = pyo.ConcreteModel()

'''
This function defines each block - the block is model m containing all equations and variables
It needs to be put in the right set (block_sets) with objective function turned off
'''
def build_individual_blocks(model, block_sets):
    model = EP[block_sets]
    model.obj.deactivate()
    model.del_component(model.obj)
    return model

#Defining the pyomo block structure with the set block sets and rule to build the blocks
Full_model.subprobs = pyo.Block(block_sets, rule = build_individual_blocks)

'''
The blocks are linked such that the extent of CCS retrofit on source i at period t + 1
should at least match the extent of CCS retrofit on source i at period t
'''

def linking_blocks(model, block_sets, s):
    if block_sets == len(prd):
        return pyo.Constraint.Skip
    else:   
        return Full_model.subprobs[block_sets + 1].CCS[s] >=  Full_model.subprobs[block_sets].CCS[s]
        
Full_model.Cons1 = pyo.Constraint(block_sets, s, rule = linking_blocks)

'''
Creating a new objective function for the new model
The objective minimises the cumulative extent of CCS retrofit from all fossil-based sources
'''
TCOST = 0
for i in range(1, numperiods, 1):
    TCOST = TCOST + Full_model.subprobs[i].sum_cost
    
Full_model.obj = pyo.Objective(expr = TCOST, sense = pyo.minimize)

#Using octeract engine solver to solve the energy planning model
opt = SolverFactory('octeract-engine')
results = opt.solve(Full_model)
print(results)
'''
Creating a fuction to publish the results energy planning scenario for a single period

Args:
    source_data = The energy and carbon intensity for [Period Number] 
    period_data = The energy planning data for [Period Number]
    period = Time period involved ('P1' or 'P2' or 'P3')
    
returns:
    the results from variables in the energy planning model, 
    a data table with the energy and emission contribution from each energy source,
    and energy planning pinch diagram
'''

def EP_Results(plant_data, period_data, period):
    model = Full_model.subprobs[period]
    print(' ')
    print('Time period', '= Period' , period)
    print(' ')
    print('CO2 load limit in Period', period, '=', model.period_data['Emission_Limit'], carbon_load_unit)
    print(' ')
    print('Revised total CO2 Emission after energy planning in Period', period, '=', round(model.new_emission(), 2), carbon_load_unit)    
    print(' ')
    print('Minimum first choice of EP_NET Deployment in Period', period, '=', round(model.EP_NET_1(), 2), energy_unit)
    print(' ')
    print('Minimum second choice of EP_NET Deployment in Period', period, '=', round(model.EP_NET_2(), 2), energy_unit)
    print(' ') 
    print('Minimum third choice of EP_NET Deployment in Period', period, '=', round(model.EP_NET_3(), 2), energy_unit)
    print(' ') 
    print('Minimum first choice of EC_NET Deployment in Period', period, '=', round(model.EC_NET_1(), 2), energy_unit)
    print(' ')
    print('Minimum second choice of EC_NET Deployment in Period', period, '=', round(model.EC_NET_2(), 2), energy_unit)
    print(' ')
    print('Minimum third choice of EC_NET Deployment in Period', period, '=', round(model.EC_NET_3(), 2), energy_unit)
    print(' ')
    print('Minimum compensatory energy deployment in Period', period, '=', round(model.comp(), 2), energy_unit)
    print(' ')
    print('Total energy cost in Period', period, '=', round(model.sum_cost(), 2), cost_unit)
    print(' ')
    
    print('Energy deployment in power plant s in Period', period)
    print(' ')    
    for s in plant_data.keys():    
        print(s, '=', round(model.energy[s](), 2), energy_unit)
    print(' ')
    
    print('Selection of power plant s for CCS retrofit in Period', period)
    print(' ')    
    for s in plant_data.keys():    
        print(s, '=', model.B[s]())
    print(' ')
    
    print('Carbon Intensity of CCS Retrofitted energy sources for power plant s in Period', period)
    print(' ')    
    for s in plant_data.keys():    
        print(s, '=', round(model.CI_RET[s](), 3), CI_unit)
    print(' ')
    
    print('Extent of CCS retrofit on energy sources for power plant s in Period', period)
    print(' ')    
    for s in plant_data.keys():    
        print(s, '=', round(model.CCS[s](), 2), energy_unit)
    print(' ')
    
    print('Net energy from energy sources without CCS retrofit for power plant s in Period', period)
    print(' ')    
    for s in plant_data.keys():
        print(s, '=', round(model.net_energy[s](), 2), energy_unit)
    print(' ')    
    
    print('Net energy from energy sources with CCS retrofit for power plant s in Period', period)
    print(' ')    
    for s in plant_data.keys():
        print(s, '=', round(model.net_energy_CCS[s](), 2), energy_unit)
    print(' ')     
    
    energy_planning = pd.DataFrame()

    for s in plant_data.keys():
        energy_planning.loc['INITIAL', 'Fuel'] = 'N/A'
        energy_planning.loc['EP_NET_1', 'Fuel'] = 'EP_NET_1'
        energy_planning.loc['EP_NET_2', 'Fuel'] = 'EP_NET_2'
        energy_planning.loc['EP_NET_3', 'Fuel'] = 'EP_NET_3'
        energy_planning.loc['EC_NET_1', 'Fuel'] = 'EC_NET_1'
        energy_planning.loc['EC_NET_2', 'Fuel'] = 'EC_NET_2' 
        energy_planning.loc['EC_NET_3', 'Fuel'] = 'EC_NET_3'         
        energy_planning.loc['COMP', 'Fuel'] = 'COMP'        
        energy_planning.loc[s, 'Fuel'] = plant_data[s]['Fuel']
        energy_planning.loc[s, 'Energy'] = round(model.energy[s](), 2)       
        energy_planning.loc[s, 'CCS Ret'] = round(model.CCS[s](), 2)        
        energy_planning.loc[s, 'Net Energy wo CCS'] = round(model.net_energy[s](), 2)
        energy_planning.loc[s, 'Net Energy w CCS'] = round(model.net_energy_CCS[s](), 2)
        energy_planning.loc[s, 'Net Energy'] = round(model.net_energy[s]() + model.net_energy_CCS[s](), 2)
        energy_planning.loc['EP_NET_1', 'Net Energy'] = round(model.EP_NET_1(), 2)
        energy_planning.loc['EP_NET_2', 'Net Energy'] = round(model.EP_NET_2(), 2)
        energy_planning.loc['EP_NET_3', 'Net Energy'] = round(model.EP_NET_3(), 2)
        energy_planning.loc['EC_NET_1', 'Net Energy'] = round(model.EC_NET_1(), 2)
        energy_planning.loc['EC_NET_2', 'Net Energy'] = round(model.EC_NET_2(), 2)
        energy_planning.loc['EC_NET_3', 'Net Energy'] = round(model.EC_NET_3(), 2)
        energy_planning.loc['COMP', 'Net Energy'] = round(model.comp(),2)     
        energy_planning.loc['INITIAL', 'Net Energy'] = 0
        energy_planning.loc[s, 'Carbon Load'] = round((model.net_energy[s]() * plant_data[s]['CI']) + (model.net_energy_CCS[s]() * model.CI_RET[s]()), 2)
        energy_planning.loc['EP_NET_1', 'Carbon Load'] = round(model.EP_NET_1() * model.period_data['EP_NET_1_CI'], 2)
        energy_planning.loc['EP_NET_2', 'Carbon Load'] = round(model.EP_NET_2() * model.period_data['EP_NET_2_CI'], 2)
        energy_planning.loc['EP_NET_3', 'Carbon Load'] = round(model.EP_NET_3() * model.period_data['EP_NET_3_CI'], 2)
        energy_planning.loc['EC_NET_1', 'Carbon Load'] = round(model.EC_NET_1() * model.period_data['EC_NET_1_CI'], 2)
        energy_planning.loc['EC_NET_2', 'Carbon Load'] = round(model.EC_NET_2() * model.period_data['EC_NET_2_CI'], 2)
        energy_planning.loc['EC_NET_3', 'Carbon Load'] = round(model.EC_NET_3() * model.period_data['EC_NET_3_CI'], 2)
        energy_planning.loc['COMP', 'Carbon Load'] = round(model.comp() * model.period_data['Comp_CI'], 2)
        energy_planning.loc['INITIAL', 'Carbon Load'] = 0
    
    print('Energy Planning Table for Period', period)
    print(' ')
    print(energy_planning)
    print(' ')
    '''
    x = pd.Series(energy_planning['Net Energy'])
    xsum = x.cumsum()
    
    y = pd.Series(energy_planning['Carbon Load'])
    ysum = y.cumsum()
        
    x_coor = [-5, 90]
    y_coor = [0, 0]
    plt.plot(x_coor, y_coor, 'k', lw = 3)
    #Creating a horizontal line at the origin
    
    if period == 1:
        plt.plot(xsum, ysum, 'r', lw=3, label = period)
    elif period == 2:
        plt.plot(xsum, ysum, 'g', lw=3, label = period)
    else:
        plt.plot(xsum, ysum, 'm', lw=3, label = period)            
    
        
    plt.xlabel('Energy / TWh/y')
    plt.ylabel('CO2 Load / Mt/y')
    plt.grid(True)
    plt.title('Energy Planning Scenarios')
    plt.legend()   
    '''
    return    

for i in range (1, numperiods,1):
    EP_Results(plant_data, period_data_dict[i], i)

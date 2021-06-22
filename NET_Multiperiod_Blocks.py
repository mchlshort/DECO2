'''
Created on 3rd June 2021

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

'''
source_period_[Period Number] represents the energy data for [Period Number]
'''
source_period_1 = {
    'Plant_1'  : {'Energy': 18.0,
                    'CI' : 0},                    
    'Plant_2'  : {'Energy' : 5.0,
                    'CI' : 0.5},                    
    'Plant_3'  : {'Energy' : 7.0,
                    'CI' : 0.5},                   
    'Plant_4'  : {'Energy' : 7.2,
                    'CI' : 0.5},                    
    'Plant_5'  : {'Energy' : 6.0,
                    'CI' : 0.8},                   
    'Plant_6'  : {'Energy' : 8.0,
                    'CI' : 1},                   
    'Plant_7'  : {'Energy' : 5.0,
                    'CI' : 1},                    
    'Plant_8'  : {'Energy' : 3.8,
                    'CI' : 1}                    
    }

source_period_2 = {
     'Plant_1' : {'Energy' : 30.0,
                    'CI' : 0},                  
    'Plant_2'  : {'Energy' : 8.0,
                    'CI' : 0.5},                   
    'Plant_3'  : {'Energy' : 10.0,
                    'CI' : 0.5},                   
    'Plant_4'  : {'Energy' : 12.0,
                    'CI' : 0.5},                   
    'Plant_5'  : {'Energy' : 5.0,
                    'CI' : 0.8},                    
    'Plant_6'  : {'Energy' : 5.0,
                    'CI' : 1},                    
    'Plant_7'  : {'Energy' : 5.0,
                    'CI' : 1},
    'Plant_8'  : {'Energy' : 0.0,
                    'CI' : 1} 
    }

source_period_3 = {
    'Plant_1'  : {'Energy' : 40.0,
                    'CI' : 0},                    
    'Plant_2'  : {'Energy' : 10.0,
                    'CI' : 0.5},                    
    'Plant_3'  : {'Energy' : 15.0,
                    'CI' : 0.5},                    
    'Plant_4'  : {'Energy' : 15.0,
                    'CI' : 0.5},                    
    'Plant_5'  : {'Energy' : 5.0,
                    'CI' : 0.8},                    
    'Plant_6'  : {'Energy' : 5.0,
                    'CI' : 1},
    'Plant_7'  : {'Energy' : 0.0,
                    'CI' : 1},
    'Plant_8'  : {'Energy' : 0.0,
                    'CI' : 1} 
    }

'''
data_period_[Period Number] represents the period data for [Period Number]
i.e. total demand, emission limit, CCS data
'''
data_period_1 = {
        'Constraints' : {'Demand' : 60,
                         'Emission_Red' : 0.8,
                         'NET_CI' : -0.6,
                         'RR': 0.85,
                         'X': 0.15}      
    }

data_period_2 = {
        'Constraints' : {'Demand' : 75,
                         'Emission_Red' : 0.6,
                         'NET_CI' : -0.6,
                         'RR': 0.85,
                         'X': 0.15}      
    }

data_period_3 = {
        'Constraints' : {'Demand' : 90,
                         'Emission_Red' : 0.4,
                         'NET_CI' : -0.6,
                         'RR': 0.85,
                         'X': 0.15}      
    }

s = source_period_1.keys()

'''
Creating a fuction to define the energy planning model

Args:
    source_data = The energy and carbon intensity for [Period Number] 
    period_data = The energy planning data for [Period Number]
    
returns:
    the energy planning model with all variables, constraints and objective function
'''
def EP_Period(source_data,period_data): 
    model = pyo.ConcreteModel()
    model.S = source_data.keys()
    model.source_data = source_data
    model.period_data = period_data
   
    #LIST OF VARIABLES
    
    #Binary variable for selection of plant s for CCS
    model.B = pyo.Var(model.S, domain = pyo.Binary)
    
    #This variable determines the total CO2 emission contribution from all energy sources
    model.emission = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable determines the CO2 emission limit for a specified period
    model.limit = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable determines the revised total CO2 emission after energy planning
    model.new_emission = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the extent of CCS retrofit for each fossil-based source
    model.CCS = pyo.Var(model.S, domain = pyo.NonNegativeReals)   
    
    #This variable represents the minimum deployment of NET 
    model.NET = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable determines the net energy available from each fossil-based source without CCS deployment
    model.net_energy = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the net energy available from each fossil-based source with CCS deployment
    model.net_energy_CCS = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the carbon intensity of each fossil-based source with CCS deployment
    model.CI_RET = pyo.Var(model.S, domain = pyo.NonNegativeReals)
       
   
    #OBJECTIVE FUNCTION
    
    #The objective function minimises the cumulative extent of CCS retrofit, thus minimising the NET requirement
    model.obj = pyo.Objective(expr = model.NET, sense = pyo.minimize)
   
    #CONSTRAINTS

    model.cons = pyo.ConstraintList()
    
    #Determining the cumulative CO2 emission from all energy sources
    model.cons.add(model.emission == sum((model.source_data[s]['Energy'] * model.source_data[s]['CI']) for s in model.S))
    
    #Determining the CO2 emission limit during a specified time period
    model.cons.add(model.limit == model.period_data['Constraints']['Emission_Red'] * model.emission)
    
    for s in model.S:
        #Calculation of carbon intensity for CCS retrofitted fossil-based sources
        model.cons.add((model.source_data[s]['CI'] * (1 - model.period_data['Constraints']['RR']) / (1 - model.period_data['Constraints']['X'])) == model.CI_RET[s])
    
        #The extent of CCS retrofit on fossil-based sources should never exceed the available energy
        model.cons.add(model.CCS[s] <= model.source_data[s]['Energy'])
        
        #Determine the net energy available from fossil-based sources with CCS retrofit
        model.cons.add(model.CCS[s] * (1 - model.period_data['Constraints']['X']) * model.B[s] == model.net_energy_CCS[s])
        
        #The summation of energy contribution from each source with and without CCS retrofit must equal to individual energy contribution
        model.cons.add(model.net_energy[s] + model.CCS[s] == model.source_data[s]['Energy'])   
                       
    #Total energy contribution from all energy sources to satisfy the total demand
    model.cons.add(sum(((model.net_energy[s]*(1 - model.B[s])) + (model.net_energy_CCS[s] * model.B[s])) for s in model.S) + model.NET == model.period_data['Constraints']['Demand'])
    
    #The total CO2 load contribution from all energy sources is equivalent to the revised total CO2 emission after energy planning 
    model.cons.add(sum((model.net_energy[s] * model.source_data[s]['CI']) + (model.net_energy_CCS[s] * model.CI_RET[s]) for s in model.S)
               + (model.NET * model.period_data['Constraints']['NET_CI']) == model.new_emission)     
    
    #Total CO2 load contribution from all energy sources to satisfy the emission limit
    model.cons.add(model.new_emission <= model.limit)  
        
    #No CCS retrofit would be done on renewable energy power plants
    model.CCS['Plant_1'].fix(0)
    
    return model

#Specifying the data for each model as an argument
model_1 = EP_Period(source_period_1, data_period_1)
model_2 = EP_Period(source_period_2, data_period_2)
model_3 = EP_Period(source_period_3, data_period_3)

#Creating a list with 3 strings
#block_sets = ['P1', 'P2', 'P3']
block_sets = [1, 2, 3]

#Adding the models to a dictionary to be accessed inside the function
EP = dict()
EP[block_sets[0]] = model_1
EP[block_sets[1]] = model_2
EP[block_sets[2]] = model_3

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
Creating a new objective function for the new model
The objective minimises the cumulative extent of CCS retrofit from all fossil-based sources
'''

def linking_blocks(model, block_sets, s):
    if block_sets == 3:
        return pyo.Constraint.Skip
    else:   
        return Full_model.subprobs[block_sets + 1].CCS[s] >=  Full_model.subprobs[block_sets].CCS[s]
        
Full_model.Cons1 = pyo.Constraint(block_sets, s, rule = linking_blocks)

Full_model.obj = pyo.Objective(expr = Full_model.subprobs[1].NET +
                               Full_model.subprobs[2].NET +
                               Full_model.subprobs[3].NET, 
                               sense = pyo.minimize)
                              

#Using ipopt solver to solve the energy planning model
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

def EP_Results(source_data, period_data, period):
    model = Full_model.subprobs[period]
    print(' ')
    print('Time period', '=' , period)
    print(' ')
    print('Total CO2 load in', period, '=', model.emission())
    print('CO2 load limit in', period, '=', round(model.limit(), 2))
    print(' ')
    
    print('Selection of plant s for CCS retrofit in', period)
    print(' ')    
    for s in source_data.keys():    
        print(s, '=', model.B[s]())
    print(' ')
    
    print('Carbon Intensity of CCS Retrofitted sources i in', period)
    print(' ')    
    for s in source_data.keys():    
        print(s, '=', round(model.CI_RET[s](), 3), 'TWh/y')
    print(' ')
    
    print('Extent of CCS retrofit on source i in', period)
    print(' ')    
    for s in source_data.keys():    
        print(s, '=', round(model.CCS[s](), 2), 'TWh/y')
    print(' ')
    
    print('Net energy from source i without CCS retrofit in', period)
    print(' ')    
    for s in source_data.keys():
        print(s, '=', round(model.net_energy[s](), 2), 'TWh/y')
    print(' ')    
    
    print('Net energy from source i with CCS retrofit in', period)
    print(' ')    
    for s in source_data.keys():
        print(s, '=', round(model.net_energy_CCS[s](), 2), 'TWh/y')
    print(' ')  
    
    print('Minimum NET Deployment in', period, '=', round(model.NET(), 2), 'TWh/y')
    print(' ') 
    
    energy_planning = pd.DataFrame()

    for s in source_data.keys():
        energy_planning.loc[s, 'Energy'] = source_data[s]['Energy']       
        energy_planning.loc[s, 'CCS Ret'] = round(model.CCS[s](), 2)        
        energy_planning.loc[s, 'Net Energy wo CCS'] = round(model.net_energy[s](), 2)
        energy_planning.loc[s, 'Net Energy w CCS'] = round(model.net_energy_CCS[s](), 2)
        energy_planning.loc[s, 'Net Energy'] = round(model.net_energy[s]() + model.net_energy_CCS[s](), 2)
        energy_planning.loc['NET', 'Net Energy'] = round(model.NET(),2)
        energy_planning.loc[s, 'Carbon Load'] = round((model.net_energy[s]() * source_data[s]['CI']) + (model.net_energy_CCS[s]() * model.CI_RET[s]()), 2)
        energy_planning.loc['NET', 'Carbon Load'] = round(model.NET() * period_data['Constraints']['NET_CI'], 2)
    
    print('Energy Planning Table for', period)
    print(' ')
    print(energy_planning)
    print(' ')
    
    print('Revised total CO2 Emission after energy planning in', period, round(model.new_emission(), 2))
    
    return    

EP_Results(source_period_1, data_period_1, 1)
EP_Results(source_period_2, data_period_2, 2)
EP_Results(source_period_3, data_period_3, 3)

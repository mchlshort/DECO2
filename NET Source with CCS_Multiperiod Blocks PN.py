import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import pandas as pd
import matplotlib.pyplot as plt

source_period_1 = {
    'Renewables'  : {'Energy' : 18.0,
                    'CI' : 0},
    'Natural Gas' : {'Energy' : 19.2,
                    'CI' : 0.5},
    'Oil'         : {'Energy' : 6,
                    'CI' : 0.8},
    'Coal'        : {'Energy' : 16.8,
                    'CI' : 1}    
    }

source_period_2 = {
    'Renewables'  : {'Energy' : 30.0,
                    'CI' : 0},
    'Natural Gas' : {'Energy' : 30.0,
                    'CI' : 0.5},
    'Oil'         : {'Energy' : 5,
                    'CI' : 0.8},
    'Coal'        : {'Energy' : 10.0,
                    'CI' : 1}    
    }

source_period_3 = {
    'Renewables'  : {'Energy' : 40.0,
                    'CI' : 0},
    'Natural Gas' : {'Energy' : 40.0,
                    'CI' : 0.5},
    'Oil'         : {'Energy' : 5,
                    'CI' : 0.8},
    'Coal'        : {'Energy' : 5.0,
                    'CI' : 1}    
    }

data_period_1 = {
        'Constraints' : {'Demand' : 60,
                         'Emission_limit' : 15,
                         'NET_CI' : -0.6,
                         'RR': 0.85,
                         'X': 0.15}      
    }

data_period_2 = {
        'Constraints' : {'Demand' : 75,
                         'Emission_limit' : 12,
                         'NET_CI' : -0.6,
                         'RR': 0.85,
                         'X': 0.15}      
    }

data_period_3 = {
        'Constraints' : {'Demand' : 90,
                         'Emission_limit' : 9,
                         'NET_CI' : -0.6,
                         'RR': 0.85,
                         'X': 0.15}      
    }

def EP_Period(source_data,period_data):
    S = source_data.keys()
    model = pyo.ConcreteModel()
   
    #LIST OF VARIABLES
    
     #This variable represents the extent of CCS retrofit for each fossil-based source
    model.CCS = pyo.Var(S, domain = pyo.NonNegativeReals)   
    
    #This variable represents the minimum deployment of NET 
    model.NET = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable determines the net energy available from each fossil-based source without CCS deployment
    model.net_energy = pyo.Var(S, domain = pyo.NonNegativeReals)
    
    #This variable determines the net energy available from each fossil-based source with CCS deployment
    model.net_energy_CCS = pyo.Var(S, domain = pyo.NonNegativeReals)
    
    #This variable determines the carbon intensity of each fossil-based source with CCS deployment
    model.CI_RET = pyo.Var(S, domain = pyo.NonNegativeReals)
    
    #This variable determines the cumulative extent of CCS retrofit of all fossil-based sources
    model.sum_CCS = pyo.Var(domain = pyo.NonNegativeReals)    

    #OBJECTIVE FUNCTION
    
    #The objective function minimises the cumulative extent of CCS retrofit, thus minimising the NET requirement
    model.obj = pyo.Objective(expr = model.sum_CCS, sense = pyo.minimize)
   
    #CONSTRAINTS

    model.cons = pyo.ConstraintList()

    for s in S:
        #Calculation of carbon intensity for CCS retrofitted fossil-based sources
        model.cons.add((source_data[s]['CI'] * (1 - period_data['Constraints']['RR']) / (1 - period_data['Constraints']['X'])) == model.CI_RET[s])
        
        #Determine the net energy available from fossil-based sources without CCS retrofit
        model.cons.add((source_data[s]['Energy'] - model.CCS[s]) == model.net_energy[s])
       
        #Determine the net energy available from fossil-based sources with CCS retrofit
        model.cons.add((model.CCS[s] * (1 - period_data['Constraints']['X'])) == model.net_energy_CCS[s])
        
        #The extent of CCS retrofit on fossil-based sources should never exceed the available energy
        model.cons.add(model.CCS[s] <= source_data[s]['Energy'])
              
    #Total energy contribution from all energy sources to satisfy the total demand
    model.cons.add(sum((model.net_energy[s] + model.net_energy_CCS[s]) for s in S) + model.NET == period_data['Constraints']['Demand'])
    
    #Total CO2 load contribution from all energy sources to satisfy the emission limit
    model.cons.add(sum((model.net_energy[s] * source_data[s]['CI']) + (model.net_energy_CCS[s] * model.CI_RET[s]) for s in S)
               + (model.NET * period_data['Constraints']['NET_CI']) == period_data['Constraints']['Emission_limit'])
    
    model.cons.add(model.sum_CCS == sum(model.CCS[s] for s in S))
    
    return model

#Specifying the data for each model as an argument
model_1 = EP_Period(source_period_1, data_period_1)
model_2 = EP_Period(source_period_2, data_period_2)
model_3 = EP_Period(source_period_3, data_period_3)

#Creating a list with 3 strings
block_sets = ['P1', 'P2', 'P3']

#Adding the models to a dictionary to be accessed inside the function
EP = dict()
EP[block_sets[0]] = model_1
EP[block_sets[1]] = model_2
EP[block_sets[2]] = model_3

Full_model = pyo.ConcreteModel()

#This function defines each block - the block is model m containing all equations and variables
#It needs to be put in the right set (block_sets) with objective function turned off
def build_individual_blocks(model, block_sets):
    model = EP[block_sets]
    model.obj.deactivate()
    return model

#Defining the pyomo block structure with the set block sets and rule to build the blocks
Full_model.subprobs = pyo.Block(block_sets, rule = build_individual_blocks)


Full_model.obj = pyo.Objective(expr = Full_model.subprobs['P1'].sum_CCS +
                               Full_model.subprobs['P2'].sum_CCS +
                               Full_model.subprobs['P3'].sum_CCS, 
                               sense = pyo.minimize)

opt = SolverFactory('ipopt')
opt.solve(Full_model)

def EP_Results(source_data, period_data, period):
    model = Full_model.subprobs[period]
    print(' ')
    print('Time period', '=' , period)
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
        energy_planning.loc[s, 'Carbon Intensity'] = round(source_data[s]['CI'], 2)
        energy_planning.loc[s, 'CCS Ret'] = round(model.CCS[s](), 2)
        energy_planning.loc[s, 'CCS Carbon Intensity'] = round(model.CI_RET[s](), 2)
        energy_planning.loc['NET', 'CCS Carbon Intensity'] = period_data['Constraints']['NET_CI']
        energy_planning.loc[s, 'Net Energy wo CCS'] = round(model.net_energy[s](), 2)
        energy_planning.loc[s, 'Net Energy w CCS'] = round(model.net_energy_CCS[s](), 2)
        energy_planning.loc[s, 'Net Energy'] = round(model.net_energy[s]() + model.net_energy_CCS[s](), 2)
        energy_planning.loc['NET', 'Net Energy'] = round(model.NET(),2)
        energy_planning.loc[s, 'Carbon Load'] = round((model.net_energy[s]() * source_data[s]['CI']) + (model.net_energy_CCS[s]() * model.CI_RET[s]()), 2)
        energy_planning.loc['NET', 'Carbon Load'] = round(model.NET() * period_data['Constraints']['NET_CI'], 2)
    
    print('Energy Planning Table for', period)
    print(' ')
    print(energy_planning)
    
    energy = [0, 
              model.NET(), 
              model.net_energy['Renewables'](), 
              model.net_energy_CCS['Natural Gas'](),
              model.net_energy_CCS['Oil'](), 
              model.net_energy_CCS['Coal'](),          
              model.net_energy['Natural Gas'](),
              model.net_energy['Oil'](), 
              model.net_energy['Coal']()]
    
    emission = [0, 
                model.NET() * period_data['Constraints']['NET_CI'], 
                model.net_energy['Renewables']() * source_data['Renewables']['CI'],
                model.net_energy_CCS['Natural Gas']() * model.CI_RET['Natural Gas'](),
                model.net_energy_CCS['Oil']() * model.CI_RET['Oil'](),
                model.net_energy_CCS['Coal']() * model.CI_RET['Coal'](),           
                model.net_energy['Natural Gas']() * source_data['Natural Gas']['CI'],
                model.net_energy['Oil']() * source_data['Oil']['CI'], 
                model.net_energy['Coal']() * source_data['Coal']['CI']]
    

    energy_series = pd.Series(energy)
    energy_cum = energy_series.cumsum()
    #Creating a cumulative series for the energy
    
    emission_series = pd.Series(emission)
    emission_cum = emission_series.cumsum()
    #Creating a cumulative series for the emission
    
    x_coor = [-5, 90]
    y_coor = [0, 0]
    plt.plot(x_coor, y_coor, 'k', lw = 3)
    #Creating a horizontal line at the origin
    
    if period == 'P1':
        plt.plot(energy_cum, emission_cum, 'r', lw=3, label = period)
    elif period == 'P2':
        plt.plot(energy_cum, emission_cum, 'g', lw=3, label = period)
    else:
        plt.plot(energy_cum, emission_cum, 'm', lw=3, label = period)            
    
        
    plt.xlabel('Energy / TWh/y')
    plt.ylabel('CO2 Load / Mt/y')
    plt.grid(True)
    plt.title('Energy Planning Scenarios')
    plt.legend()
    
    return    

EP_Results(source_period_1, data_period_1, 'P1')
EP_Results(source_period_2, data_period_2, 'P2')
EP_Results(source_period_3, data_period_3, 'P3')

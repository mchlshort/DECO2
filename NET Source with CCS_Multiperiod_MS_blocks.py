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

def EP_Period_1():
    S = source_period_1.keys()
    model = pyo.ConcreteModel()
    
    #LIST OF VARIABLES
    
    model.CCS = pyo.Var(S, domain = pyo.NonNegativeReals)
    #This variable represents the extent of CCS retrofit for each fossil-based source

    model.NET = pyo.Var(domain = pyo.NonNegativeReals)
    #This variable represents the minimum deployment of NET 

    model.net_energy = pyo.Var(S, domain = pyo.NonNegativeReals)
    #This variable determines the net energy available from each fossil-based source without CCS deployment

    model.net_energy_CCS = pyo.Var(S, domain = pyo.NonNegativeReals)
    #This variable determines the net energy available from each fossil-based source with CCS deployment

    model.CI_RET = pyo.Var(S, domain = pyo.NonNegativeReals)
    #This variable determines the carbon intensity of each fossil-based source with CCS deployment
    
    model.sum_CCS = pyo.Var(domain = pyo.NonNegativeReals)
    # I add in a new variable that will make it easier to access from blocks
    #OBJECTIVE FUNCTION

    model.obj = pyo.Objective(expr = model.sum_CCS, sense = pyo.minimize)

    #CONSTRAINT

    model.cons = pyo.ConstraintList()

    for s in S:
        model.cons.add((source_period_1[s]['CI'] * (1 - data_period_1['Constraints']['RR']) / (1 - data_period_1['Constraints']['X'])) == model.CI_RET[s])
        #Calculation of carbon intensity for CCS retrofitted fossil-based sources
    
        model.cons.add((source_period_1[s]['Energy'] - model.CCS[s]) == model.net_energy[s])
        #Determine the net energy available from fossil-based sources without CCS retrofit
    
        model.cons.add((model.CCS[s] * (1 - data_period_1['Constraints']['X'])) == model.net_energy_CCS[s])
        #Determine the net energy available from fossil-based sources with CCS retrofit
    
        model.cons.add(model.CCS[s] <= source_period_1[s]['Energy'])
        #The extent of CCS retrofit on fossil-based sources should never exceed the available energy
    

    model.cons.add(sum((model.net_energy[s] + model.net_energy_CCS[s]) for s in S) + model.NET == data_period_1['Constraints']['Demand'])
    #Total energy contribution from all energy sources to satisfy the total demand


    model.cons.add(sum((model.net_energy[s] * source_period_1[s]['CI']) + (model.net_energy_CCS[s] * model.CI_RET[s]) for s in S)
               + (model.NET * data_period_1['Constraints']['NET_CI']) == data_period_1['Constraints']['Emission_limit'])
    #Total CO2 load contribution from all energy sources to satisfy the emission limit
    
    #NOTE NEW CONSTRAINT
    def _SumCCS(m):
        return model.sum_CCS == sum(model.CCS[s] for s in S)
        
    #Note that in this way of declaring a constraint, I have the set in the constraint.
    # The function is what will generate the constraint and it will call the constraint at every S
    model.SumCCSCons = pyo.Constraint(rule = _SumCCS)
     
    opt = SolverFactory('ipopt')
    opt.solve(model)

    print('Carbon Intensity of CCS Retrofitted sources i in Period 1')
    print(' ')
    for s in source_period_1.keys():    
        print(s, '=', round(model.CI_RET[s](), 3), 'TWh/y')

    print(' ')

    print('Extent of CCS retrofit on source i in Period 1')
    print(' ')
    for s in source_period_1.keys():    
        print(s, '=', round(model.CCS[s](), 2), 'TWh/y')

    print(' ')

    print('Net energy from source i without CCS retrofit in Period 1')
    print(' ')
    for s in source_period_1.keys():
        print(s, '=', round(model.net_energy[s](), 2), 'TWh/y')

    print(' ') 
    
    print('Net energy from source i with CCS retrofit in Period 1')
    print(' ')
    for s in source_period_1.keys():
        print(s, '=', round(model.net_energy_CCS[s](), 2), 'TWh/y')

    print(' ')  

    print('Minimum NET Deployment in Period 1 =', round(model.NET(), 2), 'TWh/y')   

    print(' ') 

    energy_planning = pd.DataFrame()

    for s in S:
        energy_planning.loc[s, 'Energy'] = source_period_1[s]['Energy']
        energy_planning.loc[s, 'CCS Ret'] = round(model.CCS[s](), 2)
        energy_planning.loc[s, 'Net Energy wo CCS'] = round(model.net_energy[s](), 2)
        energy_planning.loc[s, 'Net Energy w CCS'] = round(model.net_energy_CCS[s](), 2)
        energy_planning.loc[s, 'Net Energy'] = round(model.net_energy[s]() + model.net_energy_CCS[s](), 2)
        energy_planning.loc['NET', 'Net Energy'] = round(model.NET(),2)
        #energy_planning.loc[s, 'Carbon Intensity'] = round(source[s]['CI'], 2)
        #energy_planning.loc[s, 'CCS Carbon Intensity'] = round(model.CI_RET[s](), 2)
        #energy_planning.loc['NET', 'Carbon Intensity'] = data['Constraints']['NET_CI']
        energy_planning.loc[s, 'Carbon Load'] = round((model.net_energy[s]() * source_period_1[s]['CI']) + (model.net_energy_CCS[s]() * model.CI_RET[s]()), 2)
        energy_planning.loc['NET', 'Carbon Load'] = round(model.NET() * data_period_1['Constraints']['NET_CI'], 2)
    
    print('Energy Planning Table for Period 1')
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
                model.NET() * data_period_1['Constraints']['NET_CI'], 
                model.net_energy['Renewables']() * source_period_1['Renewables']['CI'],
                model.net_energy_CCS['Natural Gas']() * model.CI_RET['Natural Gas'](),
                model.net_energy_CCS['Oil']() * model.CI_RET['Oil'](),
                model.net_energy_CCS['Coal']() * model.CI_RET['Coal'](),           
                model.net_energy['Natural Gas']() * source_period_1['Natural Gas']['CI'],
                model.net_energy['Oil']() * source_period_1['Oil']['CI'], 
                model.net_energy['Coal']() * source_period_1['Coal']['CI']]
    

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

    plt.plot(energy_cum, emission_cum, 'r', lw=3, label = 'Period 1')
    plt.xlabel('Energy / TWh/y')
    plt.ylabel('CO2 Load / Mt/y')
    plt.grid(True)
    plt.title('Energy Planning Scenarios')
    plt.legend()
    return model

def EP_Period_2():
    T = source_period_2.keys()
    model = pyo.ConcreteModel()
    
    #LIST OF VARIABLES
    
    model.CCS = pyo.Var(T, domain = pyo.NonNegativeReals)
    #This variable represents the extent of CCS retrofit for each fossil-based source

    model.NET = pyo.Var(domain = pyo.NonNegativeReals)
    #This variable represents the minimum deployment of NET 

    model.net_energy = pyo.Var(T, domain = pyo.NonNegativeReals)
    #This variable determines the net energy available from each fossil-based source without CCS deployment

    model.net_energy_CCS = pyo.Var(T, domain = pyo.NonNegativeReals)
    #This variable determines the net energy available from each fossil-based source with CCS deployment

    model.CI_RET = pyo.Var(T, domain = pyo.NonNegativeReals)
    #This variable determines the carbon intensity of each fossil-based source with CCS deployment
    model.sum_CCS = pyo.Var(domain = pyo.NonNegativeReals)
    # I add in a new variable that will make it easier to access from blocks
    #OBJECTIVE FUNCTION

    model.obj = pyo.Objective(expr = model.sum_CCS, sense = pyo.minimize)

    #CONSTRAINT

    model.cons = pyo.ConstraintList()

    for t in T:
        model.cons.add((source_period_2[t]['CI'] * (1 - data_period_2['Constraints']['RR']) / (1 - data_period_2['Constraints']['X'])) == model.CI_RET[t])
        #Calculation of carbon intensity for CCS retrofitted fossil-based sources
    
        model.cons.add((source_period_2[t]['Energy'] - model.CCS[t]) == model.net_energy[t])
        #Determine the net energy available from fossil-based sources without CCS retrofit
    
        model.cons.add((model.CCS[t] * (1 - data_period_2['Constraints']['X'])) == model.net_energy_CCS[t])
        #Determine the net energy available from fossil-based sources with CCS retrofit
    
        model.cons.add(model.CCS[t] <= source_period_2[t]['Energy'])
        #The extent of CCS retrofit on fossil-based sources should never exceed the available energy
    

    model.cons.add(sum((model.net_energy[t] + model.net_energy_CCS[t]) for t in T) + model.NET == data_period_2['Constraints']['Demand'])
    #Total energy contribution from all energy sources to satisfy the total demand


    model.cons.add(sum((model.net_energy[t] * source_period_1[t]['CI']) + (model.net_energy_CCS[t] * model.CI_RET[t]) for t in T)
               + (model.NET * data_period_2['Constraints']['NET_CI']) == data_period_2['Constraints']['Emission_limit'])
    #Total CO2 load contribution from all energy sources to satisfy the emission limit
    #NOTE NEW CONSTRAINT
    def _SumCCS(m):
        return model.sum_CCS == sum(model.CCS[s] for s in T)
        
    #Note that in this way of declaring a constraint, I have the set in the constraint.
    # The function is what will generate the constraint and it will call the constraint at every S
    model.SumCCSCons = pyo.Constraint(rule = _SumCCS)            
    opt = SolverFactory('ipopt')
    opt.solve(model)
    
    print(' ')

    print('Carbon Intensity of CCS Retrofitted sources i in Period 2')
    print(' ')
    for t in source_period_2.keys():    
        print(t, '=', round(model.CI_RET[t](), 3), 'TWh/y')

    print(' ')

    print('Extent of CCS retrofit on source i in Period 2')
    print(' ')
    for t in source_period_2.keys():    
        print(t, '=', round(model.CCS[t](), 2), 'TWh/y')

    print(' ')

    print('Net energy from source i without CCS retrofit in Period 2')
    print(' ')
    for t in source_period_2.keys():
        print(t, '=', round(model.net_energy[t](), 2), 'TWh/y')

    print(' ') 
    
    print('Net energy from source i with CCS retrofit in Period 2')
    print(' ')
    for t in source_period_2.keys():
        print(t, '=', round(model.net_energy_CCS[t](), 2), 'TWh/y')

    print(' ')  

    print('Minimum NET Deployment in Period 2 =', round(model.NET(), 2), 'TWh/y')   

    print(' ') 

    energy_planning = pd.DataFrame()

    for t in T:
        energy_planning.loc[t, 'Energy'] = source_period_2[t]['Energy']
        energy_planning.loc[t, 'CCS Ret'] = round(model.CCS[t](), 2)
        energy_planning.loc[t, 'Net Energy wo CCS'] = round(model.net_energy[t](), 2)
        energy_planning.loc[t, 'Net Energy w CCS'] = round(model.net_energy_CCS[t](), 2)
        energy_planning.loc[t, 'Net Energy'] = round(model.net_energy[t]() + model.net_energy_CCS[t](), 2)
        energy_planning.loc['NET', 'Net Energy'] = round(model.NET(),2)
        #energy_planning.loc[s, 'Carbon Intensity'] = round(source[s]['CI'], 2)
        #energy_planning.loc[s, 'CCS Carbon Intensity'] = round(model.CI_RET[s](), 2)
        #energy_planning.loc['NET', 'Carbon Intensity'] = data['Constraints']['NET_CI']
        energy_planning.loc[t, 'Carbon Load'] = round((model.net_energy[t]() * source_period_2[t]['CI']) + (model.net_energy_CCS[t]() * model.CI_RET[t]()), 2)
        energy_planning.loc['NET', 'Carbon Load'] = round(model.NET() * data_period_2['Constraints']['NET_CI'], 2)
    
    print('Energy Planning Table for Period 2')
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
                model.NET() * data_period_2['Constraints']['NET_CI'], 
                model.net_energy['Renewables']() * source_period_2['Renewables']['CI'],
                model.net_energy_CCS['Natural Gas']() * model.CI_RET['Natural Gas'](),
                model.net_energy_CCS['Oil']() * model.CI_RET['Oil'](),
                model.net_energy_CCS['Coal']() * model.CI_RET['Coal'](),           
                model.net_energy['Natural Gas']() * source_period_2['Natural Gas']['CI'],
                model.net_energy['Oil']() * source_period_2['Oil']['CI'], 
                model.net_energy['Coal']() * source_period_2['Coal']['CI']]
    

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

    plt.plot(energy_cum, emission_cum, 'g', lw=3, label = 'Period 2')
    plt.xlabel('Energy / TWh/y')
    plt.ylabel('CO2 Load / Mt/y')
    plt.grid(True)
    plt.title('Energy Planning Scenarios')
    plt.legend()
    return model
    
def EP_Period_3():
    W = source_period_3.keys()
    model = pyo.ConcreteModel()
    
    #LIST OF VARIABLES
    
    model.CCS = pyo.Var(W, domain = pyo.NonNegativeReals)
    #This variable represents the extent of CCS retrofit for each fossil-based source

    model.NET = pyo.Var(domain = pyo.NonNegativeReals)
    #This variable represents the minimum deployment of NET 

    model.net_energy = pyo.Var(W, domain = pyo.NonNegativeReals)
    #This variable determines the net energy available from each fossil-based source without CCS deployment

    model.net_energy_CCS = pyo.Var(W, domain = pyo.NonNegativeReals)
    #This variable determines the net energy available from each fossil-based source with CCS deployment

    model.CI_RET = pyo.Var(W, domain = pyo.NonNegativeReals)
    #This variable determines the carbon intensity of each fossil-based source with CCS deployment

    model.sum_CCS = pyo.Var(domain = pyo.NonNegativeReals)
    # I add in a new variable that will make it easier to access from blocks
    #OBJECTIVE FUNCTION

    model.obj = pyo.Objective(expr = model.sum_CCS, sense = pyo.minimize)

    #CONSTRAINT

    model.cons = pyo.ConstraintList()

    for w in W:
        model.cons.add((source_period_3[w]['CI'] * (1 - data_period_3['Constraints']['RR']) / (1 - data_period_3['Constraints']['X'])) == model.CI_RET[w])
        #Calculation of carbon intensity for CCS retrofitted fossil-based sources
    
        model.cons.add((source_period_3[w]['Energy'] - model.CCS[w]) == model.net_energy[w])
        #Determine the net energy available from fossil-based sources without CCS retrofit
    
        model.cons.add((model.CCS[w] * (1 - data_period_3['Constraints']['X'])) == model.net_energy_CCS[w])
        #Determine the net energy available from fossil-based sources with CCS retrofit
    
        model.cons.add(model.CCS[w] <= source_period_3[w]['Energy'])
        #The extent of CCS retrofit on fossil-based sources should never exceed the available energy
    

    model.cons.add(sum((model.net_energy[w] + model.net_energy_CCS[w]) for w in W) + model.NET == data_period_3['Constraints']['Demand'])
    #Total energy contribution from all energy sources to satisfy the total demand


    model.cons.add(sum((model.net_energy[w] * source_period_1[w]['CI']) + (model.net_energy_CCS[w] * model.CI_RET[w]) for w in W)
               + (model.NET * data_period_3['Constraints']['NET_CI']) == data_period_3['Constraints']['Emission_limit'])
    #Total CO2 load contribution from all energy sources to satisfy the emission limit
    #NOTE NEW CONSTRAINT
    def _SumCCS(m):
        return model.sum_CCS == sum(model.CCS[s] for s in W)
        
    #Note that in this way of declaring a constraint, I have the set in the constraint.
    # The function is what will generate the constraint and it will call the constraint at every S
    model.SumCCSCons = pyo.Constraint(rule = _SumCCS)        
    opt = SolverFactory('ipopt')
    opt.solve(model)
    
    print(' ')
    print('PERIOD 3')
    print(' ')

    print('Carbon Intensity of CCS Retrofitted sources i in Period 3')
    print(' ')
    for w in source_period_3.keys():    
        print(w, '=', round(model.CI_RET[w](), 3), 'TWh/y')

    print(' ')

    print('Extent of CCS retrofit on source i in Period 3')
    print(' ')
    for w in source_period_3.keys():    
        print(w, '=', round(model.CCS[w](), 2), 'TWh/y')

    print(' ')

    print('Net energy from source i without CCS retrofit in Period 3')
    print(' ')
    for w in source_period_3.keys():
        print(w, '=', round(model.net_energy[w](), 2), 'TWh/y')

    print(' ') 
    
    print('Net energy from source i with CCS retrofit in Period 3')
    print(' ')
    for w in source_period_3.keys():
        print(w, '=', round(model.net_energy_CCS[w](), 2), 'TWh/y')

    print(' ')  

    print('Minimum NET Deployment in Period 3 =', round(model.NET(), 2), 'TWh/y')   

    print(' ') 

    energy_planning = pd.DataFrame()

    for w in W:
        energy_planning.loc[w, 'Energy'] = source_period_2[w]['Energy']
        energy_planning.loc[w, 'CCS Ret'] = round(model.CCS[w](), 2)
        energy_planning.loc[w, 'Net Energy wo CCS'] = round(model.net_energy[w](), 2)
        energy_planning.loc[w, 'Net Energy w CCS'] = round(model.net_energy_CCS[w](), 2)
        energy_planning.loc[w, 'Net Energy'] = round(model.net_energy[w]() + model.net_energy_CCS[w](), 2)
        energy_planning.loc['NET', 'Net Energy'] = round(model.NET(),2)
        #energy_planning.loc[s, 'Carbon Intensity'] = round(source[s]['CI'], 2)
        #energy_planning.loc[s, 'CCS Carbon Intensity'] = round(model.CI_RET[s](), 2)
        #energy_planning.loc['NET', 'Carbon Intensity'] = data['Constraints']['NET_CI']
        energy_planning.loc[w, 'Carbon Load'] = round((model.net_energy[w]() * source_period_3[w]['CI']) + (model.net_energy_CCS[w]() * model.CI_RET[w]()), 2)
        energy_planning.loc['NET', 'Carbon Load'] = round(model.NET() * data_period_3['Constraints']['NET_CI'], 2)
    
    print('Energy Planning Table for Period 3')
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
                model.NET() * data_period_3['Constraints']['NET_CI'], 
                model.net_energy['Renewables']() * source_period_3['Renewables']['CI'],
                model.net_energy_CCS['Natural Gas']() * model.CI_RET['Natural Gas'](),
                model.net_energy_CCS['Oil']() * model.CI_RET['Oil'](),
                model.net_energy_CCS['Coal']() * model.CI_RET['Coal'](),           
                model.net_energy['Natural Gas']() * source_period_3['Natural Gas']['CI'],
                model.net_energy['Oil']() * source_period_3['Oil']['CI'], 
                model.net_energy['Coal']() * source_period_3['Coal']['CI']]
    

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

    plt.plot(energy_cum, emission_cum, 'm', lw=3, label = 'Period 3')
    plt.xlabel('Energy / TWh/y')
    plt.ylabel('CO2 Load / Mt/y')
    plt.grid(True)
    plt.title('Energy Planning Scenarios')
    plt.legend()
    return model

print("Now let's solve these together as block")

# first we reutn each submodel
model1 = EP_Period_1()
model2 = EP_Period_2()
model3 = EP_Period_3()
# Now we want to add each submodel to a block
# Let's give each model a different set name
block_sets = ['P1','P2', 'P3']
#now we add the models to a dictionary so that we can access them inside the function later
sub1 = dict()
sub1[block_sets[2]] = model3
sub1[block_sets[1]] = model2
sub1[block_sets[0]] = model1
            
#Define model that we want to use these separate models to make           
Full_model = pyo.ConcreteModel()
# This function defines each block - the block is the model m (containing all equns and vars)
# but it needs to be put in the right set (block_sets) and also have its objective function turned off          
def build_individual_blocks(m, block_sets):
    m = sub1[block_sets]    
    m.obj.deactivate()  
    m.del_component(m.obj)    
    return m
# Define the pyomo block structure with the set block_sets and the rule to build the blocks      
Full_model.subprobs = pyo.Block(block_sets, rule = build_individual_blocks)
# Ok, so now we have all we need. 3 blocks, with our 3 periods, all in model Full_model. 
# Now we need a new objective function to solve - the problem is that the objective needs to
# see all the vars across all the blocks. To do this, we may need to access

Full_model.obj = pyo.Objective(expr = Full_model.subprobs['P1'].sum_CCS + Full_model.subprobs['P2'].sum_CCS + Full_model.subprobs['P3'].sum_CCS, sense = pyo.minimize)
opt = SolverFactory('ipopt')
opt.solve(Full_model, tee = True)

'''
Created on 4th April 2022

Energy Planning Scenario in Pyomo

This script presents the mathematical optimisation formulation concerning 
carbon-constrained energy planning for a specific geographical region or 
district.
 
Power plants are fuelled by either renewable energy sources e.g., solar, 
hydropower etc or fossil-based sources e.g., coal, natural gas etc. 

This energy planning is conducted for several periods (user-specified), with 
each period having its respective demand and CO2 emission limit

The satisfaction of the CO2 load limit is via the deployment of compensatory 
energy, CCS technology, alternative low-carbon fuels (replacing fossil fuels),
and negative emission technologies (NETs)

NETs are either made up of energy-producing NETs (EP-NETs) or energy-consuming 
NETs (EC-NETs). Examples of EP-NETs are biomass and biochar, while EC-NETs
are made up of enhanced weathering, direct air capture etc. 

EP-NETs and EC-NETs produce and consume energy during CO2 removal respectively

Alternative solid and gas fuels have low CO2 intensity, with a potential of 
replacing coal and natural gas in fossil-based power plants respectively

@author: Purusothmn, Dr Michael Short

'''
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import pandas as pd
import os
from openpyxl import load_workbook

cwd = os.getcwd()
model = pyo.ConcreteModel()

file_name = r'Optimal_Decarbonisation_User_Interface_11.xlsx'
model.plant = pd.read_excel(file_name, sheet_name = 'PLANT_DATA', index_col = 0, header = 32, nrows = 7).to_dict()
model.EP = pd.read_excel(file_name, sheet_name = 'ENERGY_PLANNING_DATA', index_col = 0, header = 7).to_dict()
model.fuel = pd.read_excel(file_name, sheet_name = 'FUEL_COST_DATA', index_col = 0, header = 12).to_dict()
model.COMP_CI = pd.read_excel(file_name, sheet_name = 'RENEWABLE_CI_DATA', index_col = 0, header = 9).to_dict()
model.COMP_COST = pd.read_excel(file_name, sheet_name = 'RENEWABLE_COST_DATA', index_col = 0, header = 9).to_dict()
model.CPX_1 = pd.read_excel(file_name, sheet_name = 'CAPEX_DATA_1', index_col = 0, header = 20).to_dict()
model.CPX_2 = pd.read_excel(file_name, sheet_name = 'CAPEX_DATA_2', index_col = 0, header = 20).to_dict()
model.SLD_CI = pd.read_excel(file_name, sheet_name = 'ALT_SOLID_CI', index_col = 0, header = 6).to_dict()
model.SLD_COST = pd.read_excel(file_name, sheet_name = 'ALT_SOLID_COST', index_col = 0, header = 6).to_dict()
model.GAS_CI = pd.read_excel(file_name, sheet_name = 'ALT_GAS_CI', index_col = 0, header = 6).to_dict()
model.GAS_COST = pd.read_excel(file_name, sheet_name = 'ALT_GAS_COST', index_col = 0, header = 6).to_dict()
model.CCS_data = pd.read_excel(file_name, sheet_name = 'CCS_DATA', index_col = 0, header = 12).to_dict()
model.NET_CI = pd.read_excel(file_name, sheet_name = 'NET_CI_DATA', index_col = 0, header = 12).to_dict()
model.NET_COST = pd.read_excel(file_name, sheet_name = 'NET_COST_DATA', index_col = 0, header = 12).to_dict()
model.TIME = pd.read_excel(file_name, sheet_name = 'TECH_IMPLEMENTATION_TIME', index_col = 0, header = 19).to_dict()

wb = load_workbook(file_name)

sheet_1 = wb['PLANT_DATA']
flag = sheet_1['B30'].value

numperiods = sheet_1['B31'].value + 1

sheet_2 = wb['CAPEX_DATA_1']
AFF = sheet_2['B18'].value

periods = list(range(1,numperiods,1))

def multiperiod_energy_planning(model, i):
    model.S = model.plant.keys() 
          
    #LIST OF VARIABLES
    #This variable determines the deployment of energy sources in power plant s for period i
    model.energy = pyo.Var(i, model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the carbon intensity of energy sources in power plant s with CCS technology 1 for period i
    model.CI_RET_1 = pyo.Var(i, model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the carbon intensity of energy sources in power plant s with CCS technology 2 for period i
    model.CI_RET_2 = pyo.Var(i, model.S, domain = pyo.NonNegativeReals)
    
    #Binary variable for power generation by power plant s for period i
    model.A = pyo.Var(i, model.S, domain = pyo.Binary)
    
    #Binary variable for the deployment of CCS technology 1 in power plant s for period i
    model.B = pyo.Var(i, model.S, domain = pyo.Binary)
    
    #Binary variable for the deployment of CCS technology 2 in power plant s for period i
    model.C = pyo.Var(i, model.S, domain = pyo.Binary)
    
    #Binary variable for the deployment of EP-NETs technology 1 for period i
    model.D = pyo.Var(i, domain = pyo.Binary)
    
    #Binary variable for the deployment of EP-NETs technology 2 for period i
    model.E = pyo.Var(i, domain = pyo.Binary)
    
    #Binary variable for the deployment of EP-NETs technology 3 for period i
    model.F = pyo.Var(i, domain = pyo.Binary)
    
    #Binary variable for the deployment of EC-NETs technology 1 for period i 
    model.G = pyo.Var(i, domain = pyo.Binary)
    
    #Binary variable for the deployment of EC-NETs technology 2 for period i 
    model.H = pyo.Var(i, domain = pyo.Binary)
    
    #Binary variable for the deployment of EC-NETs technology 3 for period i
    model.I = pyo.Var(i, domain = pyo.Binary)
    
    #Binary variable for the deployment of solar compensatory energy for period i 
    model.J = pyo.Var(i, domain = pyo.Binary)
    
    #Binary variable for the deployment of hydro compensatory energy for period i 
    model.K = pyo.Var(i, domain = pyo.Binary)
    
    #Binary variable for the deployment of biomass compensatory energy for period i 
    model.L = pyo.Var(i, domain = pyo.Binary)
    
    #Binary variable for the deployment of biogas compensatory energy for period i 
    model.M = pyo.Var(i, domain = pyo.Binary)
    
    #Binary variable for the deployment of MSW compensatory energy for period i 
    model.N = pyo.Var(i, domain = pyo.Binary)      
    
    #This variable represents the total deployment of CCS technology 1 & 2 in power plant s for period i
    model.CCS = pyo.Var(i, model.S, domain = pyo.NonNegativeReals)
    
    #This variable represents the deployment of CCS technology 1 in power plant s for period i
    model.CCS_1 = pyo.Var(i, model.S, domain = pyo.NonNegativeReals) 
    
    #This variable represents the deployment of CCS technology 2 in power plant s for period i
    model.CCS_2 = pyo.Var(i, model.S, domain = pyo.NonNegativeReals) 
    
    #This variable determines the net energy available from power plant s without CCS deployment for period i
    model.net_energy = pyo.Var(i, model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the net energy available from power plant s with CCS deployment for period i
    model.net_energy_CCS = pyo.Var(i, model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the net energy available from power plant s with the deployment of CCS technology 1 for period i
    model.net_energy_CCS_1 = pyo.Var(i, model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the net energy available from power plant s with the deployment of CCS technology 2 for period i
    model.net_energy_CCS_2 = pyo.Var(i, model.S, domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of EP_NETs technology 1 for period i
    model.EP_NET_1 = pyo.Var(i, domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of EP_NETs technology 2 for period i
    model.EP_NET_2 = pyo.Var(i, domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of EP_NETs technology 3 for period i 
    model.EP_NET_3 = pyo.Var(i, domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of EC_NETs technology 1 for period i 
    model.EC_NET_1 = pyo.Var(i, domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of EC_NETs technology 2 for period i
    model.EC_NET_2 = pyo.Var(i, domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of EC_NETs technology 3 for period i
    model.EC_NET_3 = pyo.Var(i, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of solar compensatory energy for period i
    model.comp_SOLAR = pyo.Var(i, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of hydro compensatory energy for period i
    model.comp_HYDRO = pyo.Var(i, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of biomass compensatory energy for period i
    model.comp_BM = pyo.Var(i, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of biogas compensatory energy for period i
    model.comp_BG = pyo.Var(i, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of MSW compensatory energy for period i
    model.comp_MSW = pyo.Var(i, domain = pyo.NonNegativeReals)

    #This variable determines the revised total CO2 emission for period i
    model.new_emission = pyo.Var(i, domain = pyo.NonNegativeReals)

    #This variable determines the total energy cost of power plant s for period i
    model.energy_cost = pyo.Var(i, model.S, domain = pyo.NonNegativeReals, initialize = 0)

    #This variable determines the total cost for period i
    model.sum_cost = pyo.Var(i, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of alternative solid fuel technology 1 for coal-based plants for period i
    model.solid_1 = pyo.Var(i, model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of alternative solid fuel technology 2 for coal-based plants for period i
    model.solid_2 = pyo.Var(i, model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of alternative gas fuel technology 1 for natural gas-based plants for period i
    model.gas_1 = pyo.Var(i, model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of alternative gas fuel technology 2 for natural gas-based plants for period i
    model.gas_2 = pyo.Var(i, model.S, domain = pyo.NonNegativeReals)
    
    #OBJECTIVE FUNCTION
    
    #For the minimum budget objective function, the total cost is minimised, subject to the satisfaction of the CO2 emission limit
    #For the minimum emission objective function, the total emission is minimised, subject to the available budgetary constraint
    if flag == 'min_budget':
        model.obj = pyo.Objective(expr = sum(model.sum_cost[i] for i in periods), sense = pyo.minimize)
    else:
        model.obj = pyo.Objective(expr = sum(model.new_emission[i] for i in periods), sense = pyo.minimize)
   
    #CONSTRAINTS
    
    #Prior to any energy planning, the total power generation from all power plants should satisfy the regional energy demand for period i
    def demand(model, i, s):
        return model.EP['Demand'][i] == sum(model.energy[i,s] for s in model.S)
        
    model.Cons_1 = pyo.Constraint(i, model.S, rule = demand)
    
    #Calculation of carbon intensity of energy sources with CCS technology 1 in power plant s for period i
    def CCS_CI_1(model, i, s):
        return model.plant[s]['CI'] * (1 - model.CCS_data['RR_1'][i]) / (1 - model.CCS_data['X_1'][i]) == model.CI_RET_1[i,s]
    
    model.Cons_2 = pyo.Constraint(i, model.S, rule = CCS_CI_1)
    
    #Calculation of carbon intensity of energy sources with CCS technology 2 in power plant s for period i
    def CCS_CI_2(model, i, s):
        return model.plant[s]['CI'] * (1 - model.CCS_data['RR_2'][i]) / (1 - model.CCS_data['X_2'][i]) == model.CI_RET_2[i,s]
    
    model.Cons_3 = pyo.Constraint(i, model.S, rule = CCS_CI_2)
    
    #The deployment of energy source in power plant s should at least satisfy the lower bound for period i
    def lower_bound_energy(model, i, s):
        return model.energy[i,s] >= model.plant[s]['LB'] * model.A[i,s]
        
    model.Cons_4 = pyo.Constraint(i, model.S, rule = lower_bound_energy)
    
    #The deployment of energy source in power plant s should at most satisfy the upper bound for period i
    def upper_bound_energy(model, i, s):
        return model.energy[i,s] <= model.plant[s]['UB'] * model.A[i,s]
        
    model.Cons_5 = pyo.Constraint(i, model.S, rule = upper_bound_energy)
    
    def plant_commission(model, i, s):
        if i < model.plant[s]['ON']:
            return model.energy[i,s] == 0
        else:
            return model.energy[i,s] >= 0
            
    model.Cons_6 = pyo.Constraint(i, model.S, rule = plant_commission)
    
    def plant_decommission(model, i, s):
        if i >= model.plant[s]['OFF']:
            #print(i,s,model.plant[s]['OFF'])
            return model.energy[i,s] == 0
        else:
            return model.energy[i,s] >= 0
            
    model.Cons_7 = pyo.Constraint(i, model.S, rule = plant_decommission)
    
    #The total CCS deployment in power plant s should be equal to summation of deployment of individual types of  CCS technology for period i
    def CCS_total(model, i, s):
        return model.CCS_1[i,s] + model.CCS_2[i,s] ==  model.CCS[i,s]
        
    model.Cons_8 = pyo.Constraint(i, model.S, rule = CCS_total)
    
    #The total CCS deployment should be limited to the energy generation of power plant s for period i
    def CCS_limit_total(model, i, s):
        return model.CCS[i,s] <= model.energy[i,s]
    
    model.Cons_9 = pyo.Constraint(i, model.S, rule = CCS_limit_total)
    
    #The deployment of CCS technology 1 at later periods should at least match the deployment in the previous period
    def CCS_1_constraint(model, i, s):
        if i == numperiods - 1:
            return pyo.Constraint.Skip
        else:
            return model.CCS_1[i+1,s] >= model.CCS_1[i,s]
        
    model.Cons_10 = pyo.Constraint(i, model.S, rule = CCS_1_constraint)
    
    #The deployment of CCS technology 2 at later periods should at least match the deployment in the previous period    
    def CCS_2_constraint(model, i, s):
        if i == numperiods - 1:
            return pyo.Constraint.Skip
        else:
            return model.CCS_2[i+1,s] >= model.CCS_2[i,s]
        
    model.Cons_11 = pyo.Constraint(i, model.S, rule = CCS_2_constraint)
    
    #If power plant s is decomissioned in a period, it should remain decommissioned at later periods 
    def energy_constraint(model, i, s):
        if i <= model.plant[s]['OFF'] - 2:
            return model.energy[i+1,s] >= model.energy[i,s]
        else:
            return pyo.Constraint.Skip
        
    model.Cons_12 = pyo.Constraint(i, model.S, rule = energy_constraint)
    
    #Determine the net energy available from power plant s with CCS technology 1 for period i
    def CCS_1_net_energy(model, i, s):
       return model.CCS_1[i,s] * (1 - model.CCS_data['X_1'][i]) == model.net_energy_CCS_1[i,s]
        
    model.Cons_13 = pyo.Constraint(i, model.S, rule = CCS_1_net_energy)

    #Determine the net energy available from power plant s with CCS technology 2 for period i
    def CCS_2_net_energy(model, i, s):
        return model.CCS_2[i,s] * (1 - model.CCS_data['X_2'][i]) == model.net_energy_CCS_2[i,s]
        
    model.Cons_14 = pyo.Constraint(i, model.S, rule = CCS_2_net_energy)  
        
    #If selected, the deployment of CCS technology 1 in power plant s is limited by the upper bound of the energy output for period i     
    def CCS_limit_1(model, i, s):
        return model.CCS_1[i,s] <= model.plant[s]['UB'] * model.B[i,s]
        
    model.Cons_15 = pyo.Constraint(i, model.S, rule = CCS_limit_1)
	    
    #If selected, the deployment of CCS technology 2 in power plant s is limited by the upper bound of the energy output for period i
    def CCS_limit_2(model, i, s):
        return model.CCS_2[i,s] <= model.plant[s]['UB'] * model.C[i,s]
        
    model.Cons_16 = pyo.Constraint(i, model.S, rule = CCS_limit_2)  
    
        
    #Determine the net energy available from power plant s with the deployment of CCS technologies 1 & 2 for period i
    def CCS_net_energy(model, i, s):
        return model.net_energy_CCS_1[i,s] + model.net_energy_CCS_2[i,s] == model.net_energy_CCS[i,s]
        
    model.Cons_17 = pyo.Constraint(i, model.S, rule = CCS_net_energy)   
    
    #The deployment of alternative solid fuel technology 1 at later periods should at least match the deployment in the previous period
    def alt_solid_1_constraint(model, i, s):
        if i == numperiods - 1:
            return pyo.Constraint.Skip
        else:
            return model.solid_1[i+1,s] >= model.solid_1[i,s]
        
    model.Cons_18 = pyo.Constraint(i, model.S, rule = alt_solid_1_constraint)
    
    #The deployment of alternative solid fuel technology 2 at later periods should at least match the deployment in the previous period    
    def alt_solid_2_constraint(model, i, s):
        if i == numperiods - 1:
            return pyo.Constraint.Skip
        else:
            return model.solid_2[i+1,s] >= model.solid_2[i,s]
        
    model.Cons_19 = pyo.Constraint(i, model.S, rule = alt_solid_2_constraint)
    
    #The deployment of alternative gas fuel technology 1 at later periods should at least match the deployment in the previous period
    def alt_gas_1_constraint(model, i, s):
        if i == numperiods - 1:
            return pyo.Constraint.Skip
        else:
            return model.gas_1[i+1,s] >= model.gas_1[i,s]
        
    model.Cons_20 = pyo.Constraint(i, model.S, rule = alt_gas_1_constraint)
    
    #The deployment of alternative gas fuel technology 2 at later periods should at least match the deployment in the previous period    
    def alt_gas_2_constraint(model, i, s):
        if i == numperiods - 1:
            return pyo.Constraint.Skip
        else:
            return model.gas_2[i+1,s] >= model.gas_2[i,s]
        
    model.Cons_21 = pyo.Constraint(i, model.S, rule = alt_gas_2_constraint)
    
    #The total energy contribution must equal the initially determined energy contribution of power plant s for period i
    def fuel_substitution(model, i, s):
        if 'REN' in model.plant[s].values():
            return model.net_energy[i,s] == model.energy[i,s]
        elif 'NG' in model.plant[s].values():
            return model.net_energy[i,s] + model.CCS_1[i,s] + model.CCS_2[i,s] + model.gas_1[i,s] + model.gas_2[i,s] == model.energy[i,s]
        elif 'COAL' in model.plant[s].values():
            return model.net_energy[i,s] + model.CCS_1[i,s] + model.CCS_2[i,s] + model.solid_1[i,s] + model.solid_2[i,s] == model.energy[i,s]
        else:
            return model.net_energy[i,s] + model.CCS_1[i,s] + model.CCS_2[i,s] == model.energy[i,s]
        
    model.Cons_22 = pyo.Constraint(i, model.S, rule = fuel_substitution)  
    
    #If power plant s is fuelled by renewable energy sources, CCS technology 1 would not be deployed for period i
    def no_CCS_1(model, i, s):
        if 'REN' in model.plant[s].values():
            return model.CCS_1[i,s] == 0
        else:
            return pyo.Constraint.Skip
    
    model.Cons_23 = pyo.Constraint(i, model.S, rule = no_CCS_1) 
    
    #If power plant s is fuelled by renewable energy sources, CCS technology 1 would not be deployed for period i
    def no_CCS_2(model, i, s):
        if 'REN' in model.plant[s].values():
            return model.CCS_2[i,s] == 0
        else:
            return pyo.Constraint.Skip
    
    model.Cons_24 = pyo.Constraint(i, model.S, rule = no_CCS_2)  
    
    #Technology implementation time for CCS technology 1
    def deployment_CCS_1(model, i, s):
        if model.TIME['CCS_1'][i] == 'NO':
            return model.B[i,s] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_25 = pyo.Constraint(i, model.S, rule = deployment_CCS_1)   
    
    #Technology implementation time for CCS technology 2
    def deployment_CCS_2(model, i, s):
        if model.TIME['CCS_2'][i] == 'NO':
            return model.C[i,s] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_26 = pyo.Constraint(i, model.S, rule = deployment_CCS_2)   
        
    #Technology implementation time for EP-NETs technology 1
    def deployment_EP_NETs_1(model, i):
        if model.TIME['EP_NETs_1'][i] == 'NO':
            return model.D[i] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_27 = pyo.Constraint(i, rule = deployment_EP_NETs_1)   
    
    #Technology implementation time for EP-NETs technology 2
    def deployment_EP_NETs_2(model, i):
        if model.TIME['EP_NETs_2'][i] == 'NO':
            return model.E[i] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_28 = pyo.Constraint(i, rule = deployment_EP_NETs_2) 
    
    #Technology implementation time for EP-NETs technology 3
    def deployment_EP_NETs_3(model, i):
        if model.TIME['EP_NETs_3'][i] == 'NO':
            return model.F[i] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_29 = pyo.Constraint(i, rule = deployment_EP_NETs_3)
    
    #Technology implementation time for EC-NETs technology 1
    def deployment_EC_NETs_1(model, i):
        if model.TIME['EC_NETs_1'][i] == 'NO':
            return model.G[i] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_30 = pyo.Constraint(i, rule = deployment_EC_NETs_1)   
    
    #Technology implementation time for EC-NETs technology 2
    def deployment_EC_NETs_2(model, i):
        if model.TIME['EC_NETs_2'][i] == 'NO':
            return model.H[i] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_31 = pyo.Constraint(i, rule = deployment_EC_NETs_2) 
    
    #Technology implementation time for EC-NETs technology 3
    def deployment_EC_NETs_3(model, i):
        if model.TIME['EC_NETs_3'][i] == 'NO':
            return model.I[i] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_32 = pyo.Constraint(i, rule = deployment_EC_NETs_3)
    
    #Technology implementation time for solar compensatory energy
    def deployment_solar(model, i):
        if model.TIME['SOLAR'][i] == 'NO':
            return model.J[i] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_33 = pyo.Constraint(i, rule = deployment_solar)
    
    #Technology implementation time for hydro compensatory energy
    def deployment_hydro(model, i):
        if model.TIME['HYDRO'][i] == 'NO':
            return model.K[i] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_34 = pyo.Constraint(i, rule = deployment_hydro)
    
    #Technology implementation time for biomass compensatory energy
    def deployment_biomass(model, i):
        if model.TIME['BIOMASS'][i] == 'NO':
            return model.L[i] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_35 = pyo.Constraint(i, rule = deployment_biomass)
    
    #Technology implementation time for biogas compensatory energy
    def deployment_biogas(model, i):
        if model.TIME['BIOGAS'][i] == 'NO':
            return model.M[i] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_36 = pyo.Constraint(i, rule = deployment_biogas)
    
    #Technology implementation time for MSW compensatory energy
    def deployment_MSW(model, i):
        if model.TIME['MSW'][i] == 'NO':
            return model.N[i] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_37 = pyo.Constraint(i, rule = deployment_MSW)
    
    #Technology implementation time for alternative solid fuel type 1
    def deployment_alt_solid_1(model, i, s):
        if model.TIME['SOLID_1'][i] == 'NO':
            return model.solid_1[i,s] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_38 = pyo.Constraint(i, model.S, rule = deployment_alt_solid_1)

    #Technology implementation time for alternative solid fuel type 2
    def deployment_alt_solid_2(model, i, s):
        if model.TIME['SOLID_2'][i] == 'NO':
            return model.solid_2[i,s] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_39 = pyo.Constraint(i, model.S, rule = deployment_alt_solid_2)
    
    #Technology implementation time for alternative gas fuel type 1
    def deployment_alt_gas_1(model, i, s):
        if model.TIME['GAS_1'][i] == 'NO':
            return model.gas_1[i,s] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_40 = pyo.Constraint(i, model.S, rule = deployment_alt_gas_1)

    #Technology implementation time for alternative gas fuel type 2
    def deployment_alt_gas_2(model, i, s):
        if model.TIME['GAS_2'][i] == 'NO':
            return model.gas_2[i,s] == 0
        else:
            return pyo.Constraint.Skip
        
    model.Cons_41 = pyo.Constraint(i, model.S, rule = deployment_alt_gas_2)
    
    #Big M formulation for EP-NETs technology 1 deployment for period i
    def big_M_EP_NETs_1(model, i):
        return model.EP_NET_1[i] <= model.D[i] * 1000
    
    model.Cons_42 = pyo.Constraint(i, rule = big_M_EP_NETs_1) 
    
    #Big M formulation for EP-NETs technology 2 deployment for period i
    def big_M_EP_NETs_2(model, i):
        return model.EP_NET_2[i] <= model.E[i] * 1000
    
    model.Cons_43 = pyo.Constraint(i, rule = big_M_EP_NETs_2) 
    
    #Big M formulation for EP-NETs technology 3 deployment for period i
    def big_M_EP_NETs_3(model, i):
        return model.EP_NET_3[i] <= model.F[i] * 1000
    
    model.Cons_44 = pyo.Constraint(i, rule = big_M_EP_NETs_3) 

    #Big M formulation for EC-NETs technology 1 deployment for period i
    def big_M_EC_NETs_1(model, i):
        return model.EC_NET_1[i] <= model.G[i] * 1000
    
    model.Cons_45 = pyo.Constraint(i, rule = big_M_EC_NETs_1) 
    
    #Big M formulation for EC-NETs technology 2 deployment for period i
    def big_M_EC_NETs_2(model, i):
        return model.EC_NET_2[i] <= model.H[i] * 1000
    
    model.Cons_46 = pyo.Constraint(i, rule = big_M_EC_NETs_2) 
    
    #Big M formulation for EC-NETs technology 3 deployment for period i
    def big_M_EC_NETs_3(model, i):
        return model.EC_NET_3[i] <= model.I[i] * 1000
    
    model.Cons_47 = pyo.Constraint(i, rule = big_M_EC_NETs_3) 
    
    #Big M formulation for deployment of solar compensatory energy for period i
    def big_M_solar(model, i):
        return model.comp_SOLAR[i] <= model.J[i] * 1000
    
    model.Cons_48 = pyo.Constraint(i, rule = big_M_solar) 
    
    #Big M formulation for deployment of hydro compensatory energy for period i
    def big_M_hydro(model, i):
        return model.comp_HYDRO[i] <= model.K[i] * 1000
    
    model.Cons_49 = pyo.Constraint(i, rule = big_M_hydro) 
    
    #Big M formulation for deployment of BM compensatory energy for period i
    def big_M_biomass(model, i):
        return model.comp_BM[i] <= model.L[i] * 1000
    
    model.Cons_50 = pyo.Constraint(i, rule = big_M_biomass) 

    #Big M formulation for deployment of BG compensatory energy for period i
    def big_M_biogas(model, i):
        return model.comp_BG[i] <= model.M[i] * 1000
    
    model.Cons_51 = pyo.Constraint(i, rule = big_M_biogas) 
    
    #Big M formulation for deployment of MSW compensatory energy for period i
    def big_M_MSW(model, i):
        return model.comp_MSW[i] <= model.N[i] * 1000
    
    model.Cons_52 = pyo.Constraint(i, rule = big_M_MSW) 
    
     #Total energy contribution from all energy sources to satisfy the total demand for period i
    def total_energy(model, i, s):
        return sum((model.net_energy[i,s] + model.net_energy_CCS_1[i,s] + model.net_energy_CCS_2[i,s] + model.solid_1[i,s] + model.solid_2[i,s] + model.gas_1[i,s] + model.gas_2[i,s]) for s in model.S) + model.comp_SOLAR[i] + model.comp_HYDRO[i] + model.comp_BM[i] + model.comp_BG[i] + model.comp_MSW[i] + model.EP_NET_1[i] + model.EP_NET_2[i] + model.EP_NET_3[i] == model.EP['Demand'][i] + model.EC_NET_1[i] + model.EC_NET_2[i] + model.EC_NET_3[i]
        
    model.Cons_53 = pyo.Constraint(i, model.S, rule = total_energy)
    
    #The total CO2 load contribution from all energy sources must satisfy most the CO2 emission limit in period i
    def total_CO2_load(model, i, s):
        return (sum((model.net_energy[i,s] * model.plant[s]['CI']) + (model.net_energy_CCS_1[i,s] * model.plant[s]['CI'] * (1 - model.CCS_data['RR_1'][i]) / (1 - model.CCS_data['X_1'][i])) + (model.net_energy_CCS_2[i,s] * model.plant[s]['CI'] * (1 - model.CCS_data['RR_2'][i]) / (1 - model.CCS_data['X_2'][i])) 
        + (model.solid_1[i,s] * model.SLD_CI['SOLID_1'][i]) + (model.solid_2[i,s] * model.SLD_CI['SOLID_2'][i]) 
        + (model.gas_1[i,s] * model.GAS_CI['GAS_1'][i]) + (model.gas_2[i,s] * model.GAS_CI['GAS_2'][i]) for s in model.S) 
        + (model.EC_NET_1[i] * model.NET_CI['EC_NETs_1'][i])
        + (model.EC_NET_2[i] * model.NET_CI['EC_NETs_2'][i])
        + (model.EC_NET_3[i] * model.NET_CI['EC_NETs_3'][i])
        + (model.EP_NET_1[i] * model.NET_CI['EP_NETs_1'][i]) 
        + (model.EP_NET_2[i] * model.NET_CI['EP_NETs_2'][i])
        + (model.EP_NET_3[i] * model.NET_CI['EP_NETs_3'][i])
        + (model.comp_SOLAR[i] * model.COMP_CI['SOLAR'][i])
        + (model.comp_HYDRO[i] * model.COMP_CI['HYDRO'][i]) 
        + (model.comp_BM[i] * model.COMP_CI['BIOMASS'][i])
        + (model.comp_BG[i] * model.COMP_CI['BIOGAS'][i]) 
        + (model.comp_MSW[i] * model.COMP_CI['MSW'][i]) == model.new_emission[i])

    model.Cons_54 = pyo.Constraint(i, model.S, rule = total_CO2_load)
       
    #Determining the cumulative total fuel and annualised capital cost for all power plants for period i
    def energy_cost(model, i, s):
        if 'SOLAR' in model.plant[s].values():
            return model.energy_cost[i,s] == (model.net_energy[i,s] * model.fuel['SOLAR'][i]) + (AFF * model.CPX_1['SOLAR'][i] * model.A[i,s]) + (AFF * model.energy[i,s] * model.CPX_2['SOLAR'][i])
        elif 'HYDRO' in model.plant[s].values():
            return model.energy_cost[i,s] == (model.net_energy[i,s] * model.fuel['HYDRO'][i]) + (AFF * model.CPX_1['HYDRO'][i] * model.A[i,s]) + (AFF * model.energy[i,s] * model.CPX_2['HYDRO'][i])
        elif 'BIOGAS' in model.plant[s].values():
            return model.energy_cost[i,s] == (model.net_energy[i,s] * model.fuel['BIOGAS'][i]) + (AFF * model.CPX_1['BIOGAS'][i] * model.A[i,s]) + (AFF * model.energy[i,s] * model.CPX_2['BIOGAS'][i])
        elif 'BIOMASS' in model.plant[s].values():
            return model.energy_cost[i,s] == (model.net_energy[i,s] * model.fuel['BIOMASS'][i]) + (AFF * model.CPX_1['BIOMASS'][i] * model.A[i,s]) + (AFF * model.energy[i,s] * model.CPX_2['BIOMASS'][i])
        elif 'MSW' in model.plant[s].values():
            return model.energy_cost[i,s] == (model.net_energy[i,s] * model.fuel['MSW'][i]) + (AFF * model.CPX_1['MSW'][i] * model.A[i,s]) + (AFF * model.energy[i,s] * model.CPX_2['MSW'][i])
        elif 'NG' in model.plant[s].values():
            return model.energy_cost[i,s] == (model.net_energy[i,s] * model.fuel['NG'][i]) + (AFF * model.CPX_1['NG'][i] * model.A[i,s]) + (AFF * model.energy[i,s] * model.CPX_2['NG'][i])
        elif 'OIL' in model.plant[s].values():
            return model.energy_cost[i,s] == (model.net_energy[i,s] * model.fuel['OIL'][i]) + (AFF * model.CPX_1['OIL'][i] * model.A[i,s]) + (AFF * model.energy[i,s] * model.CPX_2['OIL'][i])
        else:
            return model.energy_cost[i,s] == (model.net_energy[i,s] * model.fuel['COAL'][i]) + (AFF * model.CPX_1['COAL'][i] * model.A[i,s]) + (AFF * model.energy[i,s] * model.CPX_2['COAL'][i])
    
    model.Cons_55 = pyo.Constraint(i, model.S, rule = energy_cost)        
    
    #The summation of cost for each power plant s should equal to the total cost of each period i
    def sum_cost(model, i, s):
        return (sum((model.net_energy_CCS_1[i,s] * model.CCS_data['Cost_CCS_1'][i]) + (model.net_energy_CCS_2[i,s] * model.CCS_data['Cost_CCS_2'][i]) + (model.CCS_data['FX_Cost_CCS_1'][i] * model.B[i,s]) 
        + (model.CCS_data['FX_Cost_CCS_2'][i] * model.C[i,s]) + (model.solid_1[i,s] * model.SLD_COST['SOLID_1'][i]) + (model.solid_2[i,s] * model.SLD_COST['SOLID_2'][i]) + (model.gas_1[i,s] * model.GAS_COST['GAS_1'][i]) + (model.gas_2[i,s] * model.GAS_COST['GAS_2'][i]) for s in model.S)
        + (model.EC_NET_1[i] * model.NET_COST['EC_NETs_1'][i]) + (AFF * model.CPX_1['EC_NETs_1'][i] * model.G[i]) + (AFF * model.EC_NET_1[i] * model.CPX_2['EC_NETs_1'][i])
        + (model.EC_NET_2[i] * model.NET_COST['EC_NETs_2'][i]) + (AFF * model.CPX_1['EC_NETs_2'][i] * model.H[i]) + (AFF * model.EC_NET_2[i] * model.CPX_2['EC_NETs_2'][i])
        + (model.EC_NET_3[i] * model.NET_COST['EC_NETs_3'][i]) + (AFF * model.CPX_1['EC_NETs_3'][i] * model.I[i]) + (AFF * model.EC_NET_3[i] * model.CPX_2['EC_NETs_3'][i])
        + (model.EP_NET_1[i] * model.NET_COST['EP_NETs_1'][i]) + (AFF * model.CPX_1['EP_NETs_1'][i] * model.D[i]) + (AFF * model.EP_NET_1[i] * model.CPX_2['EP_NETs_1'][i])
        + (model.EP_NET_2[i] * model.NET_COST['EP_NETs_2'][i]) + (AFF * model.CPX_1['EP_NETs_2'][i] * model.E[i]) + (AFF * model.EP_NET_2[i] * model.CPX_2['EP_NETs_2'][i])
        + (model.EP_NET_3[i] * model.NET_COST['EP_NETs_3'][i]) + (AFF * model.CPX_1['EP_NETs_3'][i] * model.F[i]) + (AFF * model.EP_NET_3[i] * model.CPX_2['EP_NETs_3'][i])
        + (model.comp_SOLAR[i] * model.COMP_COST['SOLAR'][i]) + (AFF * model.CPX_1['SOLAR'][i] * model.J[i]) + (AFF * model.comp_SOLAR[i] * model.CPX_2['SOLAR'][i])
        + (model.comp_HYDRO[i] * model.COMP_COST['HYDRO'][i]) + (AFF * model.CPX_1['HYDRO'][i] * model.K[i]) + (AFF * model.comp_HYDRO[i] * model.CPX_2['HYDRO'][i])
        + (model.comp_BM[i] * model.COMP_COST['BIOMASS'][i]) + (AFF * model.CPX_1['BIOMASS'][i] * model.L[i]) + (AFF * model.comp_BM[i] * model.CPX_2['BIOMASS'][i])
        + (model.comp_BG[i] * model.COMP_COST['BIOGAS'][i]) + (AFF * model.CPX_1['BIOGAS'][i] * model.M[i]) + (AFF * model.comp_BG[i] * model.CPX_2['BIOGAS'][i])
        + (model.comp_MSW[i] * model.COMP_COST['MSW'][i]) + (AFF * model.CPX_1['MSW'][i] * model.N[i]) + (AFF * model.comp_MSW[i] * model.CPX_2['MSW'][i])
        + sum(model.energy_cost[i,s] for s in model.S) == model.sum_cost[i])
        
    model.Cons_56 = pyo.Constraint(i, model.S, rule = sum_cost)
    
    #For the minimum budget objective function, the total cost is minimised, subject to the satisfaction of the CO2 emission limit
    #For the minimum emission objective function, the total emission is minimised, subject to the available budgetary constraint
    def objective_constraint(model, i):
        if flag == 'min_budget':
            return model.new_emission[i] <= model.EP['Limit'][i]
        else:
            return model.sum_cost[i] <= model.EP['Budget'][i]
    
    model.Cons_57 = pyo.Constraint(i, rule = objective_constraint)
    
    #opt = SolverFactory('octeract-engine', tee = True)
    #results = opt.solve(model)
    
    opt = SolverFactory('gams')
    #sys.exit()
    results = opt.solve(model, solver = 'cplex')
    
    print(results)
    #model.pprint()   
    return model

def multiperiod_energy_planning_results(model, i):
    energy_planning = pd.DataFrame()

    for s in model.plant.keys():
        energy_planning.loc[s, 'Fuel'] = model.plant[s]['Fuel']
        energy_planning.loc[s, 'Energy Generation'] = model.A[i,s]()
        energy_planning.loc[s, 'Energy'] = round(model.energy[i,s](), 2)
        energy_planning.loc[s, 'CI'] = model.plant[s]['CI']
        energy_planning.loc[s, 'CCS_1 CI'] = round(model.CI_RET_1[i,s](), 3)
        energy_planning.loc[s, 'CCS_2 CI'] = round(model.CI_RET_2[i,s](), 3)
        energy_planning.loc[s, 'CCS_1 Selection'] = model.B[i,s]()
        energy_planning.loc[s, 'CCS_2 Selection'] = model.C[i,s]()
        energy_planning.loc[s, 'CCS_1 Ret'] = round(model.CCS_1[i,s](), 2) 
        energy_planning.loc[s, 'CCS_2 Ret'] = round(model.CCS_2[i,s](), 2)       
        energy_planning.loc[s, 'Net Energy wo CCS'] = round(model.net_energy[i,s](), 2)
        energy_planning.loc[s, 'Net Energy w CCS_1'] = round(model.net_energy_CCS_1[i,s](), 2)
        energy_planning.loc[s, 'Net Energy w CCS_2'] = round(model.net_energy_CCS_2[i,s](), 2)
        energy_planning.loc[s, 'SOLID_1'] = round(model.solid_1[i,s](), 2)
        energy_planning.loc[s, 'SOLID_2'] = round(model.solid_2[i,s](), 2)
        energy_planning.loc[s, 'GAS_1'] = round(model.gas_1[i,s](), 2)
        energy_planning.loc[s, 'GAS_2'] = round(model.gas_2[i,s](), 2)
        energy_planning.loc[s, 'Net Energy'] = round(model.net_energy[i,s]() + model.net_energy_CCS[i,s]() + model.solid_1[i,s]() + model.solid_2[i,s]() + model.gas_1[i,s]() + model.gas_2[i,s](), 2)
        energy_planning.loc[s, 'Carbon Load'] = round((model.net_energy[i,s]() * model.plant[s]['CI']) + (model.net_energy_CCS_1[i,s]() * model.CI_RET_1[i,s]()) + (model.net_energy_CCS_2[i,s]() * model.CI_RET_2[i,s]()) + (model.solid_1[i,s]() * model.SLD_CI['SOLID_1'][i]) + (model.solid_2[i,s]() * model.SLD_CI['SOLID_2'][i]) + (model.gas_1[i,s]() * model.GAS_CI['GAS_1'][i]) + (model.gas_2[i,s]() * model.GAS_CI['GAS_2'][i]), 2)
        
    energy_planning.loc['EP_NET_1', 'Fuel'] = 'EP_NET_1'
    energy_planning.loc['EP_NET_2', 'Fuel'] = 'EP_NET_2'
    energy_planning.loc['EP_NET_3', 'Fuel'] = 'EP_NET_3'
    energy_planning.loc['EC_NET_1', 'Fuel'] = 'EC_NET_1'
    energy_planning.loc['EC_NET_2', 'Fuel'] = 'EC_NET_2' 
    energy_planning.loc['EC_NET_3', 'Fuel'] = 'EC_NET_3' 
    energy_planning.loc['EP_NET_1', 'Energy Generation'] = model.D[i]()
    energy_planning.loc['EP_NET_2', 'Energy Generation'] = model.E[i]()
    energy_planning.loc['EP_NET_3', 'Energy Generation'] = model.F[i]()
    energy_planning.loc['EC_NET_1', 'Energy Generation'] = model.G[i]()
    energy_planning.loc['EC_NET_2', 'Energy Generation'] = model.H[i]()
    energy_planning.loc['EC_NET_3', 'Energy Generation'] = model.I[i]()
    energy_planning.loc['EP_NET_1', 'CI'] = model.NET_CI['EP_NETs_1'][i]
    energy_planning.loc['EP_NET_2', 'CI'] = model.NET_CI['EP_NETs_2'][i]
    energy_planning.loc['EP_NET_3', 'CI'] = model.NET_CI['EP_NETs_3'][i]
    energy_planning.loc['EC_NET_1', 'CI'] = model.NET_CI['EC_NETs_1'][i]
    energy_planning.loc['EC_NET_2', 'CI'] = model.NET_CI['EC_NETs_2'][i]
    energy_planning.loc['EC_NET_3', 'CI'] = model.NET_CI['EC_NETs_3'][i]        
    energy_planning.loc['EP_NET_1', 'Net Energy'] = round(model.EP_NET_1[i](), 2)
    energy_planning.loc['EP_NET_2', 'Net Energy'] = round(model.EP_NET_2[i](), 2)
    energy_planning.loc['EP_NET_3', 'Net Energy'] = round(model.EP_NET_3[i](), 2)
    energy_planning.loc['EC_NET_1', 'Net Energy'] = round(model.EC_NET_1[i](), 2)
    energy_planning.loc['EC_NET_2', 'Net Energy'] = round(model.EC_NET_2[i](), 2)
    energy_planning.loc['EC_NET_3', 'Net Energy'] = round(model.EC_NET_3[i](), 2)
    energy_planning.loc['EP_NET_1', 'Carbon Load'] = round(model.EP_NET_1[i]() * model.NET_CI['EP_NETs_1'][i], 2)
    energy_planning.loc['EP_NET_2', 'Carbon Load'] = round(model.EP_NET_2[i]() * model.NET_CI['EP_NETs_2'][i], 2)
    energy_planning.loc['EP_NET_3', 'Carbon Load'] = round(model.EP_NET_3[i]() * model.NET_CI['EP_NETs_3'][i], 2)
    energy_planning.loc['EC_NET_1', 'Carbon Load'] = round(model.EC_NET_1[i]() * model.NET_CI['EC_NETs_1'][i], 2)
    energy_planning.loc['EC_NET_2', 'Carbon Load'] = round(model.EC_NET_2[i]() * model.NET_CI['EC_NETs_2'][i], 2)
    energy_planning.loc['EC_NET_3', 'Carbon Load'] = round(model.EC_NET_3[i]() * model.NET_CI['EC_NETs_3'][i], 2)
    energy_planning.loc['COMP_SOLAR', 'Fuel'] = 'COMP_SOLAR'  
    energy_planning.loc['COMP_HYDRO', 'Fuel'] = 'COMP_HYDRO'
    energy_planning.loc['COMP_BIOMASS', 'Fuel'] = 'COMP_BIOMASS'  
    energy_planning.loc['COMP_BIOGAS', 'Fuel'] = 'COMP_BIOGAS'
    energy_planning.loc['COMP_MSW', 'Fuel'] = 'COMP_MSW'
    energy_planning.loc['COMP_SOLAR', 'Energy Generation'] = model.J[i]() 
    energy_planning.loc['COMP_HYDRO', 'Energy Generation'] = model.K[i]() 
    energy_planning.loc['COMP_BIOMASS', 'Energy Generation'] = model.L[i]() 
    energy_planning.loc['COMP_BIOGAS', 'Energy Generation'] = model.M[i]() 
    energy_planning.loc['COMP_MSW', 'Energy Generation'] = model.N[i]() 
    energy_planning.loc['COMP_SOLAR', 'CI'] = model.COMP_CI['SOLAR'][i]  
    energy_planning.loc['COMP_HYDRO', 'CI'] = model.COMP_CI['HYDRO'][i]
    energy_planning.loc['COMP_BIOMASS', 'CI'] = model.COMP_CI['BIOMASS'][i]  
    energy_planning.loc['COMP_BIOGAS', 'CI'] = model.COMP_CI['BIOGAS'][i]
    energy_planning.loc['COMP_MSW', 'CI'] = model.COMP_CI['MSW'][i]
    energy_planning.loc['COMP_SOLAR', 'Net Energy'] = round(model.comp_SOLAR[i](),2) 
    energy_planning.loc['COMP_SOLAR', 'Carbon Load'] = round(model.comp_SOLAR[i]() * model.COMP_CI['SOLAR'][i], 2)
    energy_planning.loc['COMP_HYDRO', 'Net Energy'] = round(model.comp_HYDRO[i](),2) 
    energy_planning.loc['COMP_HYDRO', 'Carbon Load'] = round(model.comp_HYDRO[i]() * model.COMP_CI['HYDRO'][i], 2)
    energy_planning.loc['COMP_BIOMASS', 'Net Energy'] = round(model.comp_BM[i](),2) 
    energy_planning.loc['COMP_BIOMASS', 'Carbon Load'] = round(model.comp_BM[i]() * model.COMP_CI['BIOMASS'][i], 2)
    energy_planning.loc['COMP_BIOGAS', 'Net Energy'] = round(model.comp_BG[i](),2) 
    energy_planning.loc['COMP_BIOGAS', 'Carbon Load'] = round(model.comp_BG[i]() * model.COMP_CI['BIOGAS'][i], 2)
    energy_planning.loc['COMP_MSW', 'Net Energy'] = round(model.comp_MSW[i](),2) 
    energy_planning.loc['COMP_MSW', 'Carbon Load'] = round(model.comp_MSW[i]() * model.COMP_CI['MSW'][i], 2)
    energy_planning.loc['TOTAL', 'Carbon Load'] = round(model.new_emission[i](), 2)
    energy_planning.loc['TOTAL', 'Cost'] = round(model.sum_cost[i](), 2)
            
    writer = pd.ExcelWriter(file_name, engine = 'openpyxl', mode = 'a', if_sheet_exists = 'new')
    energy_planning.to_excel(writer, sheet_name = 'Results_Period_1')
    writer.save()
    
    return 
        

model = multiperiod_energy_planning(model, periods)


for i in list(range(1, numperiods,1)):
    multiperiod_energy_planning_results(model,i)

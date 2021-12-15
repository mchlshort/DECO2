'''
Created on 15th December 2021

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
import os
from openpyxl import load_workbook

cwd = os.getcwd()

file = r'Optimal_Decarbonisation_User_Interface_7.xlsx'
plant_data = pd.read_excel(file, sheet_name = 'PLANT_DATA', index_col = 0, header = 30, nrows = 5).to_dict()
EP_data = pd.read_excel(file, sheet_name = 'EP_DATA', header = 21)
EG_data = pd.read_excel(file, sheet_name = 'ENERGY_DATA', header = 12)
CPX_data_1 = pd.read_excel(file, sheet_name = 'CAPEX_DATA_1', header = 20)
CPX_data_2 = pd.read_excel(file, sheet_name = 'CAPEX_DATA_2', header = 20)
SLD_data = pd.read_excel(file, sheet_name = 'ALT_SOLID', header = 8)
GAS_data = pd.read_excel(file, sheet_name = 'ALT_GAS', header = 8)
CCS_data = pd.read_excel(file, sheet_name = 'CCS_DATA', header = 12)
CI_NET_data = pd.read_excel(file, sheet_name = 'CI_NET_DATA', header = 12)
Cost_NET_data = pd.read_excel(file, sheet_name = 'COST_NET_DATA', header = 12)

s = plant_data.keys()

wb = load_workbook(file)
sheet = wb['PLANT_DATA']
flag = sheet['B28'].value
sheet_2 = wb['CAPEX_DATA_1']
AFF = sheet_2['B18'].value

#Period number
prd = list(EP_data['Period'])

#Energy demand for each period
Demand = list(EP_data['Energy Demand'])

#Emission limit for each period
Limit = list(EP_data['Emission Limit'])

#Budget allocation for each period
Budget = list(EP_data['Budget'])

#Carbon intensity of solar compensatory energy
CI_Comp_SOLAR = list(EP_data['CI_SOLAR'])

#Cost of solar compensatory energy
Cost_Comp_SOLAR = list(EP_data['COST_SOLAR'])

#Carbon intensity of hydro compensatory energy
CI_Comp_HYDRO = list(EP_data['CI_HYDRO'])

#Cost of hydro compensatory energy
Cost_Comp_HYDRO = list(EP_data['COST_HYDRO'])

#Carbon intensity of biomass compensatory energy
CI_Comp_BM = list(EP_data['CI_BIOMASS'])

#Cost of biomass compensatory energy
Cost_Comp_BM = list(EP_data['COST_BIOMASS'])

#Carbon intensity of biogas compensatory energy
CI_Comp_BG = list(EP_data['CI_BIOGAS'])

#Cost of biogas compensatory energy
Cost_Comp_BG = list(EP_data['COST_BIOGAS'])

#Carbon intensity of MSW compensatory energy
CI_Comp_MSW = list(EP_data['CI_MSW'])

#Cost of MSW compensatory energy
Cost_Comp_MSW = list(EP_data['COST_MSW'])

#Cost of natural gas fuel for power plants
Cost_NG = list(EG_data['NG'])

#Cost of oil fuel for power plants
Cost_OIL = list(EG_data['OIL'])

#Cost of coal fuel for power plants
Cost_COAL = list(EG_data['COAL'])

#Cost of solar as energy source for power generation
Cost_SOLAR = list(EG_data['SOLAR'])

#Cost of hydro as energy source for power generation
Cost_HYDRO = list(EG_data['HYDRO'])

#Cost of biogas as energy source for power generation
Cost_BIOGAS = list(EG_data['BIOGAS'])

#Cost of biomass as energy source for power generation
Cost_BIOMASS = list(EG_data['BIOMASS'])

#Cost of MSW as energy source for power generation
Cost_MSW = list(EG_data['MSW'])

#Capital cost of natural gas power plant (fixed cost)
CPX_NG_1 = list(CPX_data_1['NG'])

#Capital cost of oil power plant (fixed cost)
CPX_OIL_1 = list(CPX_data_1['OIL'])

#Capital cost of coal power plant (fixed cost)
CPX_COAL_1 = list(CPX_data_1['COAL'])

#Capital cost of solar power plant (fixed cost)
CPX_SOLAR_1 = list(CPX_data_1['SOLAR'])

#Capital cost of hydro power plant (fixed cost)
CPX_HYDRO_1 = list(CPX_data_1['HYDRO'])

#Capital cost of biogas power plant (fixed cost)
CPX_BIOGAS_1 = list(CPX_data_1['BIOGAS'])

#Capital cost of biomass power plant (fixed cost)
CPX_BIOMASS_1 = list(CPX_data_1['BIOMASS'])

#Capital cost of MSW power plant (fixed cost)
CPX_MSW_1 = list(CPX_data_1['MSW'])

#Capital cost of EP-NETs technology 1 power plant (fixed cost)
CPX_EP_NETs1_1 = list(CPX_data_1['EP-NETs_1'])

#Capital cost of EP-NETs technology 2 power plant (fixed cost)
CPX_EP_NETs2_1 = list(CPX_data_1['EP-NETs_2'])

#Capital cost of EP-NETs technology 3 power plant (fixed cost)
CPX_EP_NETs3_1 = list(CPX_data_1['EP-NETs_3'])

#Capital cost of EC-NETs technology 1 power plant (fixed cost)
CPX_EC_NETs1_1 = list(CPX_data_1['EC-NETs_1'])

#Capital cost of EC-NETs technology 2 power plant (fixed cost)
CPX_EC_NETs2_1 = list(CPX_data_1['EC-NETs_2'])

#Capital cost of EC-NETs technology 3 power plant (fixed cost)
CPX_EC_NETs3_1 = list(CPX_data_1['EC-NETs_3'])

#Capital cost of natural gas power plant (capacity cost)
CPX_NG_2 = list(CPX_data_2['NG'])

#Capital cost of oil power plant (capacity cost)
CPX_OIL_2 = list(CPX_data_2['OIL'])

#Capital cost of coal power plant (capacity cost)
CPX_COAL_2 = list(CPX_data_2['COAL'])

#Capital cost of solar power plant (capacity cost)
CPX_SOLAR_2 = list(CPX_data_2['SOLAR'])

#Capital cost of hydro power plant (capacity cost)
CPX_HYDRO_2 = list(CPX_data_2['HYDRO'])

#Capital cost of biogas power plant (capacity cost)
CPX_BIOGAS_2 = list(CPX_data_2['BIOGAS'])

#Capital cost of biomass power plant (capacity cost)
CPX_BIOMASS_2 = list(CPX_data_2['BIOMASS'])

#Capital cost of MSW power plant (capacity cost)
CPX_MSW_2 = list(CPX_data_2['MSW'])

#Capital cost of EP-NETs technology 1 power plant (capacity cost)
CPX_EP_NETs1_2 = list(CPX_data_2['EP-NETs_1'])

#Capital cost of EP-NETs technology 2 power plant (capacity cost)
CPX_EP_NETs2_2 = list(CPX_data_2['EP-NETs_2'])

#Capital cost of EP-NETs technology 3 power plant (capacity cost)
CPX_EP_NETs3_2 = list(CPX_data_2['EP-NETs_3'])

#Capital cost of EC-NETs technology 1 power plant (capacity cost)
CPX_EC_NETs1_2 = list(CPX_data_2['EC-NETs_1'])

#Capital cost of EC-NETs technology 2 power plant (capacity cost)
CPX_EC_NETs2_2 = list(CPX_data_2['EC-NETs_2'])

#Capital cost of EC-NETs technology 3 power plant (capacity cost)
CPX_EC_NETs3_2 = list(CPX_data_2['EC-NETs_3'])

#Carbon intensity of alternative solid fuel type 1
CI_SLD_1 = list(SLD_data['CI_SOLID_1'])

#Cost of alternative solid fuel type 1
Cost_SLD_1 = list(SLD_data['COST_SOLID_1'])

#Carbon intensity of alternative solid fuel type 2
CI_SLD_2 = list(SLD_data['CI_SOLID_2'])

#Cost of alternative solid fuel type 2
Cost_SLD_2 = list(SLD_data['COST_SOLID_2'])

#Carbon intensity of alternative gas fuel type 1
CI_GAS_1 = list(GAS_data['CI_GAS_1'])

#Cost of alternative gas fuel type 1
Cost_GAS_1 = list(GAS_data['COST_GAS_1'])

#Carbon intensity of alternative gas fuel type 2
CI_GAS_2 = list(GAS_data['CI_GAS_2'])

#Cost of alternative gas fuel type 2
Cost_GAS_2 = list(GAS_data['COST_GAS_2'])

#Removal ratio of CCS technology 1
RR_1 = list(CCS_data['RR_1'])

#Parisitic power loss of CCS technology 1
X_1 = list(CCS_data['X_1'])

#Cost of CCS technology 1
Cost_CCS_1 = list(CCS_data['Cost_CCS_1'])

#Removal ratio of CCS technology 2
RR_2 = list(CCS_data['RR_2'])

#Parisitic power loss of CCS technology 2
X_2 = list(CCS_data['X_2'])

#Cost of CCS technology 2
Cost_CCS_2 = list(CCS_data['Cost_CCS_2'])

#Fixed cost of CCS technology 1
FX_Cost_CCS_1 = list(CCS_data['FX_Cost_CCS_1'])

#Fixed cost of CCS technology 2
FX_Cost_CCS_2 = list(CCS_data['FX_Cost_CCS_2'])

#Carbon intensity of EP-NETs technology 1
CI_EP_NET_1 = list(CI_NET_data['EP-NETs_1'])

#Carbon intensity of EP-NETs technology 2
CI_EP_NET_2 = list(CI_NET_data['EP-NETs_2'])

#Carbon intensity of EP-NETs technology 3
CI_EP_NET_3 = list(CI_NET_data['EP-NETs_3'])

#Cost of EP-NETs technology 1
Cost_EP_NET_1 = list(Cost_NET_data['EP-NETs_1'])

#Cost of EP-NETs technology 2
Cost_EP_NET_2 = list(Cost_NET_data['EP-NETs_2'])

#Cost of EP-NETs technology 3
Cost_EP_NET_3 = list(Cost_NET_data['EP-NETs_3'])

#Carbon intensity of EC-NETs technology 1
CI_EC_NET_1 = list(CI_NET_data['EC-NETs_1'])

#Carbon intensity of EC-NETs technology 2
CI_EC_NET_2 = list(CI_NET_data['EC-NETs_2'])

#Carbon intensity of EC-NETs technology 3
CI_EC_NET_3 = list(CI_NET_data['EC-NETs_3'])

#Cost of EC-NETs technology 1
Cost_EC_NET_1 = list(Cost_NET_data['EC-NETs_1'])

#Cost of EC-NETs technology 2
Cost_EC_NET_2 = list(Cost_NET_data['EC-NETs_2'])

#Cost of EC-NETs technology 3
Cost_EC_NET_3 = list(Cost_NET_data['EC-NETs_3'])

numperiods = len(prd) + 1
period_data_dict = {}

for (i,D,L,B,CISL,CCSL,CIHY,CCHY,CIBM,CCBM,CIBG,CCBG,CIMSW,CCMSW,CNG,CO,CCL,CSL,CHY,CBG,CBM,CMSW,CXNG1,CXO1,CXCL1,CXS1,CXH1,CXBM1,CXBG1,CXMSW1,CXEP11,CXEP21,CXEP31,CXEC11,CXEC21,CXEC31,CXNG2,CXO2,CXCL2,CXS2,CXH2,CXBM2,CXBG2,CXMSW2,CXEP12,CXEP22,CXEP32,CXEC12,CXEC22,CXEC32,SLDI1,SLDC1,SLDI2,SLDC2,GASI1,GASC1,GASI2,GASC2,RR1,X1,CCS1,RR2,X2,CCS2,FCCS1,FCCS2,EP1I,EP2I,EP3I,CEP1,CEP2,CEP3,EC1I,EC2I,EC3I,CEC1,CEC2,CEC3) in zip(prd, Demand, Limit, Budget, CI_Comp_SOLAR, Cost_Comp_SOLAR, CI_Comp_HYDRO, Cost_Comp_HYDRO, CI_Comp_BM, Cost_Comp_BM, CI_Comp_BG, Cost_Comp_BG, CI_Comp_MSW, Cost_Comp_MSW, Cost_NG, Cost_OIL, Cost_COAL, Cost_SOLAR, Cost_HYDRO, Cost_BIOGAS, Cost_BIOMASS, Cost_MSW, CPX_NG_1, CPX_OIL_1, CPX_COAL_1, CPX_SOLAR_1, CPX_HYDRO_1, CPX_BIOMASS_1, CPX_BIOGAS_1, CPX_MSW_1, CPX_EP_NETs1_1, CPX_EP_NETs2_1, CPX_EP_NETs3_1, CPX_EC_NETs1_1, CPX_EC_NETs2_1, CPX_EP_NETs3_1, CPX_NG_2, CPX_OIL_2, CPX_COAL_2, CPX_SOLAR_2, CPX_HYDRO_2, CPX_BIOMASS_2, CPX_BIOGAS_2, CPX_MSW_2, CPX_EP_NETs1_2, CPX_EP_NETs2_2, CPX_EP_NETs3_2, CPX_EC_NETs1_2, CPX_EC_NETs2_2, CPX_EC_NETs3_2, CI_SLD_1, Cost_SLD_1, CI_SLD_2, Cost_SLD_2, CI_GAS_1, Cost_GAS_1, CI_GAS_2, Cost_GAS_2, RR_1, X_1, Cost_CCS_1, RR_2, X_2, Cost_CCS_2, FX_Cost_CCS_1, FX_Cost_CCS_2, CI_EP_NET_1, CI_EP_NET_2, CI_EP_NET_3, Cost_EP_NET_1, Cost_EP_NET_2, Cost_EP_NET_3, CI_EC_NET_1, CI_EC_NET_2, CI_EC_NET_3, Cost_EC_NET_1, Cost_EC_NET_2, Cost_EC_NET_3):    
    period_data_dict[i]= {'Demand' : D, 
                          'Emission_Limit' : L,
			              'Budget'    : B,
			              'CI_Comp_SOLAR' : CISL,
                          'Cost_Comp_SOLAR' : CCSL,
                          'CI_Comp_HYDRO' : CIHY,
                          'Cost_Comp_HYDRO' : CCHY,
                          'CI_Comp_BM' : CIBM,
                          'Cost_Comp_BM' : CCBM,
                          'CI_Comp_BG' : CIBG,
                          'Cost_Comp_BG' : CCBG,
                          'CI_Comp_MSW' : CIMSW,
                          'Cost_Comp_MSW' : CCMSW,
                          'Cost_NG' : CNG,
                          'Cost_OIL' : CO,
                          'Cost_COAL' : CCL,
                          'Cost_SOLAR': CSL,
                          'Cost_HYDRO': CHY,
                          'Cost_BIOGAS': CBG,
                          'Cost_BIOMASS': CBM,
                          'Cost_MSW': CMSW,
                          'CPX_NG_1' : CXNG1,
                          'CPX_OIL_1' : CXO1,
                          'CPX_COAL_1' : CXCL1,
                          'CPX_SOLAR_1' : CXS1,
                          'CPX_HYDRO_1' : CXH1,
                          'CPX_BIOMASS_1' : CXBM1,
                          'CPX_BIOGAS_1' : CXBG1,
                          'CPX_MSW_1' : CXMSW1,
                          'CPX_EP_NETs1_1': CXEP11,
                          'CPX_EP_NETs2_1': CXEP21,
                          'CPX_EP_NETs3_1': CXEP31,
                          'CPX_EC_NETs1_1': CXEC11,
                          'CPX_EC_NETs2_1': CXEC21,
                          'CPX_EC_NETs3_1': CXEC31,
                          'CPX_NG_2' : CXNG2,
                          'CPX_OIL_2' : CXO2,
                          'CPX_COAL_2' : CXCL2,
                          'CPX_SOLAR_2' : CXS2,
                          'CPX_HYDRO_2' : CXH2,
                          'CPX_BIOMASS_2' : CXBM2,
                          'CPX_BIOGAS_2' : CXBG2,
                          'CPX_MSW_2' : CXMSW2,
                          'CPX_EP_NETs1_2': CXEP12,
                          'CPX_EP_NETs2_2': CXEP22,
                          'CPX_EP_NETs3_2': CXEP32,
                          'CPX_EC_NETs1_2': CXEC12,
                          'CPX_EC_NETs2_2': CXEC22,
                          'CPX_EC_NETs3_2': CXEC32,
                          'CI_SLD_1' : SLDI1,
                          'Cost_SLD_1': SLDC1,
                          'CI_SLD_2' : SLDI2,
                          'Cost_SLD_2': SLDC2,
                          'CI_GAS_1' : GASI1,
                          'Cost_GAS_1': GASC1,
                          'CI_GAS_2' : GASI2,
                          'Cost_GAS_2': GASC2,
			              'RR_1' : RR1,
			              'X_1' : X1,
			              'Cost_CCS_1' : CCS1,
			              'RR_2' : RR2,
			              'X_2' : X2,
			              'Cost_CCS_2' : CCS2,
			              'FX_Cost_CCS_1' : FCCS1,
			              'FX_Cost_CCS_2' : FCCS2,
                          'CI_EP_NET_1' : EP1I,
                          'CI_EP_NET_2' : EP2I,
                          'CI_EP_NET_3' : EP3I,
                          'Cost_EP_NET_1' : CEP1,
                          'Cost_EP_NET_2' : CEP2,
                          'Cost_EP_NET_3' : CEP3,
                          'CI_EC_NET_1' : EC1I,
                          'CI_EC_NET_2' : EC2I,
                          'CI_EC_NET_3' : EC3I,
                          'Cost_EC_NET_1' : CEC1,
                          'Cost_EC_NET_2' : CEC2,
                          'Cost_EC_NET_3' : CEC3}
    
def EP_Period(plant_data,period_data): 
    model = pyo.ConcreteModel()
    model.S = plant_data.keys()
    model.plant_data = plant_data
    model.period_data = period_data
       
    #LIST OF VARIABLES
    
    #This variable determines the deployment of energy sources in power plant s
    model.energy = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the carbon intensity of energy sources in power plant s with CCS technology 1
    model.CI_RET_1 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the carbon intensity of energy sources in power plant s with CCS technology 2
    model.CI_RET_2 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #Binary variable for power generation by power plant s
    model.A = pyo.Var(model.S, domain = pyo.Binary)
    
    #Binary variable for the deployment of CCS technology 1 in power plant s
    model.B = pyo.Var(model.S, domain = pyo.Binary)
    
    #Binary variable for the deployment of CCS technology 2 in power plant s
    model.C = pyo.Var(model.S, domain = pyo.Binary)
    
    #Binary variable for the deployment of EP-NETs technology 1 
    model.D = pyo.Var(domain = pyo.Binary)
    
    #Binary variable for the deployment of EP-NETs technology 2
    model.E = pyo.Var(domain = pyo.Binary)
    
    #Binary variable for the deployment of EP-NETs technology 3 
    model.F = pyo.Var(domain = pyo.Binary)
    
    #Binary variable for the deployment of EC-NETs technology 1 
    model.G = pyo.Var(domain = pyo.Binary)
    
    #Binary variable for the deployment of EC-NETs technology 2 
    model.H = pyo.Var(domain = pyo.Binary)
    
    #Binary variable for the deployment of EC-NETs technology 3 
    model.I = pyo.Var(domain = pyo.Binary)
    
    #Binary variable for the deployment of solar compensatory energy 
    model.J = pyo.Var(domain = pyo.Binary)
    
    #Binary variable for the deployment of hydro compensatory energy 
    model.K = pyo.Var(domain = pyo.Binary)
    
    #Binary variable for the deployment of biomass compensatory energy 
    model.L = pyo.Var(domain = pyo.Binary)
    
    #Binary variable for the deployment of biogas compensatory energy 
    model.M = pyo.Var(domain = pyo.Binary)
    
    #Binary variable for the deployment of MSW compensatory energy 
    model.N = pyo.Var(domain = pyo.Binary)      
    
    #This variable represents the total deployment of CCS technology 1 & 2 in power plant s
    model.CCS = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable represents the deployment of CCS technology 1 in power plant s
    model.CCS_1 = pyo.Var(model.S, domain = pyo.NonNegativeReals) 
    
    #This variable represents the deployment of CCS technology 2 in power plant s
    model.CCS_2 = pyo.Var(model.S, domain = pyo.NonNegativeReals) 
    
    #This variable determines the net energy available from power plant s without CCS deployment
    model.net_energy = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the net energy available from power plant s with CCS deployment
    model.net_energy_CCS = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the net energy available from power plant s with the deployment of CCS technology 1
    model.net_energy_CCS_1 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the net energy available from power plant s with the deployment of CCS technology 2
    model.net_energy_CCS_2 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of EP_NETs technology 1
    model.EP_NET_1 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of EP_NETs technology 2
    model.EP_NET_2 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of EP_NETs technology 3 
    model.EP_NET_3 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of EC_NETs technology 1 
    model.EC_NET_1 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of EC_NETs technology 2
    model.EC_NET_2 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable represents the minimum deployment of EC_NETs technology 3
    model.EC_NET_3 = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of solar compensatory energy
    model.comp_SOLAR = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of hydro compensatory energy
    model.comp_HYDRO = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of biomass compensatory energy
    model.comp_BM = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of biogas compensatory energy
    model.comp_BG = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of MSW compensatory energy
    model.comp_MSW = pyo.Var(domain = pyo.NonNegativeReals)

    #This variable determines the revised total CO2 emission
    model.new_emission = pyo.Var(domain = pyo.NonNegativeReals)

    #This variable determines the total energy cost
    model.energy_cost = pyo.Var(domain = pyo.NonNegativeReals)

    #This variable determines the total cost
    model.sum_cost = pyo.Var(domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of alternative solid fuel type 1 for coal-based plants
    model.solid_1 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of alternative solid fuel type 2 for coal-based plants
    model.solid_2 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of alternative gas fuel type 1 for natural gas-based plants
    model.gas_1 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
    #This variable determines the minimum deployment of alternative gas fuel type 2 for natural gas-based plants
    model.gas_2 = pyo.Var(model.S, domain = pyo.NonNegativeReals)
    
       
    #OBJECTIVE FUNCTION
    
    #For the minimum budget objective function, the total cost is minimised, subject to the satisfaction of the CO2 emission limit
    #For the minimum emission objective function, the total emission is minimised, subject to the available budgetary constraint
    if flag == 'min_budget':
        model.obj = pyo.Objective(expr = model.sum_cost, sense = pyo.minimize)
    else:
        model.obj = pyo.Objective(expr = model.new_emission, sense = pyo.minimize)
   
    #CONSTRAINTS
    
    #All constraint relevant to carbon-constrained energy planning are added
    model.cons = pyo.ConstraintList()

    #Prior to any energy planning, the total power generation from all power plants should satisfy the regional energy demand
    model.cons.add(sum(model.energy[s] for s in model.S) == model.period_data['Demand'])
    
    for s in model.S:
        #Calculation of carbon intensity of energy sources with CCS technology 1
        model.cons.add((model.plant_data[s]['CI'] * (1 - model.period_data['RR_1']) / (1 - model.period_data['X_1'])) == model.CI_RET_1[s])
        
        #Calculation of carbon intensity of energy sources with CCS technology 2
        model.cons.add((model.plant_data[s]['CI'] * (1 - model.period_data['RR_2']) / (1 - model.period_data['X_2'])) == model.CI_RET_2[s])
        
        #The deployment of energy source in power plant s should at least satisfy the lower bound
        model.cons.add(model.energy[s] >= model.plant_data[s]['LB'] * model.A[s])
        
        #The deployment of energy source in power plant s should at most satisfy the upper bound
        model.cons.add(model.energy[s] <= model.plant_data[s]['UB'] * model.A[s])
        
        #The total CCS deployment in power plant s should be equal to summation of deployment of individual types of  CCS technology
        model.cons.add(model.CCS_1[s] + model.CCS_2[s] ==  model.CCS[s])
    
        #The total CCS deployment should be limited to the energy generation of power plant s
        model.cons.add(model.CCS[s] <= model.energy[s])
        
        #Determine the net energy available from power plant s with CCS technology 1
        model.cons.add(model.CCS_1[s] * (1 - model.period_data['X_1']) == model.net_energy_CCS_1[s])
        
        #Determine the net energy available from power plant s with CCS technology 2
        model.cons.add(model.CCS_2[s] * (1 - model.period_data['X_2']) == model.net_energy_CCS_2[s])
        
	    #If selected, the deployment of CCS technology 1 in power plant s is limited by the upper bound of the energy output 
        model.cons.add(model.CCS_1[s] <= model.plant_data[s]['UB'] * model.B[s])

    	#If selected, the deployment of CCS technology 2 in power plant s is limited by the upper bound of the energy output
        model.cons.add(model.CCS_2[s] <= model.plant_data[s]['UB'] * model.C[s])        

    	#Determine the net energy available from power plant s with the deployment of CCS technologies 1 & 2
        model.cons.add(model.net_energy_CCS_1[s] + model.net_energy_CCS_2[s] == model.net_energy_CCS[s])
        
        #The total energy contribution must equal the initially determined energy contribution of power plant s
        if 'REN' in model.plant_data[s].values():
            model.cons.add(model.net_energy[s] == model.energy[s])
        elif 'NG' in model.plant_data[s].values():
            model.cons.add(model.net_energy[s] + model.CCS_1[s] + model.CCS_2[s] + model.gas_1[s] + model.gas_2[s] == model.energy[s])
        elif 'COAL' in model.plant_data[s].values():
            model.cons.add(model.net_energy[s] + model.CCS_1[s] + model.CCS_2[s] + model.solid_1[s] + model.solid_2[s] == model.energy[s])
        else:
            model.cons.add(model.net_energy[s] + model.CCS_1[s] + model.CCS_2[s] == model.energy[s])
    
        #If power plant s is fuelled by renewable energy sources, no CCS deployment will take place
        if 'REN' in model.plant_data[s].values():
            model.CCS_1[s].fix(0)
            model.CCS_2[s].fix(0)       
    
    #Big M formulation for EP-NETs technology 1 deployment
    model.cons.add(model.EP_NET_1 <= model.D * 1000) 
    
    #Big M formulation for EP-NETs technology 2 deployment
    model.cons.add(model.EP_NET_2 <= model.E * 1000) 
    
    #Big M formulation for EP-NETs technology 3 deployment
    model.cons.add(model.EP_NET_3 <= model.F * 1000) 
    
    #Big M formulation for EC-NETs technology 1 deployment
    model.cons.add(model.EC_NET_1 <= model.G * 1000)
    
    #Big M formulation for EC-NETs technology 2 deployment
    model.cons.add(model.EC_NET_2 <= model.H * 1000)
    
    #Big M formulation for EC-NETs technology 3 deployment
    model.cons.add(model.EC_NET_3 <= model.I * 1000)
    
    #Big M formulation for deployment of solar compensatory energy
    model.cons.add(model.comp_SOLAR <= model.J * 1000)
    
    #Big M formulation for deployment of hydro compensatory energy
    model.cons.add(model.comp_HYDRO <= model.K * 1000)
    
    #Big M formulation for deployment of BM compensatory energy
    model.cons.add(model.comp_BM <= model.L * 1000)
    
    #Big M formulation for deployment of BG compensatory energy
    model.cons.add(model.comp_BG <= model.M * 1000)
    
    #Big M formulation for deployment of MSW compensatory energy
    model.cons.add(model.comp_MSW <= model.N * 1000)
    
    #Total energy contribution from all energy sources to satisfy the total demand
    model.cons.add(sum(((model.net_energy[s]) + model.net_energy_CCS_1[s] + model.net_energy_CCS_2[s] + model.solid_1[s] + model.solid_2[s] + model.gas_1[s] + model.gas_2[s]) for s in model.S) + model.comp_SOLAR + model.comp_HYDRO + model.comp_BM + model.comp_BG + model.comp_MSW + model.EP_NET_1 + model.EP_NET_2 + model.EP_NET_3 == model.period_data['Demand'] + model.EC_NET_1 + model.EC_NET_2 + model.EC_NET_3) 
    
    #The total CO2 load contribution from all energy sources must satisfy most the CO2 emission limit
    model.cons.add(sum((model.net_energy[s] * model.plant_data[s]['CI']) + (model.net_energy_CCS_1[s] * model.CI_RET_1[s]) + (model.net_energy_CCS_2[s] * model.CI_RET_2[s]) + (model.solid_1[s] * model.period_data['CI_SLD_1']) + (model.solid_2[s] * model.period_data['CI_SLD_2']) + (model.gas_1[s] * model.period_data['CI_GAS_1']) + (model.gas_2[s] * model.period_data['CI_GAS_2']) for s in model.S)
               + (model.EC_NET_1 * model.period_data['CI_EC_NET_1'])
               + (model.EC_NET_2 * model.period_data['CI_EC_NET_2'])
               + (model.EC_NET_3 * model.period_data['CI_EC_NET_3'])
               + (model.EP_NET_1 * model.period_data['CI_EP_NET_1'])
               + (model.EP_NET_2 * model.period_data['CI_EP_NET_2'])
               + (model.EP_NET_3 * model.period_data['CI_EP_NET_3'])
               + (model.comp_SOLAR * model.period_data['CI_Comp_SOLAR'])
               + (model.comp_HYDRO * model.period_data['CI_Comp_HYDRO'])
               + (model.comp_BM * model.period_data['CI_Comp_BM'])
               + (model.comp_BG * model.period_data['CI_Comp_BG']) 
               + (model.comp_MSW * model.period_data['CI_Comp_MSW']) == model.new_emission)
    
    #Determining the cumulative total fuel and annualised capital cost for all power plants
    energy_cost = 0
    for s in model.S:
        if 'SOLAR' in model.plant_data[s].values():
            energy_cost = energy_cost + (model.net_energy[s] * model.period_data['Cost_SOLAR']) + (AFF * model.period_data['CPX_SOLAR_1'] * model.A[s]) + (AFF * model.energy[s] * model.period_data['CPX_SOLAR_2'])
        elif 'HYDRO' in model.plant_data[s].values():
            energy_cost = energy_cost + (model.net_energy[s] * model.period_data['Cost_HYDRO']) + (AFF * model.period_data['CPX_HYDRO_1'] * model.A[s]) + (AFF * model.energy[s] * model.period_data['CPX_HYDRO_2'])
        elif 'BIOGAS' in model.plant_data[s].values():
            energy_cost = energy_cost + (model.net_energy[s] * model.period_data['Cost_BIOGAS']) + (AFF * model.period_data['CPX_BIOGAS_1'] * model.A[s]) + (AFF * model.energy[s] * model.period_data['CPX_BIOGAS_2'])
        elif 'BIOMASS' in model.plant_data[s].values():
            energy_cost = energy_cost + (model.net_energy[s] * model.period_data['Cost_BIOMASS']) + (AFF * model.period_data['CPX_BIOMASS_1'] * model.A[s]) + (AFF * model.energy[s] * model.period_data['CPX_BIOMASS_2'])
        elif 'MSW' in model.plant_data[s].values():
            energy_cost = energy_cost + (model.net_energy[s] * model.period_data['Cost_MSW']) + (AFF * model.period_data['CPX_MSW_1'] * model.A[s]) + (AFF * model.energy[s] * model.period_data['CPX_MSW_2'])
        elif 'NG' in model.plant_data[s].values():
            energy_cost = energy_cost + (model.net_energy[s] * model.period_data['Cost_NG']) + (AFF * model.period_data['CPX_NG_1'] * model.A[s]) + (AFF * model.energy[s] * model.period_data['CPX_NG_2'])
        elif 'OIL' in model.plant_data[s].values():
            energy_cost = energy_cost + (model.net_energy[s] * model.period_data['Cost_OIL']) + (AFF * model.period_data['CPX_OIL_1'] * model.A[s]) + (AFF * model.energy[s] * model.period_data['CPX_OIL_2'])
        else:
            energy_cost = energy_cost + (model.net_energy[s] * model.period_data['Cost_COAL']) + (AFF * model.period_data['CPX_COAL_1'] * model.A[s]) + (AFF * model.energy[s] * model.period_data['CPX_COAL_2'])
            
    #The summation of cost for each power plant s should equal to the total cost of each period
    model.cons.add(sum((model.net_energy_CCS_1[s] * model.period_data['Cost_CCS_1']) + (model.net_energy_CCS_2[s] * model.period_data['Cost_CCS_2']) + (model.period_data['FX_Cost_CCS_1'] * model.B[s]) + (model.period_data['FX_Cost_CCS_2'] * model.C[s]) + (model.solid_1[s] * model.period_data['Cost_SLD_1']) + (model.solid_2[s] * model.period_data['Cost_SLD_2']) + (model.gas_1[s] * model.period_data['Cost_GAS_1']) + (model.gas_2[s] * model.period_data['Cost_GAS_2']) for s in model.S)
               + (model.EC_NET_1 * model.period_data['Cost_EC_NET_1']) + (AFF * model.period_data['CPX_EC_NETs1_1'] * model.G) + (AFF * model.EC_NET_1 * model.period_data['CPX_EC_NETs1_2'])
               + (model.EC_NET_2 * model.period_data['Cost_EC_NET_2']) + (AFF * model.period_data['CPX_EC_NETs2_1'] * model.H) + (AFF * model.EC_NET_2 * model.period_data['CPX_EC_NETs2_2'])
               + (model.EC_NET_3 * model.period_data['Cost_EC_NET_3']) + (AFF * model.period_data['CPX_EC_NETs3_1'] * model.I) + (AFF * model.EC_NET_3 * model.period_data['CPX_EC_NETs3_2'])
               + (model.EP_NET_1 * model.period_data['Cost_EP_NET_1']) + (AFF * model.period_data['CPX_EP_NETs1_1'] * model.D) + (AFF * model.EP_NET_1 * model.period_data['CPX_EP_NETs1_2'])
               + (model.EP_NET_2 * model.period_data['Cost_EP_NET_2']) + (AFF * model.period_data['CPX_EP_NETs2_1'] * model.E) + (AFF * model.EP_NET_2 * model.period_data['CPX_EP_NETs2_2'])
               + (model.EP_NET_3 * model.period_data['Cost_EP_NET_3']) + (AFF * model.period_data['CPX_EP_NETs3_1'] * model.F) + (AFF * model.EP_NET_3 * model.period_data['CPX_EP_NETs3_2'])
               + (model.comp_SOLAR * model.period_data['Cost_Comp_SOLAR']) + (AFF * model.period_data['CPX_SOLAR_1'] * model.J) + (AFF * model.comp_SOLAR * model.period_data['CPX_SOLAR_2'])
               + (model.comp_HYDRO * model.period_data['Cost_Comp_HYDRO']) + (AFF * model.period_data['CPX_HYDRO_1'] * model.K) + (AFF * model.comp_HYDRO * model.period_data['CPX_HYDRO_2'])
               + (model.comp_BM * model.period_data['Cost_Comp_BM']) + (AFF * model.period_data['CPX_BIOMASS_1'] * model.L) + (AFF * model.comp_BM * model.period_data['CPX_BIOMASS_2'])
               + (model.comp_BG * model.period_data['Cost_Comp_BG']) + (AFF * model.period_data['CPX_BIOGAS_1'] * model.M) + (AFF * model.comp_BG * model.period_data['CPX_BIOGAS_2'])
               + (model.comp_MSW * model.period_data['Cost_Comp_MSW']) + (AFF * model.period_data['CPX_MSW_1'] * model.N) + (AFF * model.comp_MSW * model.period_data['CPX_MSW_2'])
               + energy_cost == model.sum_cost) 
    
    #For the minimum budget objective function, the total cost is minimised, subject to the satisfaction of the CO2 emission limit
    #For the minimum emission objective function, the total emission is minimised, subject to the available budgetary constraint
    if flag == 'min_budget':
        model.cons.add(model.new_emission <= model.period_data['Emission_Limit'])
    else:
        model.cons.add(model.sum_cost <= model.period_data['Budget'])

    return model

#Creating a list with 3 strings
block_sets = list(range(1, numperiods, 1))

#Adding the models to a dictionary to be accessed inside the function
EP = dict()
for i in range(1, numperiods, 1):
    EP[block_sets[i-1]] = EP_Period(plant_data, period_data_dict[i])

#Specifying the class of the new model
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

#The deployment of CCS technology 1 at later periods should at least match the deployment in the previous period
def linking_blocks_1(model, block_sets, s):
    if block_sets == len(prd):
        return pyo.Constraint.Skip
    else:   
        return Full_model.subprobs[block_sets + 1].CCS_1[s] >=  Full_model.subprobs[block_sets].CCS_1[s]

#The deployment of CCS technology 2 at later periods should at least match the deployment in the previous period    
def linking_blocks_2(model, block_sets, s):
    if block_sets == len(prd):
        return pyo.Constraint.Skip
    else:   
        return Full_model.subprobs[block_sets + 1].CCS_2[s] >=  Full_model.subprobs[block_sets].CCS_2[s]
 
#If power plant s is decomissioned in a period, it should remain decommissioned at later periods 
def linking_blocks_3(model, block_sets, s):
    if block_sets == len(prd):
        return pyo.Constraint.Skip
    else:   
        return Full_model.subprobs[block_sets + 1].energy[s] >=  Full_model.subprobs[block_sets].energy[s]

#Adding the constraints to the model        
Full_model.Cons1 = pyo.Constraint(block_sets, s, rule = linking_blocks_1)
Full_model.Cons2 = pyo.Constraint(block_sets, s, rule = linking_blocks_2)
Full_model.Cons3 = pyo.Constraint(block_sets, s, rule = linking_blocks_3)

'''
Creating a new objective function for the new model
The objective minimises the cumulative extent of CCS retrofit from all fossil-based sources
'''

#Speciying the variable to be minimised subject to the choice of objective function
TCOST = 0
TEMIS = 0
for i in range(1, numperiods, 1):
    TCOST = TCOST + Full_model.subprobs[i].sum_cost
    TEMIS = TEMIS + Full_model.subprobs[i].new_emission

#For the minimum budget objective function, the total cost is minimised, subject to the satisfaction of the CO2 emission limit
#For the minimum emission objective function, the total emission is minimised, subject to the available budgetary constraint    
if flag == 'min_budget':
    Full_model.obj = pyo.Objective(expr = TCOST, sense = pyo.minimize)
else:
    Full_model.obj = pyo.Objective(expr = TEMIS, sense = pyo.minimize)

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
    
    energy_planning = pd.DataFrame()

    for s in plant_data.keys():
        energy_planning.loc[s, 'Fuel'] = plant_data[s]['Fuel']
        energy_planning.loc[s, 'Energy Generation'] = model.A[s]()
        energy_planning.loc[s, 'Energy'] = round(model.energy[s](), 2)
        energy_planning.loc[s, 'CI'] = plant_data[s]['CI']
        energy_planning.loc[s, 'CCS_1 CI'] = round(model.CI_RET_1[s](), 3)
        energy_planning.loc[s, 'CCS_2 CI'] = round(model.CI_RET_2[s](), 3)
        energy_planning.loc[s, 'CCS_1 Selection'] = model.B[s]()
        energy_planning.loc[s, 'CCS_2 Selection'] = model.C[s]()
        energy_planning.loc[s, 'CCS_1 Ret'] = round(model.CCS_1[s](), 2) 
        energy_planning.loc[s, 'CCS_2 Ret'] = round(model.CCS_2[s](), 2)       
        energy_planning.loc[s, 'Net Energy wo CCS'] = round(model.net_energy[s](), 2)
        energy_planning.loc[s, 'Net Energy w CCS_1'] = round(model.net_energy_CCS_1[s](), 2)
        energy_planning.loc[s, 'Net Energy w CCS_2'] = round(model.net_energy_CCS_2[s](), 2)
        energy_planning.loc[s, 'SOLID_1'] = round(model.solid_1[s](), 2)
        energy_planning.loc[s, 'SOLID_2'] = round(model.solid_2[s](), 2)
        energy_planning.loc[s, 'GAS_1'] = round(model.gas_1[s](), 2)
        energy_planning.loc[s, 'GAS_2'] = round(model.gas_2[s](), 2)
        energy_planning.loc[s, 'Net Energy'] = round(model.net_energy[s]() + model.net_energy_CCS[s](), 2)
        energy_planning.loc[s, 'Carbon Load'] = round((model.net_energy[s]() * plant_data[s]['CI']) + (model.net_energy_CCS_1[s]() * model.CI_RET_1[s]()) + (model.net_energy_CCS_2[s]() * model.CI_RET_2[s]()), 2)
        
    energy_planning.loc['EP_NET_1', 'Fuel'] = 'EP_NET_1'
    energy_planning.loc['EP_NET_2', 'Fuel'] = 'EP_NET_2'
    energy_planning.loc['EP_NET_3', 'Fuel'] = 'EP_NET_3'
    energy_planning.loc['EC_NET_1', 'Fuel'] = 'EC_NET_1'
    energy_planning.loc['EC_NET_2', 'Fuel'] = 'EC_NET_2' 
    energy_planning.loc['EC_NET_3', 'Fuel'] = 'EC_NET_3' 
    energy_planning.loc['EP_NET_1', 'Energy Generation'] = model.D()
    energy_planning.loc['EP_NET_2', 'Energy Generation'] = model.E()
    energy_planning.loc['EP_NET_3', 'Energy Generation'] = model.F()
    energy_planning.loc['EC_NET_1', 'Energy Generation'] = model.G()
    energy_planning.loc['EC_NET_2', 'Energy Generation'] = model.H()
    energy_planning.loc['EC_NET_3', 'Energy Generation'] = model.I()
    energy_planning.loc['EP_NET_1', 'CI'] = model.period_data['CI_EP_NET_1']
    energy_planning.loc['EP_NET_2', 'CI'] = model.period_data['CI_EP_NET_2']
    energy_planning.loc['EP_NET_3', 'CI'] = model.period_data['CI_EP_NET_3']
    energy_planning.loc['EC_NET_1', 'CI'] = model.period_data['CI_EC_NET_1']
    energy_planning.loc['EC_NET_2', 'CI'] = model.period_data['CI_EC_NET_2'] 
    energy_planning.loc['EC_NET_3', 'CI'] = model.period_data['CI_EC_NET_3']        
    energy_planning.loc['EP_NET_1', 'Net Energy'] = round(model.EP_NET_1(), 2)
    energy_planning.loc['EP_NET_2', 'Net Energy'] = round(model.EP_NET_2(), 2)
    energy_planning.loc['EP_NET_3', 'Net Energy'] = round(model.EP_NET_3(), 2)
    energy_planning.loc['EC_NET_1', 'Net Energy'] = round(model.EC_NET_1(), 2)
    energy_planning.loc['EC_NET_2', 'Net Energy'] = round(model.EC_NET_2(), 2)
    energy_planning.loc['EC_NET_3', 'Net Energy'] = round(model.EC_NET_3(), 2)
    energy_planning.loc['EP_NET_1', 'Carbon Load'] = round(model.EP_NET_1() * model.period_data['CI_EP_NET_1'], 2)
    energy_planning.loc['EP_NET_2', 'Carbon Load'] = round(model.EP_NET_2() * model.period_data['CI_EP_NET_2'], 2)
    energy_planning.loc['EP_NET_3', 'Carbon Load'] = round(model.EP_NET_3() * model.period_data['CI_EP_NET_3'], 2)
    energy_planning.loc['EC_NET_1', 'Carbon Load'] = round(model.EC_NET_1() * model.period_data['CI_EC_NET_1'], 2)
    energy_planning.loc['EC_NET_2', 'Carbon Load'] = round(model.EC_NET_2() * model.period_data['CI_EC_NET_2'], 2)
    energy_planning.loc['EC_NET_3', 'Carbon Load'] = round(model.EC_NET_3() * model.period_data['CI_EC_NET_3'], 2)
    energy_planning.loc['COMP_SOLAR', 'Fuel'] = 'COMP_SOLAR'  
    energy_planning.loc['COMP_HYDRO', 'Fuel'] = 'COMP_HYDRO'
    energy_planning.loc['COMP_BIOMASS', 'Fuel'] = 'COMP_BIOMASS'  
    energy_planning.loc['COMP_BIOGAS', 'Fuel'] = 'COMP_BIOGAS'
    energy_planning.loc['COMP_MSW', 'Fuel'] = 'COMP_MSW'
    energy_planning.loc['COMP_SOLAR', 'Energy Generation'] = model.J() 
    energy_planning.loc['COMP_HYDRO', 'Energy Generation'] = model.K() 
    energy_planning.loc['COMP_BIOMASS', 'Energy Generation'] = model.L() 
    energy_planning.loc['COMP_BIOGAS', 'Energy Generation'] = model.M() 
    energy_planning.loc['COMP_MSW', 'Energy Generation'] = model.N() 
    energy_planning.loc['COMP_SOLAR', 'CI'] = model.period_data['CI_Comp_SOLAR']  
    energy_planning.loc['COMP_HYDRO', 'CI'] = model.period_data['CI_Comp_HYDRO']
    energy_planning.loc['COMP_BIOMASS', 'CI'] = model.period_data['CI_Comp_BM']  
    energy_planning.loc['COMP_BIOGAS', 'CI'] = model.period_data['CI_Comp_BG']
    energy_planning.loc['COMP_MSW', 'CI'] = model.period_data['CI_Comp_MSW']
    energy_planning.loc['COMP_SOLAR', 'Net Energy'] = round(model.comp_SOLAR(),2) 
    energy_planning.loc['COMP_SOLAR', 'Carbon Load'] = round(model.comp_SOLAR() * model.period_data['CI_Comp_SOLAR'], 2)
    energy_planning.loc['COMP_HYDRO', 'Net Energy'] = round(model.comp_HYDRO(),2) 
    energy_planning.loc['COMP_HYDRO', 'Carbon Load'] = round(model.comp_HYDRO() * model.period_data['CI_Comp_HYDRO'], 2)
    energy_planning.loc['COMP_BIOMASS', 'Net Energy'] = round(model.comp_BM(),2) 
    energy_planning.loc['COMP_BIOMASS', 'Carbon Load'] = round(model.comp_BM() * model.period_data['CI_Comp_BM'], 2)
    energy_planning.loc['COMP_BIOGAS', 'Net Energy'] = round(model.comp_BG(),2) 
    energy_planning.loc['COMP_BIOGAS', 'Carbon Load'] = round(model.comp_BG() * model.period_data['CI_Comp_BG'], 2)
    energy_planning.loc['COMP_MSW', 'Net Energy'] = round(model.comp_MSW(),2) 
    energy_planning.loc['COMP_MSW', 'Carbon Load'] = round(model.comp_MSW() * model.period_data['CI_Comp_MSW'], 2)
    energy_planning.loc['TOTAL', 'Carbon Load'] = round(model.new_emission(), 2)
    energy_planning.loc['TOTAL', 'Cost'] = round(model.sum_cost(), 2)
    
    writer = pd.ExcelWriter(file, engine = 'openpyxl', mode = 'a')
    energy_planning.to_excel(writer, sheet_name = 'Results_Period_1')
    writer.save()
    
    return    

for i in range (1, numperiods,1):
    EP_Results(plant_data, period_data_dict[i], i)

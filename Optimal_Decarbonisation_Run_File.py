'''
Created on 24th September 2021

This script presents the mathematical optimisation formulation for an energy planning scenario in a specific geographical region or district.
Renewable energy and fossil-based sources make up the power generation in a specific geographical region or district. 
Each period consists of its respective energy demand and CO2 emission limit.
EP-NETs and EC-NETs may be utilised to achieve the CO2 emission limit for each period.
This energy planning mathematical formulation may be optimised subject to either a mininum cost or minimum emission objective function.

@author: Purusothmn, Dr Michael Short, Prof Dr Dominic C.Y.F.
'''
import os 

path = os.chdir(r'COPY_PATHNAME_ AND_REPLACE_THIS_TEXT') 

cwd = os.getcwd()

import Optimal_Decarbonisation_Model_Python
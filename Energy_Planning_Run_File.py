'''
Created on 4th August 2021

This script presents the mathematical optimisation formulation for an energy planning scenario in a specific geographical region or district.
Renewable energy and fossil-based sources make up the power generation in a specific geographical region or district. 
Each period consists of its respective energy demand and CO2 emission limit.
EP-NETs and EC-NETs may be utilised to achieve the CO2 emission limit for each period.
This energy planning mathematical formulation may be optimised subject to either a mininum cost or minimum emission objective function.

@author: Purusothmn, Dr Michael Short, Prof Dr Dominic C.Y.F.
'''
import os 
'''
The user would be required to alter the directory name according to one's requirement
'''
path = os.chdir(r'C:/Users/LENOVO/OneDrive - University of Nottingham Malaysia/The University of Nottingham/BC COP26 Trilateral Research Initiative/BCCOP26TrilateralProject') 

cwd = os.getcwd()

import Energy_Planning_Model_Python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 17:20:28 2026

@author: dalaislydon
"""
# Importing tools
import pandas as pd
import matplotlib.pyplot as plt

# Reading in data set and creating dataframes
CTD= pd.read_csv('CTD_data.dat', sep='\t')
Temp= CTD['Temperature(degrees Celsius)']
Salinity=CTD['Salinity(psu)']
Depth= CTD['Depth(m)']

# Temperature profile
fig, ax = plt.subplots(1,2, sharey= True)
ax[0].plot(Temp, Depth, color='r' )
ax[0].set_xlabel('Temperature (degrees Celsius)')
ax[0].set_ylabel('Depth (m)')
ax[0].set_title('Temperature profile')

# Salinity profile
ax[1].plot(Salinity, Depth, color='b')
ax[1].set_xlabel('Salinity (psu)')
ax[1].set_title('Salinity profile')

# inverts axis
ax[0].invert_yaxis()

# saves figure
fig.savefig('Temperature and Salinity profiles.png')

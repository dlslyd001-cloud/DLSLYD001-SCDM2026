#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 19:59:16 2026

@author: dalaislydon
"""
# Importing tools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("SAA2_WC_2017_metocean_10min_avg.csv", na_values=['NULL'])

# Convert TIME_SERVER to datetime
df['Datetime'] = pd.to_datetime(df['TIME_SERVER'], format='%Y/%m/%d %H:%M')

# Set as index and sort
df.set_index('Datetime', inplace=True)
df = df.sort_index()

df_time = df.loc['2017-06-28':'2017-07-04']

# Plotting time series of temperature
plt.style.use('grayscale')
fig1, ax1 = plt.subplots(figsize=(12,5))
ax1.plot(df_time.index, df_time['TSG_TEMP'])

ax1.set_xlabel('Date')
ax1.set_ylabel('Temperature (degrees C)')
ax1.set_title('Temperature time series')
fig1.savefig('Temperature time series.png')

# Plotting histogram of salinity distribution
bins= np.arange(30, 35, 0.5)
fig2, ax2= plt.subplots()
plt.style.use('default')
ax2.hist(df_time['TSG_SALINITY'], bins=bins)
ax2.set_xlabel('Salinity')
ax2.set_ylabel('Frequency')
ax2.set_title('Salinity distribution in the Southern Ocean')
fig2.savefig('Salinity distribution in the Southern Ocean.png')

# Table for the mean, standard deviation and the interquartile range for
# temperature and salinity
table_data= pd.DataFrame({
    'Mean': df_time[['TSG_TEMP', 'TSG_SALINITY']].mean(),
    'Standard deviation': df_time[['TSG_TEMP', 'TSG_SALINITY']].std(),
    'IQR': df_time[['TSG_TEMP','TSG_SALINITY']].quantile(0.75) - 
    df_time[['TSG_TEMP', 'TSG_SALINITY']].quantile(0.25)})

print("\nStatistics Table")
print(table_data)

# Scatter plot of wind speed and air temperature
def ddmm2dd(ddmm):
    """
    Converts a position input from degrees and minutes to decimal degrees
    Input is ddmm.cccc and output is dd.cccc
    Note: it does not check if positive or negative
    """
    thedeg = np.floor(ddmm/100.)
    themin = (ddmm - thedeg*100.)/60.
    return thedeg + themin

df_time.loc[:,'LATITUDE'] = ddmm2dd(df_time["LATITUDE"])   # changes the latitude to
#have decimals instead of minutes

plt.style.use('bmh')
fig3, ax3 = plt.subplots()
scatter= plt.scatter(df_time['WIND_SPEED_TRUE'], df_time['AIR_TEMPERATURE'],
            c= df_time['LATITUDE'])
ax3.set_xlabel('Wind speed (m/s)')
ax3.set_ylabel('Air temperature (degrees C)')
plt.colorbar(scatter, label= 'Latitude (degrees and decimals)')
ax3.set_title('Wind speed vs air temperature across varying latitudes')
fig3.savefig('Wind speed vs air temperature across varying latitudes.png',
            dpi=300)





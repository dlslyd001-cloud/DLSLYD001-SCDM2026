#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 13:12:49 2026

@author: dalaislydon
"""

# Importing in all packages
import cartopy.crs as ccrs
import cartopy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import cartopy.feature as cfeature
# %%
#  Looking at Antarctica and the surrounding Southern Ocean

# Axes and figure
plt.figure()
ax = plt.axes(projection=ccrs.SouthPolarStereo())      

# Extent of Antarctica and the Southern Ocean
extent = [-180, 180, -90, -60]             
ax.set_extent(extent, crs=ccrs.PlateCarree())           

# Labels and their placements
gl= ax.gridlines(draw_labels=True, alpha=0.9)  
gl.right_labels= False
gl.top_labels= True

# Adding features
ax.coastlines(resolution='110m')                     
ax.add_feature(cartopy.feature.LAND)
ax.add_feature(cartopy.feature.OCEAN, facecolor='lightblue')
ax.stock_img()
plt.title('Antarctica and the surrounding Southern Ocean')

plt.show()
# %%
# Figure and axes
plt.figure(figsize=(10,6))
ax = plt.axes(projection=ccrs.PlateCarree())

# Extent of the South Atlantic region countaining the coastal cities
extent = [-60,30, -50, -20]
ax.set_extent(extent, crs=ccrs.PlateCarree())

# Gridlines
gl= ax.gridlines(draw_labels=True, linestyle='--', alpha=0.6)
gl.right_labels = False
gl.top_labels= False
gl.xlabel_style = {'size':8}
gl.ylabel_style = {'size':8}

# Locations
geolocator= Nominatim(user_agent='map')
place = ['Cape Town', 'Walvis Bay', 'Rio de Janeiro', 'Montevideo']
address =[]
for p in place:
    loc = geolocator.geocode(p, language='en')
    address.append(loc)
print(address)

# For loop used to plot each location and their appropriate labelling
for p in range(len(place)):
    ax.plot(address[p].longitude, address[p].latitude,
        marker='o', color='red', markersize=4,
        transform=ccrs.PlateCarree())
    
    ax.text(address[p].longitude + 0.5, address[p].latitude -1.5, 
            place[p], 
            transform=ccrs.Geodetic(), 
            fontsize=7,
            bbox=dict(facecolor='white', alpha=0.7, pad=1),
            )
    
# Features
ax.coastlines(resolution='10m')
ax.add_feature(cartopy.feature.LAND,  facecolor='lightgray')
ax.add_feature(cartopy.feature.OCEAN, facecolor='lightblue')
ax.add_feature(cartopy.feature.BORDERS, linewidth=0.5)
plt.title('Cities on the coasts of the South Atlantic Ocean')

plt.show()
# %%
# Extent of False Bay
extent = [18.2, 19.0, -34.5, -34.0]

# Resolutions and titles for each plot
resolutions = ['c', 'i', 'f']  # crude, intermediate, full
titles = ['Crude', 'Intermediate', 'Full']

# 3 figures and their axes
fig, axs = plt.subplots(1, 3, figsize=(20,5), subplot_kw={'projection': ccrs.PlateCarree()})

# For loop that uses the the 'resolution' and 'titles' variables to plot each subplot without having to code the same code repeatedly
for i, ax in enumerate(axs):
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    
    # Features with each resolution
    ax.add_feature(cfeature.GSHHSFeature(scale=resolutions[i]), facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.coastlines(resolution='10m')
    
    # Adds the False Bay text on the map
    ax.text(18.6, -34.2,
        'False Bay',
        transform=ccrs.PlateCarree(),
        fontsize=10)
    
    # Gridlines and titles for each figure
    gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
    gl.top_labels = False
    gl.right_labels = False
    ax.set_title(titles[i])

plt.suptitle("Effect of GSHHS Coastline Resolution on False Bay", fontsize=16)
plt.tight_layout()
plt.show()










# Importing packages
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
# %%
# Loading the dataset
bathy = xr.open_dataset('GMRTv4_4_1_20260326topo.grd')

# Checking dataset
print(bathy.data_vars)
# %%
# I cant casually define the region using longitude and latitude since they arent variables there, rather there is x and y range

# Extract info
x_min, x_max = bathy['x_range'].values
y_min, y_max = bathy['y_range'].values

nx, ny = bathy['dimension'].values  # number of points

print(nx, ny)
# %%
# Creates longitude and latitude arrays
lon = np.linspace(x_min, x_max, nx)
lat = np.linspace(y_min, y_max, ny)

# Reshapes bathymetry since it is flattened
z = bathy['z'].values.reshape(ny, nx)

# FLips the axis since I was not getting the the right direction on my plot
z = np.flipud(z)
# %%
# Plotting
fig, ax = plt.subplots(figsize=(10,6),
                       subplot_kw={'projection': ccrs.PlateCarree()})

# Plots bathymetry
im = ax.pcolormesh(
    lon, lat, z,
    cmap='turbo' ,
    vmin=-5000, vmax=0,
    shading='auto',
    transform=ccrs.PlateCarree()   
)

# Adds land and coastlines
ax.coastlines(linewidth=1.2)
ax.add_feature(cfeature.LAND, facecolor='lightgray', zorder=1)

# Gridlines
gl = ax.gridlines(draw_labels=True, linewidth=0.5, linestyle='--', alpha=0.5)
gl.top_labels = False
gl.right_labels = False

# Colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Depth (m)')

levels = [-4000, -2000, -1000, -500, -100]

# Adding contours
levels = [-4000, -2000, -1000, -500, -100]

cs = ax.contour(
    lon, lat, z,
    levels=levels,
    colors='black',
    linewidths=1.2,
    transform=ccrs.PlateCarree()
)

labels = ax.clabel(cs, inline=True, fontsize=9, fmt='%d')

# Improve label visibility
for txt in labels:
    txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=1))

ax.set_title('Bathymetry of Humboldt Current Region')

plt.savefig('bathymetry_map.png', dpi=300, bbox_inches='tight')
plt.show()
# %%



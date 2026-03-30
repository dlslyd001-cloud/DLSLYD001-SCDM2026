
# Importing packages
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.patches import Patch
# %%
# Loading the dataset
ds = xr.open_dataset('ESACCI-OC-MAPPED-CLIMATOLOGY-1M_MONTHLY_4km_PML_CHL-fv5.0.nc')

# Variable names
print(ds)
# %%
# Define region 
lat_min, lat_max = -20, -16
lon_min, lon_max = -76, -72

# Subset the data
ds_region = ds.sel(lat=slice(lat_max, lat_min), 
                   lon=slice(lon_min, lon_max))

# Checking data
print(ds_region)
# %%
# Reordering time
ds_region = ds_region.sortby('time.month')
# Checking 
print(ds_region['time.month'].values)
# %%
# Annual mean on the region

chl_mean = ds_region['chlor_a'].mean(dim='time')

fig, ax = plt.subplots(figsize=(10,6), subplot_kw={'projection': ccrs.PlateCarree()})

# Plot
im = ax.pcolormesh(
    chl_mean['lon'], chl_mean['lat'], chl_mean,
    cmap='plasma',
    norm=LogNorm(vmin=0.01, vmax=20),
    shading='auto')

# Coastlines and borders
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, facecolor='lightgray')

# Adds gridlines with labels
gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),
                  linewidth=1, color='gray', alpha=0.5, linestyle='--')

# Only shows lat/lon on left and bottom
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 9}
gl.ylabel_style = {'size': 9}

# Colorbar
cbar = plt.colorbar(im, ax=ax, orientation='vertical')

# Define ticks in real values
ticks = [0.01, 0.1, 1, 2, 5, 10, 20]

cbar.set_ticks(ticks)
cbar.set_ticklabels([str(t) for t in ticks])

cbar.set_label('Chlorophyll (mg/m³)', fontsize=11)

cs = ax.contour(
    chl_mean['lon'], chl_mean['lat'], chl_mean,
    levels=[1, 2, 5, 10],
    colors='black',
    linewidths=0.8,
    transform=ccrs.PlateCarree()
)

ax.clabel(cs, inline=True, fontsize=8)

ax.set_title('Annual Mean Chlorophyll (Humboldt Current Region)', fontsize=14)
plt.savefig('annual_mean_chlorophyll.png', dpi=300, bbox_inches='tight')
plt.show()
# %%
# Monthly mean of the regions chlorophyll

# Month labels
months = ds_region['time'].dt.strftime('%b').values

# Create figure
fig, axes = plt.subplots(3, 4, figsize=(20, 12),
                         subplot_kw={'projection': ccrs.PlateCarree()})

for i in range(12):
    ax = axes.flatten()[i]

    # Plot the chlorophyll
    chl = ds_region['chlor_a'].isel(time=i)
    im = chl.plot(
        ax=ax,
        cmap='viridis',
        norm=LogNorm(vmin=0.01, vmax=20),
        add_colorbar=False
    )

    # Highlight regions where chlorophyll > 2
    mask = np.where(chl > 2, 1, np.nan)  # change threshold here if needed
    ax.contourf(
        chl.lon, chl.lat, mask,
        levels=[0.5, 1.5],  # contour levels to cover mask
        colors='red',        # color for high-chl region
        alpha=0.3            # semi-transparent
    )

    # Coastlines and borders
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, facecolor='lightgray', zorder=0)

    # Adds gridlines with labels for lat/lon
    gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),
                      linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    if i % 4 != 0:
        gl.left_labels = False
    if i < 8:
        gl.bottom_labels = False
    gl.xlabel_style = {'size': 10}
    gl.ylabel_style = {'size': 10}

    # Title
    ax.set_title(months[i])
    
    # Contour lines
    cs = ax.contour(
    chl.lon, chl.lat, chl,
    levels=[1, 2, 5, 10],
    colors='black',
    linewidths=0.6,
    transform=ccrs.PlateCarree()
)
    
    ax.clabel(cs, inline=True, fontsize=7)

# Adds one shared colorbar for chlorophyll
cbar = plt.colorbar(
    plt.cm.ScalarMappable(norm=LogNorm(vmin=0.01, vmax=20), cmap='viridis'),
    ax=axes,
    orientation='vertical',
    fraction=0.02,
    pad=0.02
    )
cbar.set_ticks([0.01, 0.1, 1, 2, 5, 10, 20])
cbar.set_ticklabels([str(t) for t in [0.01, 0.1, 1, 2, 5, 10, 20]])
cbar.set_label('Chlorophyll (mg/m³)')

# Creates legend element
legend_elements = [
    Patch(facecolor='red', edgecolor='red', alpha=0.4, label='Chlorophyll > 2 mg/m³')
]

# Adds legend to figure
fig.legend(handles=legend_elements, loc='lower center', ncol=1, fontsize=11)

plt.suptitle(
    'Monthly Climatology of Chlorophyll (Humboldt Current Region)', 
    fontsize=16
)
plt.savefig('monthly_chlorophyll_panels.png', dpi=300, bbox_inches='tight')
plt.show()
# %%
# Month labels
months = ds_region['time'].dt.strftime('%b').values

# Create figure
fig, axes = plt.subplots(3, 4, figsize=(20, 12),
                         subplot_kw={'projection': ccrs.PlateCarree()})

for i in range(12):
    ax = axes.flatten()[i]

    # Plot the chlorophyll
    chl = ds_region['chlor_a'].isel(time=i)
    im = chl.plot(
        ax=ax,
        cmap='viridis',
        norm=LogNorm(vmin=0.01, vmax=20),
        add_colorbar=False
    )

    # Highlights regions where chlorophyll > 5
    mask = np.where(chl > 5, 1, np.nan)  # 1 where chl>5, nan elsewhere
    ax.contourf(
        chl.lon, chl.lat, mask,
        levels=[0.5, 1.5],  # contour levels to cover mask
        colors='red',        # color for high-chl region
        alpha=0.4            # semi-transparent
    )

    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)
    ax.set_title(months[i])

# Adds one shared colorbar for chlorophyll
cbar = plt.colorbar(
    plt.cm.ScalarMappable(norm=LogNorm(vmin=0.01, vmax=20), cmap='viridis'),
    ax=axes,
    orientation='vertical',
    fraction=0.02,
    pad=0.02
)
cbar.set_ticks([0.01, 0.1, 1, 10, 20])
cbar.set_ticklabels([str(t) for t in [0.01, 0.1, 1, 10, 20]])
cbar.set_label('Chlorophyll (mg/m³)')

plt.suptitle('Monthly Climatology of Chlorophyll (Humboldt Current Region)\nRed highlights: Chlorophyll > 5 mg/m³', fontsize=16)
plt.show()
# %%
# Checking seasonality

# Check data range
print("Min chlorophyll:", ds_region['chlor_a'].min().values)
print("Max chlorophyll:", ds_region['chlor_a'].max().values)

# Compute monthly mean
monthly_mean = ds_region['chlor_a'].mean(dim=['lat','lon'])

print("Monthly mean values:", monthly_mean.values)

# Month labels
months = ['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']

# Plot
plt.figure(figsize=(10,5))

plt.plot(months, monthly_mean, marker='o', linewidth=2, label='Regional mean')

# Labels and title
plt.xlabel('Month')
plt.ylabel('Chlorophyll (mg/m³)')
plt.title('Regional Mean Seasonal Cycle (Humboldt Current)')

# Grid
plt.grid(True, linestyle='--', alpha=0.5)

# Optional: set a nice y-range
plt.ylim(0, np.nanmax(monthly_mean.values)*1.2)

plt.legend()

plt.savefig('chlorophyll_seasonality_check.png', dpi=300, bbox_inches='tight')
plt.show()
# %%
# Time series comparing a maximum chlorophyll point to the regional mean

# Find the location of the maximum chlorophyll over the whole region and all months
max_idx = ds_region['chlor_a'].argmax(dim=['time', 'lat', 'lon'])

# Get the coordinates of that maximum
max_lat = ds_region['lat'][max_idx['lat']].values
max_lon = ds_region['lon'][max_idx['lon']].values

print(f"Highest chlorophyll point is at lat: {max_lat}, lon: {max_lon}")

# The max chlorophyll point
high_point = ds_region['chlor_a'].sel(lat=max_lat, lon=max_lon, method='nearest')

# Regional mean
regional_mean = ds_region['chlor_a'].mean(dim=['lat','lon'])

# Month labels
months = ds_region['time'].dt.strftime('%b').values

# Plot
plt.figure(figsize=(10,6))
plt.plot(months, regional_mean, marker='o', label='Regional mean')
plt.plot(months, high_point, marker='s', label=f'Max point ({max_lat:.2f}°S, {max_lon:.2f}°W)')

# Labels and title
plt.xlabel('Month')
plt.ylabel('Chlorophyll (mg/m³)')
plt.title('Humboldt Current: Monthly Chlorophyll Time Series (Linear Scale)')

plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

plt.savefig('chlorophyll_timeseries.png', dpi=300, bbox_inches='tight')
plt.show()
# %%
# The code below is to create a plot that overlays bathymetry with the chlorophyll
# %%
# Loading the dataset
bathy = xr.open_dataset('GMRTv4_4_1_20260326topo.grd')

# I cant casually define the region using longitude and latitude since they arent variables there, rather there is x and y range

# Extract info
x_min, x_max = bathy['x_range'].values
y_min, y_max = bathy['y_range'].values

nx, ny = bathy['dimension'].values  # number of points

# Creates longitude and latitude arrays
lon = np.linspace(x_min, x_max, nx)
lat = np.linspace(y_min, y_max, ny)

# Reshapes bathymetry since it is flattened
z = bathy['z'].values.reshape(ny, nx)

# FLips the axis since I was not getting the the right direction on my plot
z = np.flipud(z)

# Annual mean chlorophyll
chl_mean = ds_region['chlor_a'].mean(dim='time')

fig, ax = plt.subplots(figsize=(10,6),
                       subplot_kw={'projection': ccrs.PlateCarree()})

# 🌈 Chlorophyll (background)
im = ax.pcolormesh(
    chl_mean['lon'], chl_mean['lat'], chl_mean,
    cmap='viridis',
    norm=LogNorm(vmin=0.01, vmax=20),
    shading='auto',
    transform=ccrs.PlateCarree()
)

# 🌊 Bathymetry contours (overlay)
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

# 🌍 Land and coastlines
ax.add_feature(cfeature.LAND, facecolor='lightgray', zorder=1)
ax.coastlines(linewidth=1.2)

# 🧭 Gridlines
gl = ax.gridlines(draw_labels=True, linewidth=0.5, linestyle='--', alpha=0.5)
gl.top_labels = False
gl.right_labels = False

# 🎨 Colorbar (chlorophyll)
cbar = plt.colorbar(im, ax=ax)
ticks = [0.01, 0.1, 1, 2, 5, 10, 20]
cbar.set_ticks(ticks)
cbar.set_ticklabels([str(t) for t in ticks])
cbar.set_label('Chlorophyll (mg/m³)')

# 📏 Focus region
ax.set_extent([-76, -72, -20, -16], crs=ccrs.PlateCarree())

# Title
ax.set_title('Chlorophyll and Bathymetry (Humboldt Current Region)', fontsize=14)

plt.tight_layout()
plt.savefig('chlorophyll_bathymetry_combined.png', dpi=300, bbox_inches='tight')
plt.show()
# %%


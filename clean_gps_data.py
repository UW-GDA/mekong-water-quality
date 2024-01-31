# %%
import geopandas as gpd
import os
import pandas as pd
import matplotlib.pyplot as plt
# %%
# GPS points for 3S sampling
nov3s = gpd.read_file('data/3S_GPS/Waypoints_21-NOV-23.gpx')
# Filter out mistakes (unnamed)
nov3s = nov3s[nov3s['name'].str.match("[^0]")]
# Save as geojson
#nov3s.to_file('data/nov_3s.geojson', driver = 'GeoJSON')

# %%
# Look at other files (there are 25 total)
gdf = nov3s
for filename in os.listdir('data/3S_GPS'):
    gdf = pd.concat([gdf, gpd.read_file(f'data/3S_GPS/{filename}')])
gdf['time_string'] = [t.strftime('%Y-%m') for t in gdf['time']]

# %%
# Names look pretty clean for the most part.
# Plot the points to see what we're working with
 
# import shapefiles for borders and rivers
borders = gpd.read_file('data/asia-shp/yg089df0008.shp')
rivers = gpd.read_file('data/gmsriversadb/gms_river.shp')

# %%
import contextily
fig, ax = plt.subplots()
gdf.plot(ax = ax, column='time_string', legend=True)
rivers[rivers['Strahler'] > 3].plot(ax = ax, alpha=0.5, linewidth=2)
ax.set_ylim(10, 20)
ax.set_xlim(100, 112)
contextily.add_basemap(ax, 
                       crs=gdf.crs.to_string(), 
                       source=contextily.providers.Esri.WorldStreetMap)

# Start with a map near Vientiane
# It's some fish markets, apparently
fig, ax = plt.subplots()
gdf.plot(ax = ax, color = "green")
rivers[rivers['Strahler'] > 3].plot(ax = ax, alpha=0.5, linewidth=2)
# Add labels
for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.name):
    ax.annotate(label, xy=(x, y), xytext=(3,3), textcoords='offset points')
ax.set_ylim(14, 19)
ax.set_xlim(102, 106)
contextily.add_basemap(ax, 
                       crs=gdf.crs.to_string(), 
                       source=contextily.providers.Esri.WorldStreetMap)

# %%
# Now let's zoom way in on Stung Treng
# This is bbox for 3S samples from Nov, 2023
(xmin, ymin, xmax, ymax)= [105.8932, 13.4641, 106.2130, 13.59725]
fig, ax = plt.subplots()
gdf['time_string'] = [t.strftime('%Y-%m') for t in gdf['time']]
gdf.plot(ax = ax, column='time_string', legend=True)
rivers[rivers['Strahler'] > 3].plot(ax = ax, alpha=0.5, linewidth=2)
for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.name):
    ax.annotate(label, xy=(x, y), xytext=(3,3), textcoords='offset points')
ax.set_ylim(ymin, ymax)
ax.set_xlim(xmin, xmax)
contextily.add_basemap(ax, 
                       crs=gdf.crs.to_string(), 
                       source=contextily.providers.Esri.WorldStreetMap)

# %%
# East of Stung Treng

# Try to pull some sentinel data for this place/time
# June 24, 2022
import helpers
catalog = helpers.get_catalog()
(xmin, ymin, xmax, ymax)= [106.1, 13.4, 106.7, 13.7]
search = catalog.search(
    collections=['sentinel-2-l2a'], # this includes all Landsats
    bbox=[xmin, ymin, xmax, ymax], 
    datetime="2022-06-23/2022-06-24"
)
items = search.item_collection() # pystac.ItemCollection
#sentinel = gpd.GeoDataFrame.from_features(items.to_dict(), crs="epsg:4326")

# %%
# visualize sentinel https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/l2a_optimized/
import odc.stac
data = odc.stac.stac_load(
    items, 
    bands=['B04', 'B03', 'B02','visual'], 
    bbox=[xmin, ymin, xmax, ymax],
).isel(time=0)

# %%
fig, ax = plt.subplots(figsize=(15, 15))
#d = data[['B04', 'B03', 'B02']].to_array()
ax.axis('off')
data[['B04', 'B03', 'B02']].to_array().plot.imshow(robust=True, ax=ax, alpha = 0.9)
points = gdf[gdf['time_string'] == "2022-06"].to_crs('EPSG:32648')
points.plot(ax = ax, color = "black", facecolor = "pink")
for x, y, label in zip(points.geometry.x, points.geometry.y, points.name):
    ax.annotate(label, xy=(x, y), xytext=(3,-3), textcoords='offset points', color = "white")
ax.set_title("Sentinel-2 June 24, 2022")
plt.savefig('reservoir_locations.png', bbox_inches='tight')
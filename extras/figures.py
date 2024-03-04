# Run on planetary computer

# This will pull some sentinel data and plot sampling locations 
# near lower sesan-2 reservoir and save it to a png called
# reservoir_locations.png


# %%
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily

# %%
# Load sampling data
gdf = gpd.read_file('data/mekong_sampling_locations.geojson')

# %%
# East of Stung Treng: Make a satellite map

# Try to pull some sentinel data for this place/time
# June 24, 2022
import extras.helpers as helpers
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





##### Locations/context plot #####
# -------------------------------#
# %%
# Load mekong watershed
lmb = gpd.read_file('data/lmb.geojson')
# load asia countries file
countries = gpd.read_file('data/external/asia_polygons.gpkg')
# load rivers file (large rivers)
rivers = gpd.read_file('data/external/HydroRIVERS_v10_as_shp', 
                       mask = lmb,
                       where='ORD_FLOW < 5')
tsl = gpd.read_file('data/tonle_sap_lake.geojson')
# %%

# %%
# convert everything to utm zone 48 N
fig, ax = plt.subplots(figsize=(6, 12))
bounds = rivers.to_crs('EPSG:32648').unary_union.bounds
ax.set_xlim(bounds[0]-100000, bounds[2]+100000)
ax.set_ylim(bounds[1]-100000, bounds[3]+100000)
ax.axis('off')
rivers.to_crs('EPSG:32648').plot(ax=ax, color = "#01099e")
lmb.to_crs('EPSG:32648').plot(ax=ax, facecolor = '#6e9ecc66', edgecolor='#6e9ecc')
tsl.to_crs('EPSG:32648').plot(ax=ax, color = "#01099e")
countries.to_crs('EPSG:32648').plot(ax=ax, facecolor='none', edgecolor='k', linewidth=0.5)
# add basemap
contextily.add_basemap(ax, 
                       crs='EPSG:32648', 
                       source=contextily.providers.Esri.WorldImagery,
                       alpha=0.8)
plt.savefig('extras/overview_map.png', 
            bbox_inches='tight', 
            pad_inches=0)

#### 3S samples #####
#### ---------- #####

# %%

# load samples
gdf = gpd.read_file('data/nov_3s.geojson')
minidots = gdf[gdf.name.str.contains("1$")]
# no SSN
minidots = minidots[~minidots.name.str.contains("SSN")]

# %%
# Get sentinel from Nov, 2023
time_range="2023-11-19/2023-12-01"
bbox = [105.9300, 13.4841, 106.0653, 13.59725]
search = catalog.search(
    collections=['sentinel-2-l2a'], # this includes all Landsats
    bbox=bbox, 
    datetime=time_range,
    query={"s2:mgrs_tile": {"in": ["48PXA"]}}
)
items = search.item_collection()
#sentinel = gpd.GeoDataFrame.from_features(items.to_dict(), crs="epsg:4326")
dec_1_s2b = items[0]
nov_26_s2a = items[1]
nov_21_s2b = items[2]# 11/21, 11/26, 12/1

# %%
# visualize sentinel https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/l2a_optimized/
data = odc.stac.stac_load(
    [nov_21_s2b], 
    bands=['B04', 'B03', 'B02','visual'], 
    bbox=bbox,
).isel(time=0)
fig, ax = plt.subplots()
#d = data[['B04', 'B03', 'B02']].to_array()
ax.axis('off')
data[['B04', 'B03', 'B02']].to_array().plot.imshow(robust=True, ax=ax)
ax.set_title("Locations of oxygen sensors\n(Sentinel 2B, Nov 21, 2023)")
ax.title.set_visible(False)

# Now plot points https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.plot.html
#samples.plot(ax=ax, color = "#00125b", markersize=90, marker="D", edgecolor="white")
minidots.to_crs("EPSG:32648").plot(ax=ax, color = "#00125b", markersize=120, edgecolor="white")
plt.savefig('extras/sample_locations.png', 
            bbox_inches='tight', 
            pad_inches=0)



#### TSL samples #####
#### ---------- #####
# %%
# Load sampling locations
tsl_locations = pd.read_csv('data/tsl-locations.csv')
tsl_gdf = gpd.GeoDataFrame(
    tsl_locations, 
    geometry=gpd.points_from_xy(tsl_locations.longitude, 
                                tsl_locations.latitude), 
                                crs="EPSG:4326"
)
tsl_gdf = tsl_gdf.to_crs('EPSG:32648')
# %%
# Pull sentinel data from 12/14/2023
# ymin = 12.302442, xmax = 104.574902
# ymax = 13.344433, xmin = 103.618602

# %%
# Get limits for plotting
ymin = 12.302442
xmax = 104.574902
ymax = 13.344433
xmin = 103.618602
lims = gpd.points_from_xy([xmin, xmax], [ymin, ymax], crs='EPSG:4326')
(xmin, ymin, xmax, ymax) = lims.to_crs('EPSG:32648').unary_union().bounds
#gpd.GeoDataFrame(geometry = lims).plot()
# %% 

fig, ax = plt.subplots()
ax.axis('off')
tsl_gdf.plot(ax=ax, color = "#00125b", markersize=120, edgecolor="white")
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
contextily.add_basemap(ax, 
                       crs='EPSG:32648', 
                       source=contextily.providers.Esri.WorldImagery,
                       alpha=0.8)
plt.savefig('extras/tsl_sample_locations.png', 
            bbox_inches='tight', 
            pad_inches=0)



# %%

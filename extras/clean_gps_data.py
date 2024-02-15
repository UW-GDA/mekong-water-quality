# This will read in the gpx data from the garmin, clean it up, 
# and save it as a geojson called mekong_sampling_locations.geojson

# %%
import geopandas as gpd
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
# %%
# GPS points for 3S sampling
nov3s = gpd.read_file('data/3S_GPS/Waypoints_21-NOV-23.gpx')
# Filter out mistakes (unnamed)
nov3s = nov3s[nov3s['name'].str.match("[^0]")]
# Save as geojson
nov3s.to_file('data/nov_3s.geojson', driver = 'GeoJSON')

# %%
# Look at other files (there are 25 total)
gdf = nov3s
for filename in os.listdir('data/3S_GPS'):
    if filename != 'Waypoints_21-NOV-23.gpx':
        gdf = pd.concat([gdf, gpd.read_file(f'data/3S_GPS/{filename}')])

# Add a categorical variable with month and year
gdf['time_string'] = [t.strftime('%Y-%m') for t in gdf['time']]

# drop NaN columns and column for symbol in garmin
gdf = gdf.dropna(axis=1).drop('sym', axis = 1)

# get rid of one last bad name
gdf = gdf.loc[-gdf['name'].str.contains('!'), :]

# add a column for local time
gdf['time_local'] = [dt.astimezone(datetime.timezone(datetime.timedelta(hours=7))) for dt in gdf['time']]

# %%
# Names look pretty clean for the most part. 
# Remove any points where the name doesn't have any letters

# don't do this: it removes points with a letter at the beginning (eg 3SB)
# gdf = gdf[gdf['name'].str.match("\D")]

# I don't know what the difference is between match and contains but contains seems to work 
# as I would expect and match does not.  
gdf = gdf.loc[gdf['name'].str.contains('\D'), :]

# %%
# Add a column to classify points depending on campaign
gdf.loc[:,'campaign'] = pd.Series(dtype = "string")
gdf

# %%
# Fish samples
gdf.loc[gdf['name'].str.contains("MARKET"), 'campaign'] = 'Fish'

# %%
# What are SKG-3A and PHNOM? 

# Set this campaign to 3S
gdf.loc[gdf['time_string'] == '2023-11', 'campaign'] = '3S'

# %%
gdf.loc[gdf['time_string'] == '2022-06', 'campaign'] = 'Sesan2'

# %%
gdf.loc[
        np.logical_and( gdf['time_string'] == '2022-07', 
                    gdf['name'].str.contains('\d') ),
        'campaign'
    ] = 'Phnom_Penh'

# %%
gdf.loc[gdf['name'] == 'BAN MAI', 'campaign'] = 'ban_mai'

# %% Write it

gdf.to_file('data/mekong_sampling_locations.geojson', driver = 'GeoJSON')

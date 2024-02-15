# Tracking water quality over time in the Lower Mekong

Helen Miller

A satellite remote sensing workflow for detecting water quality parameters in the Lower Mekong River basin. 

__Background__: The Mekong River is one of the world's largest rivers, and the Lower Mekong Basin (LMB) feeds an estimated 60 million people daily. Its biodiversity and productivity is driven by seasonal fluctuations in flow driven by the monsoonal climate, known as the flood-pulse. The processes driving productivity are likely changing with the onset of widespread deforestation and hydropower dam development in the last two decades. Remote sensing methods exist for some key indicators of water quality, including chlorophyll (an indicator for phytoplankton abundance) and turbidity. Using the Harmonized Landsat Sentinel dataset, this project will track chlorophyll and turbidity over the last decade in all large mainstem and tributary river reaches in the Lower Mekong Basin. 

__Questions__:  
* How have chlorophyll concentrations and turbidity changed in the last decade across the Lower Mekong Basin?
* Where have any changes occurred? Does it vary across the river network?

__Datasets__: 
* [HydroSHEDs river reaches](https://www.hydrosheds.org/products/hydrorivers) -- for identifying and differentiating river reaches. 
* [JRC water extent](https://global-surface-water.appspot.com/download) -- for delineating where water is (and is not)
* [Harmonized Landsat Sentinel](https://hls.gsfc.nasa.gov/) -- for calculating indices

__Tools/packages__: 

* For working with vector data (stream shapefiles): geopandas
* For working with raster data (water masks and satellite data): rasterio and rioxarray
* For accessing HLS data: [earthaccess](https://github.com/nsidc/earthaccess/) python package. It is an api for accessing NASA earth data. 
    * tutorial [here](https://github.com/nasa/HLS-Data-Resources/blob/main/python/tutorials/HLS_Tutorial.ipynb)
* For analyzing changes in seasonality and trends: [BFAST](https://bfast2.github.io/) 


__Methodology__:

The data processing for this project will largely follow methods from [Gardner et al, 2021](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2020GL088946) for retrieving remote sensing reflectance associated with individual river reaches. This will involve: 

1. Create water masks for each river reach: 
    1. Identify river reaches of interest 
    1. Create a buffer around those river reaches
    1. Identify water pixels within the buffer
    1. Associate water pixels with individual river reaches
    1. Exclude water pixels which are not connected to the main river channel
1. Get time series of median NDCI and NDTI indices for each river reach: 
    1. Pull reflectance for river reach mask for one satellite image (R,G,NIR)
    1. Remove clouds, cloud shadows, or any pixels which did not pass QC. 
    1. Record the number (or percentage) of pixels which DID pass QC. 
    1. Calculate median NDCI and NDTI for remaining pixels
    1. Repeat for all river reaches and all images
1. Analyze time series
    1. Plot indices over time
    1. Analyze seasonal and multi-year trends

__Expected outcomes__:
This project will result in a time series of NDCI and NDTI for the last decade from five connected river reaches in the LMB, and some preliminary analysis of seasonal and longer-term trends in chlorophyll and turbidity. No long-term datasets exist at large spatial scales for these water quality parameters, and they can be used to asses how water quality is changing over time as a result of changes to water and land use. These methods can be used to further this analysis for all river reaches across the LMB to perform an analysis of spatial and temporal variability.




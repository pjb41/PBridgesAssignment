import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import rasterio as rio
from rasterio.plot import show
import fiona as f
import numpy as np
import matplotlib.lines as mlines

plt.ion()





seadef = gpd.read_file('Data/seadef_sel.shp')
dtm = gpd.read_file('Data/Raster_tr35_dt3.shp')
points1 = gpd.read_file('Data/points1.shp')



print(seadef.crs)
print(dtm.crs)
print(points1.crs)



myFig = plt.figure(figsize=(25, 25))

myCRS = ccrs.UTM(31)

ax = plt.axes(projection=ccrs.Mercator(31))









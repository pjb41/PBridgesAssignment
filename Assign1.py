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

def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles


seadef = gpd.read_file('Data/Flood_Map_for_Planning_Rivers_and_Sea_Areas_Benefiting_from_Flood_Defences.shp')
dtm = gpd.read_file('Data/Raster_tr35_dt3.shp')
myFig = plt.figure(figsize=(10, 10))

myCRS = ccrs.UTM(29)

ax = plt.axes(projection=ccrs.Mercator())

print(seadef.head())
seadef.crs
dtm.crs
seadef_bng = seadef.to_crs(epsg=27700)
print(seadef_bng.head())
dtm_bng = dtm.to_crs(epsg=27700)
print(seadef_bng)
print(seadef.crs == dtm.crs)

join = gpd.sjoin(seadef, dtm, how='inner', lsuffix='left', rsuffix='right')
join

print(join)








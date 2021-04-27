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

def scale_bar(ax, location=(0.92, 0.95)):
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]

    tmc = ccrs.TransverseMercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    plt.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=9, transform=tmc)
    plt.plot([sbx, sbx - 5000], [sby, sby], color='k', linewidth=6, transform=tmc)
    plt.plot([sbx-5000, sbx - 10000], [sby, sby], color='w', linewidth=6, transform=tmc)


seadef = gpd.read_file('Data/seadef_sel.shp')
dtm = gpd.read_file('Data/Raster_tr35_dt3.shp')
myCRS = ccrs.UTM(29)
myFig, ax = plt.subplots(1, 1, figsize=(12,12), subplot_kw=dict(projection=myCRS))



ax = plt.axes(projection=ccrs.Mercator())













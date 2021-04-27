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

    plt.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=tmc)
    plt.plot([sbx, sbx - 5000], [sby, sby], color='k', linewidth=4, transform=tmc)
    plt.plot([sbx-5000, sbx - 10000], [sby, sby], color='w', linewidth=4, transform=tmc)

    plt.text(sbx, sby-4500, '10km', transform=tmc, fontsize=8)
    plt.text(sbx-12500, sby-4500, '5km', transform=tmc, fontsize=8)
    plt.text(sbx-24500, sby-4500, '0km', transform=tmc, fontsize=8)

outline = gpd.read_file('Data/outline_kent.shp')
seadef = gpd.read_file('Data/seadef_sel.shp')
dtm = gpd.read_file('Data/Raster_tr35_dt3.shp')

myFig = plt.figure(figsize=(12, 12))

myCRS = ccrs.UTM(31)

ax = plt.axes(projection=ccrs.Mercator())

outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='gray')
xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature)

inset_feature = ShapelyFeature(seadef['geometry'], myCRS, edgecolor='k', facecolor='CornflowerBlue')
xmin, ymin, xmax, ymax = seadef.total_bounds
ax.add_feature(inset_feature)

top_feature = ShapelyFeature(dtm['geometry'], myCRS, edgecolor='k', facecolor='w')
xmin, ymin, xmax, ymax = dtm.total_bounds
ax.add_feature(top_feature)



ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)

myFig.savefig('assign1.png', bbox_inches= 'tight', dpi=300)













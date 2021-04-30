
# load the modules required for this exercise, depending on sources of data (vector or raster).
# You can also import Polygon in addition to Point from shapely.geometry.
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import fiona as f
import numpy as np
import matplotlib.lines as mlines
from shapely.geometry import Point

# make the plot interactive.
plt.ion()




# load the required datasets. In this instance we have used 3 vector shapefiles and 2 csv sheets.
seadef = gpd.read_file('Data/seadef_sel.shp')
dtm = gpd.read_file('Data/Raster_tr35_dt3.shp')
points1 = gpd.read_file('Data/points1.shp')
settlement = gpd.read_file('Data/settlement_xy.csv')
seadefpoints = gpd.read_file('Data/seadef_points.csv')


# display the Co-ordinate reference system (CRS) information here to ensure all datasets have identical information.
print(seadef.crs)
print(dtm.crs)
print(points1.crs)


# create a figure of size 12x12 (based in inches)
myFig = plt.figure(figsize=(12, 12))

myCRS = ccrs.UTM(31)

ax = plt.axes(projection=ccrs.Mercator(31))


top_feature = ShapelyFeature(dtm['geometry'], myCRS, edgecolor='black', facecolor='w')
xmin, ymin, xmax, ymax = dtm.total_bounds
ax.add_feature(top_feature)

ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)


inset_feature = ShapelyFeature(seadef['geometry'], myCRS, edgecolor='blue', facecolor='CornflowerBlue')
xmin, ymin, xmax, ymax = seadef.total_bounds
ax.add_feature(inset_feature)
alpha = 1

end_feature = ax.plot(points1.geometry.x, points1.geometry.y, 's', color='red', ms=10, transform=myCRS)


plt.suptitle('Settlements at risk from coastal protection breach', fontsize=30)

top_feature = mpatches.Patch(color='black', label='Topography')
inset_feature = mpatches.Patch(color='CornflowerBlue', label='Protection area')
end_feature = mpatches.Patch(color='red', label='Settlements')


plt.legend(handles=[top_feature, inset_feature, end_feature], fontsize=12, title="LEGEND")


ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)

def scale_bar(ax, location=(0.92, 0.95)):
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]

    tmc = ccrs.TransverseMercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    plt.plot([sbx, sbx - 1000], [sby, sby], color='k', linewidth=9, transform=tmc)
    plt.plot([sbx, sbx - 500], [sby, sby], color='k', linewidth=6, transform=tmc)
    plt.plot([sbx-500, sbx - 1000], [sby, sby], color='w', linewidth=6, transform=tmc)

    plt.text(sbx, sby-100, '5 km', transform=tmc, fontsize=8)
    plt.text(sbx-500, sby-100, '2.5 km', transform=tmc, fontsize=8)
    plt.text(sbx-1000, sby-100, '0 km', transform=tmc, fontsize=8)

scale_bar(ax)


plt.show()

print(settlement)

print(seadefpoints)


pnt1 = Point(51.2704600, 1.3610670)
pnt2 = Point(51.2704600, 1.3610670)
points_df = gpd.GeoDataFrame({'geometry': [pnt1, pnt2]}, crs='EPSG:4326')
points_df = points_df.to_crs('EPSG:27700')
points_df2 = points_df.shift()
points_df.distance(points_df2)
print(points_df.distance(points_df2))






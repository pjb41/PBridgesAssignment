
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


# create a figure of size 25x25 (based in inches)
myFig = plt.figure(figsize=(25, 25))

# Create a Universal Transverse Mercator reference system to transfrom the data.
# In this case for the East of UK we use 31.
# To find the UTM for your desired location go to : https://mangomap.com/robertyoung/maps/69585/what-utm-zone-am-i-in-#
myCRS = ccrs.UTM(31)

# Create an axis object in the figure using a Mercator projection, where we can actually plot our data
ax = plt.axes(projection=ccrs.Mercator())

# We are adding the topography data using ShapelyFeature from cartopy with black lines and a white face.
top_feature = ShapelyFeature(dtm['geometry'], myCRS, edgecolor='black', facecolor='w')
# add the features
xmin, ymin, xmax, ymax = dtm.total_bounds
ax.add_feature(top_feature)

# using set_extent we are re-ordering the co-ordinates to zoom the map to our area of interest.
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)

# We are adding our sea defences polygon data onto the topography data again using ShapelyFeature.
# Here we are using a blue outline with a Cornflower Blue fill.
inset_feature = ShapelyFeature(seadef['geometry'], myCRS, edgecolor='blue', facecolor='CornflowerBlue')
xmin, ymin, xmax, ymax = dtm.total_bounds
ax.add_feature(inset_feature)


# Here we plot the point data of at risk settlements on top of both previously plotted layers.
# To stand out against black and blue I have used red fro these points.
end_feature = ax.plot(points1.geometry.x, points1.geometry.y, 's', color='red', ms=10, transform=myCRS)

# Here we create a title for our map and use a font size of 30.
plt.suptitle('Settlements at risk from coastal protection breach', fontsize=30)


# This is where we create the component for our legend using just colors and label names.
top_feature = mpatches.Patch(color='black', label='Topography')
inset_feature = mpatches.Patch(color='CornflowerBlue', label='Protection area')
end_feature = mpatches.Patch(color='red', label='Settlements')

# Plot the legend, here we have used a font size of 12 and just "LEGEND" for the title.
plt.legend(handles=[top_feature, inset_feature, end_feature], fontsize=12, title="LEGEND")


# Design a scale bar for a length of 5km to go in the top right corner of your map.
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

# Change the numbering of your increments here.
    plt.text(sbx, sby-100, '5 km', transform=tmc, fontsize=8)
    plt.text(sbx-500, sby-100, '2.5 km', transform=tmc, fontsize=8)
    plt.text(sbx-1000, sby-100, '0 km', transform=tmc, fontsize=8)


#Plot the scale bar
scale_bar(ax)

# Plot your map
plt.show()
myFig

# Display the data for the settlement csv
print(settlement)
# Display the data for seadefpoints csv
print(seadefpoints)

# pnt1 takes the lat and lon co-ordinates from settlement csv (in this case Sandown)
pnt1 = Point(51.2704600, 1.3610670)
# pnt2 takes the lat and lon co-ordinates from seadefpoints csv (in this case Sandown)
pnt2 = Point(51.2704600, 1.3610670)
# Using GeoPandas we call the point data using the WGS 84 co-ordinate system as a default geometry.
points_df = gpd.GeoDataFrame({'geometry': [pnt1, pnt2]}, crs='EPSG:4326')
# We then transfer the system to what our previous projections are based upon (EPSG 27700 - British National Grid).
points_df = points_df.to_crs('EPSG:27700')
# The data frame is shifted by 1 to align pt1 with pt2.
points_df2 = points_df.shift()
points_df.distance(points_df2)
# The calculate is printed to display at the end of the console. In this case the answer should be 0.0 (in metres),
# which means Sandown already lies within the areas protected by sea defences.
print(points_df.distance(points_df2))






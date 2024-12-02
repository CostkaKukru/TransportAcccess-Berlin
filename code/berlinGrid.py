import geopandas as gpd
import matplotlib.pyplot as plt
import osmnx as ox

# Define the place and tags
place = "Berlin, Germany"
tags = {"amenity": True}  # Filter for POIs with amenities

# Download POIs for Berlin using osmnx
pois = ox.features_from_place(place, tags)

# Load Berlin streets shapefile
path = 'berlinStreets.shp'
# bln = gpd.read_file(path)

# # Ensure CRS of POIs matches streets data
# pois = pois.to_crs(bln.crs)

# # Plot streets and POIs
# fig, ax = plt.subplots(figsize=(24, 16))
# bln.plot(ax=ax, color="gray", linewidth=0.5)
# pois.plot(ax=ax, color="red", markersize=10, label="POIs")

# plt.title("Berlin Streets and POIs", fontsize=16)
# plt.legend()
# plt.show()

#sometimes you need to play with which_result parameter
#because you can receive node point, not the polygon
region = ox.geocoder.geocode_to_gdf([place])

#building: True means that every type of buildings will be downloaded
#buildings = ox.geometries.geometries_from_polygon(region['geometry'][0], tags = {'building': True})
#Using graph module we will recieve graph of roads in the city
roads = ox.graph.graph_from_polygon(region['geometry'][0])

#Here we specify specific tags
# forest = ox.geometries.geometries_from_polygon(region['geometry'][0], tags = {'landuse': 'forest'})
# rivers = ox.geometries.geometries_from_polygon(region['geometry'][0], tags = {'waterway': 'river'})
#city
ax = region.plot(facecolor = '#494D4D', figsize=(85,85))
ax.set_facecolor('#2C2E2E')
# buildings['geometry'].plot(facecolor = '#C61313',
#                            edgecolor = '#C61313',
#                            linewidth = 3,
#                            markersize = 1,
#                            ax = ax)

# rivers.plot(edgecolor = '#67A0C3',
            # linewidth = 6,
            # linestyle = '-',
            # ax = ax)

ox.plot_graph(roads,
              edge_color = 'white',
              edge_linewidth=0.2,
              node_size = 0,
              ax=ax)

ax.grid('on', which='major', axis='x', color = '#99A2A2')
ax.grid('on', which='major', axis='y', color = '#99A2A2')
plt.show()
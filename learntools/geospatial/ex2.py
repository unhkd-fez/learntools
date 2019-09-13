from learntools.core import *

import pandas as pd
import geopandas as gpd

# Q1
birds_df = pd.read_csv("../input/geospatial-course-data/purple_martin.csv", parse_dates=['timestamp'])
birds = gpd.GeoDataFrame(birds_df, geometry=gpd.points_from_xy(birds_df["location-long"], birds_df["location-lat"]))
birds.crs = {'init' :'epsg:4326'}

# Q3
end_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: x[-1]).reset_index()
end_gdf = gpd.GeoDataFrame(end_df, geometry=end_df.geometry)
end_gdf.crs = {'init' :'epsg:4326'}

# Q5
protected_filepath = "../input/geospatial-course-data/SAPA_Aug2019-shapefile/SAPA_Aug2019-shapefile-polygons.shp"
protected_areas = gpd.read_file(protected_filepath)

# Q7
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
americas = world.loc[world['continent'].isin(['North America', 'South America'])]
south_america = americas.loc[americas['continent']=='South America']
totalArea = sum(south_america.geometry.to_crs(epsg=3035).area) / 10**6

class Q1(EqualityCheckProblem):
    _var = "birds"
    _expected = birds
    _hint = ("Use `gpd.GeoDataFrame()`, and use `gpd.points_from_xy()` to create `Point` objects "
        "from the latitude and longitude locations.")
    _solution = CS(
"""# Create the GeoDataFrame
birds = gpd.GeoDataFrame(birds_df, geometry=gpd.points_from_xy(birds_df["location-long"], birds_df["location-lat"]))

# Set the CRS to {'init': 'epsg:4326'}
birds.crs = {'init' :'epsg:4326'}
""")

class Q2(CodingProblem):
    _hint = "Use the `plot()` method of each GeoDataFrame."
    _solution = CS(
"""ax = americas.plot(figsize=(10,10), color='white', linestyle=':', edgecolor='gray')
birds.plot(ax=ax, markersize=10)

# Uncomment to zoom in
#ax.set_xlim([-110, -30])
#ax.set_ylim([-30, 60])
""")
    def check(self):
        pass 

class Q3(CodingProblem):
    _var = "end_gdf"
    _hint = "The code that you need to write is very similar to the code that was used to create `start_gdf`."
    _solution = CS(
"""end_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: x[-1]).reset_index()
end_gdf = gpd.GeoDataFrame(end_df, geometry=end_df.geometry)
end_gdf.crs = {'init': 'epsg:4326'}
""")
    def check(self, results):
        assert type(results) == gpd.geodataframe.GeoDataFrame, \
        "`end_gdf` should be a GeoDataFrame."
        assert results.crs == {'init': 'epsg:4326'}, \
        "Don't forget to set the CRS to `{'init': 'epsg:4326'}`."
        sorted_end_gdf = end_gdf.sort_values(by='tag-local-identifier')
        sorted_results = results.sort_values(by='tag-local-identifier')
        assert sorted_end_gdf.equals(sorted_results), \
        "The results don't look right.  Please try again."

class Q4(CodingProblem):
    _hint = "Use the `plot()` method of each GeoDataFrame."
    _solution = CS(
"""ax = americas.plot(figsize=(10, 10), color='white', linestyle=':', edgecolor='gray')

start_gdf.plot(ax=ax, color='red',  markersize=30)
path_gdf.plot(ax=ax, cmap='tab20b', linestyle='-', linewidth=1, zorder=1)
end_gdf.plot(ax=ax, color='black', markersize=30)
""")
    def check(self):
        pass 

class Q5(EqualityCheckProblem):
    _var = "protected_areas"
    _expected = protected_areas
    _hint = ("Use `gpd.read_file()`.")
    _solution = CS(
"""protected_areas = gpd.read_file(protected_filepath)
""")
        
class Q6(CodingProblem):
    _hint = ("Use the `plot()` method of the `south_america` and `protected_areas` GeoDataFrames.")
    _solution = CS(
"""# Plot protected areas in South America
ax = south_america.plot(figsize=(10,10), color='white', edgecolor='gray')
protected_areas.plot(ax=ax, alpha=0.4)
""")
    def check(self):
        pass
    
class Q7(EqualityCheckProblem):
    _var = "totalArea"
    _expected = totalArea
    _hint = ("Use the `to_crs()` method to change the CRS to EPSG 3035.")
    _solution = CS(
"""totalArea = sum(south_america.geometry.to_crs(epsg=3035).area) / 10**6
""")
    
class Q8(CodingProblem):
    _hint = "When in South America, the birds are south of the equator."
    _solution = CS(
"""ax = south_america.plot(figsize=(10,10), color='white', edgecolor='gray')
protected_areas[protected_areas['MARINE']!='2'].plot(ax=ax, alpha=0.4, zorder=1)
birds[birds.geometry.y < 0].plot(ax=ax, color='red', alpha=0.6, markersize=10, zorder=2)
""")
    def check(self):
        pass

qvars = bind_exercises(globals(), [
    Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8
    ],
    tutorial_id=0,
    var_format='q_{n}',
    )
__all__ = list(qvars)

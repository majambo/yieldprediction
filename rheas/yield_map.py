import pandas as pd
import pandas as pd
import geopandas as gpd
from bokeh.plotting import figure, show
from bokeh.models import GeoJSONDataSource, ColumnDataSource, HoverTool
from bokeh.palettes import Viridis256
from bokeh.models import LinearColorMapper, ColorBar

shapefile = gpd.read_file("unimodal.shp")
country_shapefile = gpd.read_file('tanzania.shp')
yield_data = pd.read_csv("districts_points2.csv")
merged_data = pd.merge(shapefile, yield_data, on="NAME_2")

geo_source = GeoJSONDataSource(geojson=merged_data.to_json())
country_geo_source = GeoJSONDataSource(geojson=country_shapefile.to_json())

p = figure(title='Yield Data by District',
           plot_width=600, plot_height=600)


color_mapper = LinearColorMapper(palette=Viridis256, low=min(merged_data['gwad']), high=max(merged_data['gwad']))

p.multi_line('xs','ys', source=country_geo_source,
            line_color='black', line_width=0.5)

p.patches('xs','ys', source=geo_source,
          fill_color={'field': 'gwad', 'transform': color_mapper},
          fill_alpha=0.7, line_color='black', line_width=0.5)


hover = HoverTool(tooltips=[('District', '@NAME_2'), ('Yield', '@gwad')])
p.add_tools(hover)


color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=20, height=300,
                     border_line_color=None, location=(0,0), orientation='vertical')
p.add_layout(color_bar, 'right')

show(p)
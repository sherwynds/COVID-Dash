import json
import requests
import pandas as pd
from pandas import json_normalize
import numpy as np
import bokeh
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource

class Plotter:

    # colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
    colors = ["#824737", "#67923D", "#D6562B", "#007042", "#F09B36", "#74CCE5", "#F4BB3A", "#00BBD6", "#ABC178", "#C6A9B5", "#9C8156", "#895881", "#BC9F77"]

    data = {
        'British Columbia': pd.DataFrame(),
        'Alberta': pd.DataFrame(),
        'Saskatchewan': pd.DataFrame(),
        'Manitoba': pd.DataFrame(),
        'Ontario': pd.DataFrame(),
        'Quebec': pd.DataFrame(),
        'Newfoundland and Labrador': pd.DataFrame(),
        'Prince Edward Island': pd.DataFrame(),
        'Nova Scotia': pd.DataFrame(),
        'New Brunswick': pd.DataFrame(),
        'Yukon': pd.DataFrame(),
        'Northwest Territories': pd.DataFrame(),
        #'Nunavut': pd.DataFrame(), TODO: Handle Nunavut
    }


    def __init__(self):
        self.get_data()
    
    def get_data(self):
        cases = json_normalize((requests.request("GET", "https://api.covid19api.com/dayone/country/Canada/status/confirmed", headers={}, data={})).json())
        cases = cases.groupby(['Province'])

        # Add and organize the data into dataframes with Dates, Cases, DailyCases, TODO Deaths, DailyDeaths
        for prov in self.data:
            if prov not in cases.groups:
                # TODO: handle this functionality here
                pass
            else:
                df = cases.get_group(prov)
                df = df[['Date', 'Cases']]
                index = np.arange(0, len(df.index))
                df.set_index(index, inplace=True)
                df[['DailyCases']] = df[['Cases']].diff()
                df.at[0, 'DailyCases'] = df.at[0, 'Cases']
                df['Date'] = df['Date'].apply(lambda x: x[0:10])
                df['Date'] = pd.to_datetime(df['Date'])
                self.data[prov] = df

        # Print DataFrame to console for debugging
        for prov in self.data:
            print(prov)
            print(self.data[prov])
    
    # Plot new cases per day by province
    def plot_cases(self):

        p = figure(title="COVID Daily Active Cases by Province", x_axis_type='datetime', plot_height=700, plot_width=1400, x_axis_label='Date', y_axis_label='Active Cases')
        
        for data, name, color in zip(self.data.values(), self.data.keys(), self.colors):
            size = len(data)
            names = [name for x in range(size)]             # Create names for tooltips
            source = ColumnDataSource(data={
                'Date': data['Date'],
                'ActiveCases': data['DailyCases'],
                'Province': names,
            })
            p.line(x='Date', y='ActiveCases', line_width=2, color=color, alpha=0.9, legend_label=name, source=source)
        p.legend.location='top_left'
        
        # Add hover information
        p.add_tools(HoverTool(
            tooltips=[
                ('Province', '@Province'),
                ('Active Cases', '@ActiveCases{0}'),
                ('Date', '@Date{%F}'),
            ],
            formatters={
                '@Date': 'datetime',
                'ActiveCases': 'printf',
            }
        ))
        return p

    # End Code

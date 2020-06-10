import json
import requests
import pandas as pd
from pandas import json_normalize
import numpy as np
import bokeh
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource

class Plotter:

    BC = pd.DataFrame()
    colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']

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
        result = json_normalize((requests.request("GET", "https://api.covid19api.com/dayone/country/Canada/status/confirmed", headers={}, data={})).json())
        result = result.groupby(['Province'])
        self.BC = result.get_group("British Columbia")
        self.BC = self.BC[['Date', 'Cases']]
        self.BC[['DailyCases']] = self.BC[['Cases']].diff()
        bc_index = np.arange(0, len(self.BC.index))        
        self.BC.set_index(bc_index, inplace=True)
        self.BC.at[0, 'DailyCases'] = self.BC.at[0, 'Cases']
        (self.BC)['Date'] = (self.BC)['Date'].apply(lambda x: x[0:10])
        (self.BC)['Date'] = pd.to_datetime((self.BC)['Date'])
    
    def get_data(self):
        cases = json_normalize((requests.request("GET", "https://api.covid19api.com/dayone/country/Canada/status/confirmed", headers={}, data={})).json())
        cases = cases.groupby(['Province'])
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
        for prov in self.data:
            print(prov)
            length = len(self.data[prov].index)
            print(self.data[prov].head(length))
            print(self.data[prov]['Date'].dtype)
    
    def plot_cases(self):
        p = figure(title="COVID Daily Cases by Province", x_axis_type='datetime', plot_height=700, plot_width=1400, x_axis_label='Date', y_axis_label='New Cases')
        for data, name, color in zip(self.data.values(), self.data.keys(), self.colors):
            source = ColumnDataSource(data={
                'Date': data['Date'],
                'DailyCases': data['DailyCases']
            })
            p.line(x='Date', y='DailyCases', line_width=2, color=color, alpha=0.8, legend_label=name, source=source)
        p.legend.location='top_left'
        p.add_tools(HoverTool(
            tooltips=[
                ('Date', '@Date{%F}'),
                ('New Cases', '@DailyCases{0}'),
            ],

            formatters={
                '@Date': 'datetime',
                'DailyCases': 'printf',
            }
        ))
        return p

    def plot_BC_cases(self):
        p = figure(title="BC Test Plot", x_axis_type='datetime', plot_height=700, plot_width=1400)
        x = self.BC['Date']
        y = self.BC['DailyCases']
        p.line(x,y)
        return p
        

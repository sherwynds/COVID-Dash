import json
import requests
import pandas as pd
from pandas import json_normalize
import numpy as np
import bokeh
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, CrosshairTool

class Plotter:

    # colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
    colors = ["#000000", "#824737", "#67923D", "#D6562B", "#007042", "#F09B36", "#74CCE5", "#F4BB3A", "#00BBD6", "#ABC178", "#C6A9B5", "#9C8156", "#895881", "#BC9F77"]
    prov_colors = ["#824737", "#67923D", "#D6562B"]

    data = {
        'All': pd.DataFrame(),
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
        # recovered = json_normalize((requests.request("GET", "https://api.covid19api.com/dayone/country/Canada/status/recovered", headers={}, data={})).json())
        # recovered = recovered.groupby(['Province'])
        deaths = json_normalize((requests.request("GET", "https://api.covid19api.com/dayone/country/Canada/status/deaths", headers={}, data={})).json())
        deaths = deaths.groupby(['Province'])

        # TODO: Fix this code
        # for prov in self.data:
        #     if prov not in cases.groups:
        #         pass
        #     else:
        #         df = cases.get_group(prov)
        #         recovered_df = recovered.get_group(prov)
        #         deaths_df = deaths.get_group(prov)
        #         index=np.arange(0, len(df.index))
        #         df.set_index(index, inplace=True)
        #         recovered_df.set_index(index, inplace=True)
        #         deaths_df.set_index(index, inplace=True)

        #         df = df[['Date','Cases']]
        #         # print(prov)
        #         # print(df.tail())

        #         df['Recovered'] = recovered_df['Cases']
        #         df['Deaths'] = deaths_df['Cases']

        #         df['Date'] = df['Date'].apply(lambda x: x[0:10])
        #         df['Date'] = pd.to_datetime(df['Date'])

        #         # print(df.tail())
        #         df['DailyCases'] = (df['Cases'] - df['Recovered'] - df['Deaths'])
        #         self.data[prov] = df

        for prov in self.data:
            if prov != "All" and prov not in cases.groups:
                pass
            else:
                if prov == "All":
                    df = cases.get_group("")
                    deaths_df = deaths.get_group("")
                else:
                    df = cases.get_group(prov)
                    deaths_df = deaths.get_group(prov)
                df = df[['Date', 'Cases']]
                index = np.arange(0, len(df.index))
                df.set_index(index, inplace=True)
                deaths_df.set_index(index, inplace=True)
                df['Deaths'] = deaths_df['Cases']
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

        p = figure(title="Daily Increase in COVID-19 Cases by Province", x_axis_type='datetime', plot_height=500, plot_width=1600, sizing_mode='stretch_width', x_axis_label='Date', y_axis_label='Increase in Cases')
        
        for data, name, color in zip(self.data.values(), self.data.keys(), self.colors):
            size = len(data)
            names = [name for x in range(size)]             # Create names for tooltips
            source = ColumnDataSource(data={
                'Date': data['Date'],
                'CaseIncrease': data['DailyCases'],
                'Province': names,
            })
            if name == "All":
                p.line(x='Date', y='CaseIncrease', line_width=4, color=color, alpha=0.4, legend_label=name, source=source)
            else:
                p.line(x='Date', y='CaseIncrease', line_width=2, color=color, alpha=0.9, legend_label=name, source=source)
        p.legend.location='top_left'
        
        # Add hover information
        p.add_tools(HoverTool(
            tooltips=[
                ('Province', '@Province'),
                ('Increase', '@CaseIncrease{0}'),
                ('Date', '@Date{%F}'),
            ],
            formatters={
                '@Date': 'datetime',
                'CaseIncrease': 'printf',
            }
        ))

        p.add_tools(CrosshairTool())

        return p

    def plot_province(self, prov):
        p = figure(title=(f"{prov} COVID-19 Data"), x_axis_type='datetime', plot_height=250, plot_width=300, sizing_mode='stretch_width')
        df = self.data[prov]
        source = ColumnDataSource(data={
            'Date': df['Date'],
            'Cases': df['Cases'],
            'Deaths': df['Deaths'],
            'CaseIncrease': df['DailyCases']
        })
        if prov == "All":
            pass
        else:
            p.line(x='Date', y='Cases', line_width=4, color=self.prov_colors[0], alpha=0.7, legend_label='Cases', source=source)
            p.line(x='Date', y='Deaths', line_width=4, color=self.prov_colors[1], alpha=0.7, legend_label='Deaths', source=source)
            p.line(x='Date', y='CaseIncrease', line_width=4, color=self.prov_colors[2], alpha=0.7, legend_label='Daily Case Increase', source=source)
            p.legend.location='center_right'

        return(p)
        
    # End Code

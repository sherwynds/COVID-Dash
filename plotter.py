import json
import requests
import pandas as pd
from pandas import json_normalize
import numpy as np
import bokeh
from bokeh.plotting import figure


class Plotter:

    BC = pd.DataFrame()

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
        'Nunavut': pd.DataFrame(),
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
                


    
    def plot_BC_cases(self):
        p = figure(title="BC Test Plot", x_axis_type='datetime', plot_height=700, plot_width=1400)
        x = self.BC['Date']
        y = self.BC['DailyCases']
        print(x)
        print(y)
        p.line(x,y)
        return p
        

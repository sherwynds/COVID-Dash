import json
import requests
import pandas as pd
from pandas import json_normalize

class Plotter:

    raw_data = pd.DataFrame()
    BC_cases = pd.DataFrame()
    ON_cases = pd.DataFrame()

    def __init__(self):
        self.raw_data = json_normalize((requests.request("GET", "https://api.covid19api.com/dayone/country/Canada/status/confirmed", headers={}, data={})).json())
        self.raw_data = self.raw_data.groupby(['Province'])
        self.BC_cases = self.raw_data.get_group("British Columbia")



p = Plotter()
print(p.BC_cases.head())
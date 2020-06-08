import json
import requests
import pandas as pd
from pandas import json_normalize

class Plotter:

    cases = pd.DataFrame()

    def __init__(self):
        self.cases = json_normalize((requests.request("GET", "https://api.covid19api.com/dayone/country/Canada/status/confirmed", headers={}, data={})).json())

p = Plotter()
print(p.cases.head(100))
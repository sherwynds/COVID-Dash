import json
import gunicorn


from flask import Flask
from jinja2 import Template

from plotter import Plotter
from bokeh.embed import json_item
from bokeh.resources import CDN

app = Flask(__name__)

# Basic webpage
page = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  {{ resources }}
  <title> Canadian COVID Dashboard </title>
  <h1> Canada COVID Case Tracker </h1>
</head>
<body>
  <div id="mainplot"></div>
  <div> Note: Nunavut is not included because it has no confirmed cases. Data sourced from https://api.covid19api.com/. </div>
  <script>
  fetch('/mainplot')
    .then(function(response) { return response.json(); })
    .then(function(item) { return Bokeh.embed.embed_item(item); })
  </script>
</body>
""")

@app.route('/')
def root():
    return page.render(resources=CDN.render())

# Plots the main chart comparing new covid cases
@app.route('/mainplot')
def plot():
    plotter = Plotter()
    p = plotter.plot_cases()
    return json.dumps(json_item(p, "mainplot"))

if __name__ == '__main__':
    app.run()
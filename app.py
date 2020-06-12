import json
import gunicorn


from flask import Flask
from jinja2 import Template

from plotter import Plotter
from bokeh.embed import json_item
from bokeh.resources import CDN

app = Flask(__name__)
plotter = Plotter()

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
  <div class="row">
    <div class="column">
      <div id="yt"></div>
      <div id="bc"></div>
      <div id="nt"></div>
      <div id="ab"></div>
    </div>
    <div class="column">
      <div id="sk"></div>
      <div id="mb"></div>
      <div id="on"></div>
      <div id="qc"></div>
    </div>
    <div class="column">
      <div id="nl"></div>
      <div id="nb"></div>
      <div id="pe"></div>
      <div id="ns"></div>
    </div>
  </div>
  <script>
  fetch('/mainplot')
    .then(function(response) { return response.json(); })
    .then(function(item) { return Bokeh.embed.embed_item(item); })
  </script>
  <script>
  fetch('/bc')
    .then(function(response) {return response.json();})
    .then(function(item) {return Bokeh.embed.embed_item(item);})
  </script>
  <script>
    fetch('/ab')
    .then(function(response) {return response.json();})
    .then(function(item) {return Bokeh.embed.embed_item(item);})
  </script>
  <script>
    fetch('/on')
    .then(function(response) {return response.json();})
    .then(function(item) {return Bokeh.embed.embed_item(item);})
  </script>
  <script>
    fetch('/qc')
    .then(function(response) {return response.json();})
    .then(function(item) {return Bokeh.embed.embed_item(item);})
  </script>
</body>
""")

@app.route('/')
def root():
    return page.render(resources=CDN.render())

# Plots the main chart comparing new covid cases
@app.route('/mainplot')
def plot():
    p = plotter.plot_cases()
    return json.dumps(json_item(p, "mainplot"))

@app.route('/bc')
def bc_plot():
  p = plotter.plot_province("British Columbia")
  return json.dumps(json_item(p, "bc"))

@app.route('/ab')
def ab_plot():
  p = plotter.plot_province("Alberta")
  return json.dumps(json_item(p, "ab"))

@app.route('/on')
def on_plot():
  p = plotter.plot_province("Ontario")
  return json.dumps(json_item(p, "on"))

@app.route('/qc')
def qc_plot():
  p = plotter.plot_province("Quebec")
  return json.dumps(json_item(p, "qc"))

if __name__ == '__main__':
    app.run()
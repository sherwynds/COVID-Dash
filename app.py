import json
import gunicorn


from flask import Flask, render_template
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
  <link rel="stylesheet" href="styles.css">
  <title> Canadian COVID Dashboard </title>
  <h1> Canada COVID Case Tracker </h1>
</head>
<body>
  <div id="mainplot"></div>
  <div> Note: Nunavut is not included because it has no confirmed cases. Data sourced from https://api.covid19api.com/. </div>
  <div class="row">
    <div class="column">
      <div id="bc">British Columbia</div>
    </div>
    <div class="column">
      <div id="ab">Alberta</div>
    </div>
    <div class="column">
      <div id="on">Ontario</div>
    </div>
  </div>
  <div id="qc">Quebec</div>
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
  return render_template("index.html")
    #return page.render(resources=CDN.render())

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

@app.route('/sk')
def sk_plot():
  p = plotter.plot_province("Saskatchewan")
  return json.dumps(json_item(p, "sk"))

@app.route('/mb')
def mb_plot():
  p = plotter.plot_province("Manitoba")
  return json.dumps(json_item(p, "mb"))

@app.route('/qc')
def qc_plot():
  p = plotter.plot_province("Quebec")
  return json.dumps(json_item(p, "qc"))


@app.route('/ns')
def ns_plot():
  p = plotter.plot_province("Nova Scotia")
  return json.dumps(json_item(p, "ns"))

@app.route('/nb')
def nb_plot():
  p = plotter.plot_province("New Brunswick")
  return json.dumps(json_item(p, "nb"))

@app.route('/nl')
def nl_plot():
  p = plotter.plot_province("Newfoundland and Labrador")
  return json.dumps(json_item(p, "nl"))

@app.route('/yt')
def yt_plot():
  p = plotter.plot_province("Yukon")
  return json.dumps(json_item(p, "yt"))

@app.route('/nt')
def nt_plot():
  p = plotter.plot_province("Northwest Territories")
  return json.dumps(json_item(p, "nt"))

@app.route('/pe')
def pe_plot():
  p = plotter.plot_province("Prince Edward Island")
  return json.dumps(json_item(p, "pe"))

if __name__ == '__main__':
    app.run()
import json


from flask import Flask
from jinja2 import Template

from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.resources import CDN

app = Flask(__name__)


page = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  {{ resources }}
  <title> COVID-19 Dashboard </title>
  <h1> COVID-19 Dashboard </h1>
</head>
<body>
  <div id="mainplot"></div>
  <script>
  fetch('/mainplot')
    .then(function(response) { return response.json(); })
    .then(function(item) { return Bokeh.embed.embed_item(item); })
  </script>
</body>
""")

def make_plot():
    p = figure(title = "Canada COVID Information")
    x = [1,2,3,4,5,6,7,8,9,10]
    y = [1,4,9,16,25,36,49,64,81,100]
    p.line(x, y)
    return p

@app.route('/')
def root():
    return page.render(resources=CDN.render())

@app.route('/mainplot')
def plot():
    p = make_plot()
    return json.dumps(json_item(p, "mainplot"))

if __name__ == '__main__':
    app.run()
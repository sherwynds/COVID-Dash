# COVID-Dash
📉 Interactive Flask/Bokeh dashboard for COVID-19 data in Canada: [covid-can-dash.herokuapp.com](http://covid-can-dash.herokuapp.com/)

The website might take long to load on Heroku because it puts the web app to sleep when not in use. It will load much faster locally. 

**IMPORTANT NOTE: The above link will not display graphs correctly right now, as the code needs to be updated follwoing changes to the upstream API it depends on.**

![image](https://user-images.githubusercontent.com/4008778/84304791-e994f780-ab0d-11ea-87f2-4080d0f1be76.PNG)

Our lives have been structurally and materially altered by the global pandemic in a multitude of ways. Interested in analyzing the growth rate of the novel coronavirus, I built a web app to calculate and track the increase in total coronavirus cases by province in Canada. It pulls JSON data from [api.covid19api.com](https://api.covid19api.com/).

Check out the link to the live web app, or clone this repository, run `pip install -r requirements.txt` and then `flask run`.

Special thanks to Michelle Illing for curating the color palette.



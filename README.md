# bokeh-weather-plots

[![CI](https://github.com/roberto-aldera/bokeh-weather-plots/actions/workflows/python-app.yml/badge.svg)](https://github.com/roberto-aldera/bokeh-weather-plots/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/roberto-aldera/bokeh-weather-plots/branch/main/graph/badge.svg?token=GDN7W7WRU9)](https://codecov.io/gh/roberto-aldera/bokeh-weather-plots)

A place to play with Bokeh plots and look at some local weather data from the [Radcliffe Observatory](https://www.geog.ox.ac.uk/research/climate/rms/daily-data.html).

Code coverage can be checked using `coverage`, which can also generate an HTML to assess each line:
```
coverage run --source . -m pytest && coverage html
```
(maybe one day this will be a fancy badge)

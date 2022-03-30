import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, save
from bokeh.palettes import Category10_10 as palette

PLOT_WIDTH = 1200
BACKGROUND_COLOUR = "#fafafa"


def main():
    # Data from https://www.geog.ox.ac.uk/research/climate/rms/daily-data.html
    weather_data_raw = pd.read_csv("daily-data-to-dec-2020.csv")

    # handle non-numeric instances like where data is missing
    weather_data_raw = weather_data_raw.apply(pd.to_numeric, errors="coerce")

    weather_data_subset = weather_data_raw[weather_data_raw["YYYY"] >= 2019]
    weather_data = weather_data_subset.reset_index(drop=True)

    # Make a datetime column to use as x-index
    weather_data = weather_data.rename(
        columns={"YYYY": "year", "MM": "month", "DD": "day"})
    weather_data["datetime"] = pd.to_datetime(
        weather_data[["day", "month", "year"]])

    weather_data["left"] = weather_data["datetime"] - pd.DateOffset(days=0.5)
    weather_data["right"] = weather_data["datetime"] + pd.DateOffset(days=0.5)

    print("Running...")
    # set output to static HTML file
    output_file(filename="/tmp/output.html", title="Weather data")
    source = ColumnDataSource(weather_data)

    # create plots
    s1 = figure(background_fill_color=BACKGROUND_COLOUR,
                sizing_mode="stretch_width", width=PLOT_WIDTH, x_axis_type='datetime')
    s1.quad(top="Tmax °C", bottom="Tmin °C", left="left", right="right",
            source=source, color=palette[0], alpha=0.2, legend_label="min/max")

    s2 = figure(background_fill_color=BACKGROUND_COLOUR, width=PLOT_WIDTH)
    s2.circle(x="index", y="Daily Tmean °C", source=source, color=palette[1],
              size=5, alpha=0.8, legend_label="Mean temperature")

    # make a grid and save to file
    grid_plot = gridplot([[s1], [s2]])
    save(grid_plot)


if __name__ == "__main__":
    main()

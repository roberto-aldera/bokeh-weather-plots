import pandas as pd
from argparse import ArgumentParser
from bokeh.models import ColumnDataSource, WheelZoomTool
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, save
from bokeh.palettes import Category10_10 as palette

PLOT_WIDTH = 1200
BACKGROUND_COLOUR = "#fafafa"


def main(args):
    # Data from https://www.geog.ox.ac.uk/research/climate/rms/daily-data.html
    weather_data_raw = pd.read_csv("daily-data-to-dec-2020.csv")

    # handle non-numeric instances like where data is missing
    weather_data_raw = weather_data_raw.apply(pd.to_numeric, errors="coerce")

    weather_data_subset = weather_data_raw[((weather_data_raw["YYYY"] >= args.start_year) & (
        weather_data_raw["YYYY"] <= args.start_year + (args.num_years-1)))]

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
    output_file(filename=f"{args.output_dir}/weather_plots.html",
                title="Weather data")
    source = ColumnDataSource(weather_data)
    tools = "pan, wheel_zoom, xbox_select, reset"

    # create plots
    s1 = figure(background_fill_color=BACKGROUND_COLOUR, tools=tools,
                sizing_mode="stretch_width", width=PLOT_WIDTH, x_axis_type="datetime")
    s1.toolbar.active_scroll = s1.select_one(WheelZoomTool)
    s1.quad(top="Tmax °C", bottom="Tmin °C", left="left", right="right",
            source=source, color=palette[0], alpha=0.2, legend_label="min/max")

    s2 = figure(background_fill_color=BACKGROUND_COLOUR, tools=tools,
                width=PLOT_WIDTH, x_axis_type="datetime", x_range=s1.x_range)
    s2.toolbar.active_scroll = s2.select_one(WheelZoomTool)
    s2.circle(x="datetime", y="Daily Tmean °C", source=source, color=palette[1],
              size=5, alpha=0.8, legend_label="Mean temperature")

    # make a grid and save to file
    grid_plot = gridplot([[s1], [s2]])
    save(grid_plot)


if __name__ == "__main__":
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--output_dir", type=str, default="",
                        help="Path to folder where outputs will be saved")
    parser.add_argument("--start_year", type=int, default=2019,
                        help="Year from which to start analysis")
    parser.add_argument("--num_years", type=int, default=1,
                        help="Number of years to analyse")
    args = parser.parse_args()

    if args.start_year < 1815 or args.start_year > 2020:
        raise ValueError(
            f"Invalid start year: {args.start_year} - this must be between 1815 and 2020.")

    if args.start_year + (args.num_years-1) > 2020:
        print(
            f"The requested start year ({args.start_year}) plus the entered "
            f"number of years ({args.num_years}) exceeds the latest available data from the end of 2020. "
            "Truncating to the end of 2020.")
        args.num_years = 2020 - args.start_year + 1

    main(args)

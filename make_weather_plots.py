import argparse
import pandas as pd
from argparse import ArgumentParser
from bokeh.models import ColumnDataSource, WheelZoomTool
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, save
from bokeh.palettes import Category10_10 as palette
from utilities import get_historical_data

PLOT_WIDTH = 1200
PLOT_HEIGHT = 300
BACKGROUND_COLOUR = "#fafafa"


def prepare_weather_dataframe(args: argparse.Namespace, weather_data_raw: pd.DataFrame) -> pd.DataFrame:
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

    return weather_data


def make_bokeh_plots(weather_data, historical_day_records, args):
    # set output to static HTML file
    output_file(filename=f"{args.output_dir}/weather_plots.html",
                title="Weather data")

    source = ColumnDataSource(weather_data)
    records_source = ColumnDataSource(historical_day_records)
    tools = "pan, wheel_zoom, box_select, reset"

    # create plots
    temp_range_plot = figure(background_fill_color=BACKGROUND_COLOUR, tools=tools,
                             sizing_mode="stretch_width", width=PLOT_WIDTH, height=PLOT_HEIGHT,
                             x_axis_type="datetime")
    temp_range_plot.toolbar.active_scroll = temp_range_plot.select_one(
        WheelZoomTool)
    temp_range_plot.quad(top="Tmax-degC", bottom="Tmin-degC", left="left", right="right",
                         source=records_source, color=palette[0], alpha=0.2, legend_label="Record temperature")
    temp_range_plot.quad(top="Tmax °C", bottom="Tmin °C", left="left", right="right",
                         source=source, color=palette[0], alpha=0.5, legend_label="Temperature range")

    mean_temp_plot = figure(background_fill_color=BACKGROUND_COLOUR, tools=tools,
                            width=PLOT_WIDTH, height=PLOT_HEIGHT, x_axis_type="datetime",
                            x_range=temp_range_plot.x_range)
    mean_temp_plot.toolbar.active_scroll = mean_temp_plot.select_one(
        WheelZoomTool)
    mean_temp_plot.circle(x="datetime", y="Daily Tmean °C", source=source, color=palette[0],
                          size=5, alpha=0.8, legend_label="Mean temperature")

    min_temp_plot = figure(background_fill_color=BACKGROUND_COLOUR, tools=tools,
                           width=PLOT_WIDTH, height=PLOT_HEIGHT, x_axis_type="datetime",
                           x_range=temp_range_plot.x_range)
    min_temp_plot.toolbar.active_scroll = min_temp_plot.select_one(
        WheelZoomTool)
    min_temp_plot.circle(x="datetime", y="Tmin °C", source=source, color=palette[0],
                         size=5, alpha=0.8, legend_label="Min temperature")

    max_temp_plot = figure(background_fill_color=BACKGROUND_COLOUR, tools=tools,
                           width=PLOT_WIDTH, height=PLOT_HEIGHT, x_axis_type="datetime",
                           x_range=temp_range_plot.x_range)
    max_temp_plot.toolbar.active_scroll = max_temp_plot.select_one(
        WheelZoomTool)
    max_temp_plot.circle(x="datetime", y="Tmax °C", source=source, color=palette[0],
                         size=5, alpha=0.8, legend_label="Max temperature")

    rainfall_plot = figure(background_fill_color=BACKGROUND_COLOUR, tools=tools,
                           width=PLOT_WIDTH, height=PLOT_HEIGHT, x_axis_type="datetime",
                           x_range=temp_range_plot.x_range)
    rainfall_plot.toolbar.active_scroll = rainfall_plot.select_one(
        WheelZoomTool)
    rainfall_plot.circle(x="datetime", y="Rainfall mm raw incl traces", source=source, color=palette[0],
                         size=5, alpha=0.8, legend_label="Rainfall (mm)")

    sunlight_plot = figure(background_fill_color=BACKGROUND_COLOUR, tools=tools,
                           width=PLOT_WIDTH, height=PLOT_HEIGHT, x_axis_type="datetime",
                           x_range=temp_range_plot.x_range)
    sunlight_plot.toolbar.active_scroll = sunlight_plot.select_one(
        WheelZoomTool)
    sunlight_plot.circle(x="datetime", y="Sunshine duration h", source=source, color=palette[0],
                         size=5, alpha=0.8, legend_label="Sunshine duration")

    # make a grid and save to file
    grid_plot = gridplot([[temp_range_plot], [mean_temp_plot], [
                         min_temp_plot], [max_temp_plot], [rainfall_plot], [sunlight_plot]])
    save(grid_plot)


def main(args=None):
    print("Running...")
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--output_dir", type=str, default="",
                        help="Path to folder where outputs will be saved")
    parser.add_argument("--start_year", type=int, default=2020,
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

    weather_data_raw = pd.read_csv("daily-data-to-dec-2020.csv")
    # handle non-numeric instances like where data is missing
    weather_data_raw = weather_data_raw.apply(pd.to_numeric, errors="coerce")

    weather_data = prepare_weather_dataframe(args, weather_data_raw)

    historical_day_records = get_historical_data(
        args.start_year, args.num_years, weather_data_raw)

    make_bokeh_plots(weather_data, historical_day_records, args)


if __name__ == "__main__":
    main()

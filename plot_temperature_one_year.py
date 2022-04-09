import argparse
import pandas as pd
from argparse import ArgumentParser
from pathlib import Path
import matplotlib.pyplot as plt
from utilities import get_historical_data


def prepare_weather_dataframe(args: argparse.Namespace, weather_data_raw: pd.DataFrame):
    # Possible alteration: make this index relevant for current month (perhaps 15 days either side of today?)
    # Crop dataset to cover selected years
    weather_data_subset = weather_data_raw[(
        (weather_data_raw["YYYY"] == args.year))]

    weather_data = weather_data_subset.reset_index(drop=True)

    # Make a datetime column to use as x-index
    weather_data = weather_data.rename(
        columns={"YYYY": "year", "MM": "month", "DD": "day"})
    weather_data["datetime"] = pd.to_datetime(
        weather_data[["day", "month", "year"]])

    weather_data["left"] = weather_data["datetime"] - pd.DateOffset(days=0.5)
    weather_data["right"] = weather_data["datetime"] + pd.DateOffset(days=0.5)

    return weather_data


def make_plots(output_file, weather_data, historical_day_records):
    _, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
    ax.plot(weather_data["datetime"], weather_data["Daily Tmean °C"], '*-',
            color="tab:blue", label="Mean temp")
    ax.bar(x=historical_day_records["datetime"],
           height=historical_day_records["Tmax-degC"] -
           historical_day_records["Tmin-degC"],
           bottom=historical_day_records["Tmin-degC"],
           width=1.0,
           linewidth=1.0,
           edgecolor="tab:blue",
           facecolor="tab:blue",
           alpha=0.25,
           label="Record temperature")

    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()

    plt.savefig(output_file)
    plt.close()

    print("Plots generated and written to:", output_file)


def main(args_list=None):
    print("Running...")
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--output_dir", type=Path, default="",
                        help="Path to folder where outputs will be saved")
    parser.add_argument("--year", type=int, default=2019,
                        help="Year for which to run analysis")
    args = parser.parse_args(args_list)

    if args.year < 1815 or args.year > 2020:
        raise ValueError(
            f"Invalid start year: {args.year} - this must be between 1815 and 2020.")

    weather_data_raw = pd.read_csv("daily-data-to-dec-2020.csv", dtype=str)
    # handle non-numeric instances like where data is missing
    weather_data_raw = weather_data_raw.apply(pd.to_numeric, errors="coerce")

    weather_data = prepare_weather_dataframe(args,
                                             weather_data_raw)
    historical_day_records = get_historical_data(
        start_year=args.year, num_years=1, weather_data_raw=weather_data_raw)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    make_plots(args.output_dir / "one_year_temperature.pdf",
               weather_data, historical_day_records)


if __name__ == "__main__":
    main()
